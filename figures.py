import mathbuddy as mb
from math import tan, pi, atan2, acos, sqrt

class Intercept(object):
  def __init__(self, distance, point, normal, obj, texcoords):
    self.distance = distance
    self.point = point
    self.normal = normal
    self.obj = obj
    self.texcoords = texcoords


class Shape:
  def __init__(self, position, material):
    self.position = position
    self.material = material

  def intersect(self, origin, direction):
    return None

  def normal(self, point):
    raise NotImplementedError()
  

class Sphere(Shape):
    def __init__(self, position, radius, material):
      super().__init__(position, material)
      self.radius = radius

    def intersect(self, origin, direction):
      L = mb.subtract_vectors(self.position, origin)
      lengthL = mb.linalg_norm(L)
      tca = mb.dot_product(L, direction)
      d = (lengthL ** 2 - tca ** 2) ** 0.5

      if d > self.radius:
          return None

      thc = (self.radius ** 2 - d ** 2) ** 0.5
      t0 = tca - thc
      t1 = tca + thc

      if t0 < 0:
          t0 = t1

      if t0 < 0:
          return None

      point = mb.add_vectors(origin, mb.multiply_ve(direction,t0))
      normal = mb.subtract_vectors(point, self.position)
      normal = mb.normalize(normal)
      
      u = (atan2(normal[2], normal[0]) / (2 * pi)+0.5)
      v = acos(normal[1]) / pi
      
      return Intercept(distance=t0,
                        point=point,
                        normal=normal,
                        texcoords=(u, v),
                        obj=self)
      

class Plane(Shape):
    def __init__(self, position, normal, material, repeat_texture=True):
      self.normal = mb.normalize(normal)
      super().__init__(position, material)
      self.repeat_texture = repeat_texture

    def intersect(self, origin, direction):
        denom = mb.dot_product(direction, self.normal)

        if abs(denom) <=0.0001:
            return None

        num = mb.dot_product(mb.subtract_vectors(self.position, origin), self.normal)
        t= num / denom

        if t < 0 :
            return None

        P = mb.add_vectors(origin, mb.multiply_ve(direction, t))

        return Intercept(distance=t,
                         point=P,
                         normal=self.normal,
                         texcoords=None,
                         obj=self)


class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        super().__init__(position, normal, material)
        self.radius = radius

    def intersect(self, origin, direction):
        intersect = super().intersect(origin, direction)

        if intersect is None:
            return None

        distance = mb.subtract_vectors(intersect.point, self.position)     
        distance = mb.magVec(distance)

        if distance > self.radius:
            return None

        return Intercept(distance=intersect.distance,
                         point=intersect.point,
                         normal=intersect.normal,
                         texcoords=None,
                         obj=self)


class Cube(Shape):
    def __init__(self, position, size, material):
        self.size = size
        super().__init__(position, material)

        self.planes = []

        self.size = size

        leftPlane = Plane(mb.add_vectors(position, (-size[0] / 2, 0, 0)), (-1, 0, 0), material)
        rightPlane = Plane(mb.add_vectors(position, (size[0] / 2, 0, 0)), (1, 0, 0), material)

        topPlane = Plane(mb.add_vectors(position, (0, size[1] / 2, 0)), (0, 1, 0), material)
        bottomPlane = Plane(mb.add_vectors(position, (0, -size[1] / 2, 0)), (0, -1, 0), material)

        frontPlane = Plane(mb.add_vectors(position, (0, 0, size[2]/ 2)), (0, 0, 1), material)
        backPlane = Plane(mb.add_vectors(position, (0, 0, -size[2]/ 2)), (0, 0, -1), material)

        self.planes.append(leftPlane)
        self.planes.append(rightPlane)
        self.planes.append(topPlane)
        self.planes.append(bottomPlane)
        self.planes.append(frontPlane)
        self.planes.append(backPlane)

        self.boundsMin =[0,0,0]
        self.boundsMax =[0,0,0]

        bias = 0.0001

        for i in range(3):
            self.boundsMin[i] = self.position[i] - (self.size[i] / 2 + bias)
            self.boundsMax[i] = self.position[i] + self.size[i] / 2 + bias

    def intersect(self, origin, direction):
        intersect = None
        t = float("inf")

        u=0
        v=0

        for plane in self.planes:

            planeIntersect = plane.intersect(origin, direction)

            if planeIntersect is not None:

                planePoint = planeIntersect.point

                if self.boundsMin[0] < planePoint[0] < self.boundsMax[0]:
                    if self.boundsMin[1] < planePoint[1] < self.boundsMax[1]:
                        if self.boundsMin[2] < planePoint[2] < self.boundsMax[2]:
                            if planeIntersect.distance < t:
                                t = planeIntersect.distance
                                intersect = planeIntersect

                                if abs(plane.normal[0])>0:
                                    u= (planePoint[1]-self.boundsMin[1]) / (self.size[1] + 0.002)
                                    v= (planePoint[2]-self.boundsMin[2]) / (self.size[2] + 0.002)
                                elif abs(plane.normal[1])>0:
                                    u= (planePoint[0]-self.boundsMin[0]) / (self.size[0] + 0.002)
                                    v= (planePoint[2]-self.boundsMin[2]) / (self.size[2] + 0.002)
                                elif abs(plane.normal[2])>0:
                                    u= (planePoint[0]-self.boundsMin[0]) / (self.size[0] + 0.002)
                                    v= (planePoint[1]-self.boundsMin[1]) / (self.size[1] + 0.002)

        if intersect is None:
            return None

        return Intercept(distance=t,
                            point=intersect.point,
                            normal=intersect.normal,
                            texcoords=(u,v),
                            obj=self)
        

# Figure Cylinder, it can use the Disk class to create the top and bottom
# The atributtes of the cylinder are the position, radius, height and material

class Cylinder(Shape):
    def __init__(self, position, radius, height, material):
        super().__init__(position, material)
        self.radius = radius
        self.height = height

        self.top = Disk(position=(position[0], position[1] + height / 2, position[2]),
                        normal=(0, 1, 0),
                        radius=radius,
                        material=material)

        self.bottom = Disk(position=(position[0], position[1] - height / 2, position[2]),
                           normal=(0, -1, 0),
                           radius=radius,
                           material=material)

    def intersect(self, origin, direction):
        # Intersect with the top and bottom disks
        top_intersect = self.top.intersect(origin, direction)
        bottom_intersect = self.bottom.intersect(origin, direction)

        # Intersect with the side surface
        side_intersect = self.intersect_side(origin, direction)

        # Determine the closest intersection
        closest_intersect = None

        if top_intersect is not None:
            closest_intersect = top_intersect

        if bottom_intersect is not None:
            if closest_intersect is None or bottom_intersect.distance < closest_intersect.distance:
                closest_intersect = bottom_intersect

        if side_intersect is not None:
            if closest_intersect is None or side_intersect.distance < closest_intersect.distance:
                closest_intersect = side_intersect

        return closest_intersect

    def intersect_side(self, origin, direction):
        a = direction[0] ** 2 + direction[2] ** 2
        b = 2 * (direction[0] * (origin[0] - self.position[0]) + direction[2] * (origin[2] - self.position[2]))
        c = (origin[0] - self.position[0]) ** 2 + (origin[2] - self.position[2]) ** 2 - self.radius ** 2

        discriminant = b ** 2 - 4 * a * c

        if discriminant < 0:
            return None

        t1 = (-b + sqrt(discriminant)) / (2 * a)
        t2 = (-b - sqrt(discriminant)) / (2 * a)

        if t1 > t2:
            t1, t2 = t2, t1

        # Check if the intersection points are within the height of the cylinder
        y1 = origin[1] + t1 * direction[1]
        y2 = origin[1] + t2 * direction[1]

        if y1 > self.position[1] + self.height / 2 or y2 < self.position[1] - self.height / 2:
            return None

        t = t1 if y1 > self.position[1] - self.height / 2 and y1 < self.position[1] + self.height / 2 else t2

        # Calculate the intersection point and normal
        point = mb.add_vectors(origin, mb.multiply_ve(direction, t))
        normal = [point[0] - self.position[0], 0, point[2] - self.position[2]]
        normal = mb.normalize(normal)

        # Calculate texture coordinates
        u = 0.5 + atan2(normal[2], normal[0]) / (2 * pi)
        v = 0.5 - (normal[1] - self.position[1] + self.height / 2) / self.height

        return Intercept(distance=t,
                         point=point,
                         normal=normal,
                         texcoords=(u, v),
                         obj=self)