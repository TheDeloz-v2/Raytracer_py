import mathbuddy as mb

class Intercept(object):
  def __init__(self, distance, point, normal, obj):
    self.distance = distance
    self.point = point
    self.normal = normal
    self.obj = obj


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

      return Intercept(distance=t0,
                        point=point,
                        normal=normal,
                        obj=self)