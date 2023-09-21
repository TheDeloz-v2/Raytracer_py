import mathbuddy as mb
from math import pi, tan

class Raytracer(object):
  def __init__(self, screen):
    self.vpX = 0
    self.vpY = 0
    self.vpWidth = 0
    self.vpHeight = 0
    self.nearPlane = 0
    self.topEdge = 0
    self.rightEdge = 0
    self.ClearColor = None
    self.currColor = None
    
    self.screen = screen
    _,_, self.width, self.height = screen.get_rect()

    self.scene = []
    self.lights = []

    self.camPosition = [0,0,0]

    self.rtViewport(0, 0, self.width, self.height)
    self.rtProjection()

    self.rtClearColor(0,0,0)
    self.rtColor(1,1,1)
    self.rtClear()

  def rtViewport(self, posX, posY, width, height):
    self.vpX = posX
    self.vpY = posY
    self.vpWidth = width
    self.vpHeight = height

  def rtProjection(self, fov= 60, n = 0.1):
    aspectRatio = self.vpWidth / self.vpHeight
    self.nearPlane = n
    self.topEdge = tan(fov * pi / 360) * n
    self.rightEdge = self.topEdge * aspectRatio

  def rtClearColor(self, r, g, b):
    self.ClearColor = (r * 255, g * 255, b * 255)
  
  def rtClear(self):
    self.screen.fill(self.ClearColor)
    
  def rtColor(self, r, g, b):
    self.currColor = (r * 255, g * 255, b * 255)

  def rtPoint(self, x, y, color=None):
    y = self.width - y
    if (0<=x<self.width) and (0<=y<self.height):
      if color != None:
        color = (int(color[0] * 255), 
                 int(color[1] * 255), 
                 int(color[2] * 255))
        self.screen.set_at((x, y), color)
      else:
        self.screen.set_at((x, y), self.currColor)

  def rtCastRay(self, orig, dir, sceneObject=None):
    depth = float('inf')
    hit = None
    
    for obj in self.scene:
      if obj is not sceneObject:
        intercept = obj.intersect(orig, dir)
        if intercept != None:
          if intercept.distance < depth:
            depth = intercept.distance
            hit = intercept
      
    return hit

  def rtRender(self):
    for x in range(self.vpX, self.vpX + self.vpWidth + 1):
      for y in range(self.vpY, self.vpY + self.vpHeight + 1):
        if (0<=x< self.width) and (0<=y<self.height):
          Px = 2 * ((x + 0.5 - self.vpX) / self.vpWidth) -1
          Py = 2 * ((y + 0.5 - self.vpY) / self.vpHeight) -1

          Px *= self.rightEdge
          Py *= self.topEdge

          direction = (Px, Py, -self.nearPlane)
          direction = mb.normalize(direction)

          intercept = self.rtCastRay(self.camPosition, direction)

          if intercept is not None:

            surfaceColor = intercept.obj.material.diffuse

            ambientLight = [0, 0, 0]
            diffuseLightColor = [0, 0, 0]
            specularLightColor = [0, 0, 0]

            for light in self.lights:
              if light.type == "Ambient":
                ambientLight[0] += light.intensity * light.color[0]
                ambientLight[1] += light.intensity * light.color[1]
                ambientLight[2] += light.intensity * light.color[2]

              else:
                shadowDirection = None
                
                if light.type == "Directional":
                  shadowDirection = [i * -1 for i in light.direction]
                
                if light.type == "Point":
                  lightDirection = mb.subtract_vectors(light.position, intercept.point)
                  shadowDirection = mb.normalize(lightDirection)
                  
                shadowIntercept = self.rtCastRay(intercept.point, shadowDirection, intercept.obj)
                
                if shadowIntercept is None:
                  diffColor = light.getDiffuseColor(intercept)
                  diffuseLightColor = [diffuseLightColor[i] + diffColor[i] for i in range(3)]
                  
                  specColor = light.getSpecularColor(intercept, self.camPosition)
                  specularLightColor = [specularLightColor[i] + specColor[i] for i in range(3)]
                  
            lightColor = [ambientLight[i] + diffuseLightColor[i] + specularLightColor[i] for i in range(3)]
            
            finalColor = [surfaceColor[i] * lightColor[i] for i in range(3)]
            finalColor = [min(1, i) for i in finalColor]
            
            self.rtPoint(x, y, finalColor)
      