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

    def intersect(self, origin, direction):
        L = mb.subtract_vectors(origin, self.position)
        a = direction[0] * direction[0] + direction[2] * direction[2]
        b = 2 * (L[0] * direction[0] + L[2] * direction[2])
        c = L[0] * L[0] + L[2] * L[2] - self.radius * self.radius

        discriminant = b * b - 4 * a * c

        if discriminant < 0:
            return None

        t1 = (-b - sqrt(discriminant)) / (2 * a)
        t2 = (-b + sqrt(discriminant)) / (2 * a)

        if t1 > t2:
            t1, t2 = t2, t1

        y1 = L[1] + t1 * direction[1]
        y2 = L[1] + t2 * direction[1]

        if (y1 < 0 and y2 < 0) or (y1 > self.height and y2 > self.height):
            return None

        t = t1 if 0 <= y1 <= self.height else t2
        point = mb.add_vectors(origin, mb.multiply_ve(direction, t))

        if 0 <= y1 <= self.height:
            normal = mb.normalize(mb.subtract_vectors(point, mb.add_vectors(self.position, (0, 0, 0))))
        else:
            normal = mb.normalize(mb.subtract_vectors(point, mb.add_vectors(self.position, (0, self.height, 0))))

        return Intercept(distance=t, point=point, normal=normal, texcoords=None, obj=self)

    def normal(self, point):
        if point[1] <= 0:
            return mb.normalize(mb.subtract_vectors(point, mb.add_vectors(self.position, (0, 0, 0))))
        elif point[1] >= self.height:
            return mb.normalize(mb.subtract_vectors(point, mb.add_vectors(self.position, (0, self.height, 0))))
        else:
            return mb.normalize(mb.subtract_vectors(point, mb.add_vectors(self.position, (0, point[1], 0))))
        

# Figure Triangle
# The atributtes of the triangle are the vertices and material
class Triangle(Shape):
    def __init__(self, vertices, material):
        super().__init__(position=vertices[0], material=material)
        self.vertices = vertices

    def intersect(self, origin, direction):
        v0, v1, v2 = self.vertices

        edge1 = mb.subtract_vectors(v1, v0)
        edge2 = mb.subtract_vectors(v2, v0)
        edge_cross = mb.cross_product(edge1, edge2)
        normal = mb.normalize(edge_cross)

        d = mb.dot_product(normal, v0)

        denominator = mb.dot_product(normal, direction)
        if abs(denominator) < 0.0001:
            return None

        t = (d - mb.dot_product(normal, origin)) / denominator
        if t < 0:
            return None

        point = mb.add_vectors(origin, mb.multiply_ve(direction, t))

        edge0 = mb.subtract_vectors(v0, v2)
        if mb.dot_product(normal, mb.cross_product(edge0, mb.subtract_vectors(point, v2))) < 0:
            return None

        edge1 = mb.subtract_vectors(v1, v0)
        if mb.dot_product(normal, mb.cross_product(edge1, mb.subtract_vectors(point, v0))) < 0:
            return None

        edge2 = mb.subtract_vectors(v2, v1)
        if mb.dot_product(normal, mb.cross_product(edge2, mb.subtract_vectors(point, v1))) < 0:
            return None

        c0 = mb.dot_product(edge0, mb.subtract_vectors(point, v2))
        c1 = mb.dot_product(edge1, mb.subtract_vectors(point, v0))
        c2 = mb.dot_product(edge2, mb.subtract_vectors(point, v1))
        total = c0 + c1 + c2
        u = c1 / total
        v = c2 / total

        return Intercept(distance=t,
                         point=point,
                         normal=normal,
                         texcoords=(u, 1-v),
                         obj=self)
        

# Figure Pyramid, it can use the Triangle class to create the sides
# The atributtes of the pyramid are the position, width, height, lenght and material
class Pyramid(Shape):
    def __init__(self, position, width, height, lenght, material):
        super().__init__(position=position, material=material)
        self.width = width
        self.height = height
        self.lenght = lenght

    def intersect(self, origin, direction):

        v0 = (-self.width / 2, 0, -self.lenght / 2)
        v1 = (-self.width / 2, 0, self.lenght / 2)
        v2 = (self.width / 2, 0, self.lenght / 2)
        v3 = (self.width / 2, 0, -self.lenght / 2)

        apex = (0, self.height, 0)

        v0 = mb.add_vectors(v0, self.position)
        v1 = mb.add_vectors(v1, self.position)
        v2 = mb.add_vectors(v2, self.position)
        v3 = mb.add_vectors(v3, self.position)
        apex = mb.add_vectors(apex, self.position)

        triangles = []
        triangles.append(Triangle((v0, v1, v2), self.material))
        triangles.append(Triangle((v0, v2, v3), self.material))

        triangles.append(Triangle((v0, v1, apex), self.material))
        triangles.append(Triangle((v1, v2, apex), self.material))
        triangles.append(Triangle((v2, v3, apex), self.material))
        triangles.append(Triangle((v3, v0, apex), self.material))

        closestIntercept = None
        for triangle in triangles:
            intercept = triangle.intersect(origin, direction)
            if intercept is not None:
                if closestIntercept is None or intercept.distance < closestIntercept.distance:
                    closestIntercept = intercept

        if closestIntercept:
            return Intercept(distance=closestIntercept.distance,
                            point=closestIntercept.point,
                            normal=closestIntercept.normal,
                            texcoords=closestIntercept.texcoords,
                            obj=self)
        return None
