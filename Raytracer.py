import pygame
from pygame.locals import *

from figures import *
from lights import *
from rt import Raytracer
from materials import *

width = 450
height = 450

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

rayTracer = Raytracer(screen)
rayTracer.envMap = pygame.image.load('textures/space.bmp')
rayTracer.rtClearColor(56/255, 75/255, 116/255)
rayTracer.rtColor(1, 1, 1)


# Pared trasera
rayTracer.scene.append(
    Plane(position=(0, 0, -12), normal=(0, 0, -1), material=wall2())
)
# Pared frontal
rayTracer.scene.append(
    Plane(position=(0, 0, 6), normal=(0, 0, 1), material=wall2())
)
# Pared izquierda
rayTracer.scene.append(
    Plane(position=(-3, 0, 0), normal=(1, 0, 0), material=wall())
)
# Pared derecha
rayTracer.scene.append(
    Plane(position=(3, 0, 0), normal=(-1, 0, 0), material=wall())
)
# Suelo
rayTracer.scene.append(
    Plane(position=(0, -1.5, 0), normal=(0, 1, 0), material=floor())
)
# Techo
rayTracer.scene.append(
    Plane(position=(0, 3, 0), normal=(0, -1, 0), material=brilliant_black())
)

# position, radius, height, material)
rayTracer.scene.append(
    Cylinder(position=(0, 0.2, -5), radius=1, height=1, material=moon())
)


# Lights
rayTracer.lights.append(
    Ambient(intensity=0.7)
)
rayTracer.lights.append(
    Directional(direction=(-1, -1.5, -2), intensity=0.3)
)
rayTracer.lights.append(
    Point(position=(0, 0, -4.5), intensity=1, color=(0.2, 0.2, 0.2))
)

rayTracer.rtClear()
rayTracer.rtRender()
"""
isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
"""
rect = pygame.Rect(0, 0, width, height)
sub = screen.subsurface(rect)
pygame.image.save(sub, "outputs/output3.png")

pygame.quit()