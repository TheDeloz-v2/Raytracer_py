import pygame
from pygame.locals import *

from figures import *
from lights import *
from rt import Raytracer
from materials import *

width = 350
height = 350

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

rayTracer = Raytracer(screen)
# rayTracer.envMap = pygame.image.load('textures/kanto.png')
rayTracer.rtClearColor(1, 1, 1)
rayTracer.rtColor(1, 1, 1)


# Pared trasera
rayTracer.scene.append(
    Plane(position=(0, 0, -12), normal=(0, 0, -1), material=wall2())
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
    Plane(position=(0, 3, 0), normal=(0, -1, 0), material=floor())
)

# Figuras
rayTracer.scene.append(
    Pyramid(position=(-2, -1.2, -5), width=0.5, height=0.5, lenght=0.5, material=diamond())
)

rayTracer.scene.append(
    Pyramid(position=(-0.5, -1.2, -5), width=1, height=1, lenght=1, material=gold())
)

rayTracer.scene.append(
    Pyramid(position=(1.5, -1.2, -5), width=1.5, height=1.5, lenght=1.5, material=moon())
)

rayTracer.scene.append(
    Cylinder(position=(-2, 0, -7), radius=0.5, height=0.5, material=glass())
)

rayTracer.scene.append(
    Cylinder(position=(-0.5, 0.5, -7), radius=0.5, height=1, material=gold())
)

rayTracer.scene.append(
    Cylinder(position=(1.5, 1, -7), radius=0.5, height=1.5, material=white())
)







# Lights
rayTracer.lights.append(
    Ambient(intensity=0.5)
)
rayTracer.lights.append(
    Directional(direction=(-1, -2.5, -1), intensity=0.6)
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
pygame.image.save(sub, "outputs/output4.png")

pygame.quit()