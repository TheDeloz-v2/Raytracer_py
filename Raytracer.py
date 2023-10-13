import pygame
from pygame.locals import *

from figures import *
from lights import *
from rt import Raytracer
from materials import *

width = 650
height = 650

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

rayTracer = Raytracer(screen)
rayTracer.envMap = pygame.image.load('textures/space.bmp')
rayTracer.rtClearColor(56/255, 75/255, 116/255)
rayTracer.rtColor(1, 1, 1)

rayTracer.scene.append(
    Cube(position=(-1.5, -0.75, -5), size=(1.5, 1.5, 1.5), material=cube())
)
rayTracer.scene.append(
    Cube(position=(1.5, -0.75, -5), size=(1.5, 1.5, 1.5), material=cube())
)
rayTracer.scene.append(
    Sphere(position=(0, 1.5, -10), radius=1.5, material=robot())
)
rayTracer.scene.append(
    Disk(position=(0, 0.5, -11.9), normal=(0, 0, 1), radius=1.5, material=mirror())
)
rayTracer.scene.append(
    Disk(position=(-2, 0.5, -5), normal=(1, 0, 0.2), radius=1, material=mirror())
)
rayTracer.scene.append(
    Disk(position=(2, 0.5, -5), normal=(1, 0, -0.2), radius=1, material=mirror())
)
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
pygame.image.save(sub, "outputs/output2.png")

pygame.quit()