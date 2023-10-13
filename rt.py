import mathbuddy as mb
from math import pi, tan, atan2, acos
import pygame
from materials import *
import lights

MAX_RECURSION_DEPTH = 4

class Raytracer(object):
    def __init__(self, screen):
        self.vpX = 0
        self.vpY = 0
        self.vpWidth = 0
        self.vpHeight = 0
        self.nearPlane = 0
        self.topEdge = 0
        self.rightEdge = 0
        self.clearColor = None
        self.currentColor = None

        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.scene = []
        self.lights = []

        self.cameraPosition = [0, 0, 0]

        self.rtViewPort(0, 0, self.width, self.height)
        self.rtProjection()

        self.rtClearColor(0, 0, 0)
        self.rtColor(1, 1, 1)
        self.rtClear()

        self.envMap = None

    def rtViewPort(self, x, y, width, height):
        self.vpX = x
        self.vpY = y
        self.vpWidth = width
        self.vpHeight = height

    def rtProjection(self, fov=60, near=0.1):
        aspectRatio = self.vpWidth / self.vpHeight
        self.nearPlane = near
        self.topEdge = near * tan(fov * pi / 360)
        self.rightEdge = self.topEdge * aspectRatio

    def rtClearColor(self, r, g, b):
        self.clearColor = (r * 255, g * 255, b * 255)

    def rtColor(self, r, g, b):
        self.currentColor = (r * 255, g * 255, b * 255)

    def rtClear(self):
        self.screen.fill(self.clearColor)

    def rtPoint(self, x, y, color=None):
        y = self.width - y
        if (0 <= x < self.width) and (0 <= y < self.height):
            if color is None:
                color = self.currentColor
            else:
                color = (color[0] * 255, color[1] * 255, color[2] * 255)

            self.screen.set_at((x, y), color)

    def rtCastRay(self, origin, direction, sceneObject=None, recursion=0):
        if recursion >= MAX_RECURSION_DEPTH:
            return None
        
        depth = float("inf")
        intercept = None
        hit = None

        for obj in self.scene:
            if obj is not sceneObject:
                intercept = obj.intersect(origin, direction)
                if intercept is not None:
                    if intercept.distance < depth:
                        depth = intercept.distance
                        hit = intercept

        return hit

    def rtRayColor(self, intercept, rayDirection, recursion=0):
        if intercept is None:
            if self.envMap:
                x = (atan2(rayDirection[2], rayDirection[0]) / (2 * pi)+0.5)*self.envMap.get_width()
                y = acos(rayDirection[1]) / pi * self.envMap.get_height()

                envColor = self.envMap.get_at((int(x), int(y)))

                return [envColor[i]/255 for i in range(3)]
            
            else:
                color = self.clearColor
                return [envColor[i]/255 for i in range(3)]
                

        material = intercept.obj.material
        surfaceColor = material.diffuse
        if material.texture and intercept.texcoords:
            tx = int(intercept.texcoords[0] * material.texture.get_width()-1)
            ty = int(intercept.texcoords[1] * material.texture.get_height()-1)
            texColor = material.texture.get_at((tx, ty))
            texColor = [i / 255 for i in texColor]
            surfaceColor = [surfaceColor[i] * texColor[i] for i in range(3)]

        reflectColor = [0, 0, 0]
        refractColor = [0, 0, 0]
        ambientLightColor = [0, 0, 0]
        diffuseLightColor = [0, 0, 0]
        specularLightColor = [0, 0, 0]
        finalColor = [0, 0, 0]

        if material.matType == OPAQUE:
            for light in self.lights:
                if light.type == "AMBIENT":
                    color = light.getColor()
                    ambientLightColor = [ambientLightColor[i] + color[i] for i in range(3)]
                else:
                    shadowDirection = None
                    if light.type == "DIRECTIONAL":
                        shadowDirection = [i * -1 for i in light.direction]
                    if light.type == "POINT":
                        lightDirection = mb.subtract_vectors(light.position, intercept.point)
                        shadowDirection = mb.normalize(lightDirection)

                    shadowIntersect = self.rtCastRay(intercept.point, shadowDirection, intercept.obj)

                    if shadowIntersect is None:
                        diffColor = light.getDiffuseColor(intercept)
                        diffuseLightColor = [diffuseLightColor[i] + diffColor[i] for i in range(3)]

                        specColor = light.getSpecularColor(intercept, self.cameraPosition)
                        specularLightColor = [specularLightColor[i] + specColor[i] for i in range(3)]


        elif material.matType == REFLECTIVE:
            reflect = lights.reflect(intercept.normal, mb.negativeTuple(rayDirection))
            reflectIntercept = self.rtCastRay(intercept.point, reflect, intercept.obj, recursion + 1)
            reflectColor = self.rtRayColor(reflectIntercept, reflect, recursion + 1)
            
            for light in self.lights:
                if light.type != "AMBIENT":
                    lightDir = None
                    if light.type == "DIRECTIONAL":
                        lightDir = [i * -1 for i in light.direction]
                    if light.type == "POINT":
                        lightDir = mb.subtract_vectors(light.position, intercept.point)
                        lightDir = mb.normalize(lightDir)
                    
                    shadowIntersect = self.rtCastRay(intercept.point, lightDir, intercept.obj)
                    if shadowIntersect is None:
                        specColor = light.getSpecularColor(intercept, self.cameraPosition)
                        specularLightColor = [specularLightColor[i] + specColor[i] for i in range(3)]
            

        elif material.matType == TRANSPARENT:
            outside = mb.dot_product(rayDirection, intercept.normal) < 0
            bias = mb.multiply_ve(intercept.normal, 0.001)

            reflect = lights.reflect(intercept.normal, mb.negativeTuple(rayDirection))
            reflectOrig = mb.add_vectors(intercept.point, bias) if outside else mb.subtract_vectors(intercept.point, bias)
            reflectIntercept = self.rtCastRay(reflectOrig, reflect, None, recursion + 1)
            reflectColor = self.rtRayColor(reflectIntercept, reflect, recursion + 1)

            for light in self.lights:
                if light.type != "AMBIENT":
                    shadowDirection = None
                    if light.type == "DIRECTIONAL":
                        shadowDirection = [i * -1 for i in light.direction]
                    if light.type == "POINT":
                        lightDirection = mb.subtract_vectors(light.position, intercept.point)
                        shadowDirection = mb.normalize(lightDirection)

                    shadowIntersect = self.rtCastRay(intercept.point, shadowDirection, intercept.obj)

                    if shadowIntersect is None:
                        specColor = light.getSpecularColor(intercept, self.cameraPosition)
                        specularLightColor = [specularLightColor[i] + specColor[i] for i in range(3)]

            if not lights.totalInternalReflection(intercept.normal, rayDirection, 1.0, material.ior):
                refract = lights.refract(intercept.normal, rayDirection, 1.0, material.ior)
                refractOrig = mb.subtract_vectors(intercept.point, bias) if outside else mb.add_vectors(intercept.point, bias)
                refractIntercept = self.rtCastRay(refractOrig, refract, None, recursion + 1)
                refractColor = self.rtRayColor(refractIntercept, refract, recursion + 1)

                kr, kt = lights.fresnel(intercept.normal, rayDirection, 1.0, intercept.obj.material.ior)
                reflectColor = mb.multiply_ve(reflectColor, kr)
                refractColor = mb.multiply_ve(refractColor, kt)


        lightColor = [ambientLightColor[i] + diffuseLightColor[i] + specularLightColor[i] + reflectColor[i] + refractColor[i]
                            for i in range(3)]
        finalColor = [surfaceColor[i] * lightColor[i] for i in range(3)]
        finalColor = [min(1, i) for i in finalColor]

        return finalColor

    def rtRender(self):
        for x in range(self.vpX, self.vpX + self.vpWidth + 1):
            for y in range(self.vpY, self.vpY + self.vpHeight + 1):
                if (0 <= x < self.width) and (0 <= y < self.height):
                    pX = 2 * ((x + 0.5 - self.vpX) / self.vpWidth) - 1
                    pY = 2 * ((y + 0.5 - self.vpY) / self.vpHeight) - 1

                    pX *= self.rightEdge
                    pY *= self.topEdge

                    direction = (pX, pY, -self.nearPlane)
                    direction = mb.normalize(direction)

                    intercept = self.rtCastRay(self.cameraPosition, direction)
                    
                    rayColor = self.rtRayColor(intercept, direction)
                        

                    self.rtPoint(x, y, rayColor)
                    pygame.display.flip()