import pygame
from pygame.locals import *

from figures import *
from lights import *
from rt import Raytracer
from materials import *

width = 700
height = 700

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

rayTracer = Raytracer(screen)
rayTracer.envMap = pygame.image.load('textures/fondoresized.png')
rayTracer.rtClearColor(30/255, 30/255, 30/255)
rayTracer.rtColor(1, 1, 1)


# Mesa
rayTracer.scene.append(
    Cube(position=(0, -2.2, -6), size=(7.3, 0.2, 4), material=white())
)

rayTracer.scene.append(
    Cube(position=(0, -2.1, -5.8), size=(6.5, 0.1, 3.3), material=table())
)

# Bulbassaur
rayTracer.scene.append(
    Cylinder(position=(-1.7, -1.95, -5), radius=0.6, height=0.3, material=metal()) # Figura extra
)

rayTracer.scene.append(
    Sphere(position=(-1.7, -1.45, -5), radius=0.4, material=pokeball())
)

rayTracer.scene.append(
    Sphere(position=(-2, -1.8, -4.5), radius=0.07, material=mirror())
)

rayTracer.scene.append(
    Sphere(position=(-1.4, -1.8, -4.5), radius=0.07, material=mirror())
)

rayTracer.scene.append(
    Cube(position=(-1.7, -1.8, -4.4), size=(0.35, 0.12, 0.05), material=esmerald()) # Transparente
)

# Charmander
rayTracer.scene.append(
    Cylinder(position=(0, -1.95, -5), radius=0.6, height=0.3, material=metal()) # Figura extra
)

rayTracer.scene.append(
    Sphere(position=(0, -1.45, -5), radius=0.4, material=pokeball())
)

rayTracer.scene.append(
    Sphere(position=(-0.3, -1.8, -4.5), radius=0.07, material=mirror())
)

rayTracer.scene.append(
    Sphere(position=(0.3, -1.8, -4.5), radius=0.07, material=mirror())
)

rayTracer.scene.append(
    Cube(position=(0, -1.8, -4.4), size=(0.35, 0.12, 0.05), material=ruby()) # Transparente
)

# Squirtle
rayTracer.scene.append(
    Cylinder(position=(1.7, -1.95, -5), radius=0.6, height=0.3, material=metal()) # Figura extra
)

rayTracer.scene.append(
    Sphere(position=(1.7, -1.45, -5), radius=0.4, material=pokeball())
)

rayTracer.scene.append(
    Sphere(position=(1.4, -1.8, -4.5), radius=0.07, material=mirror())
)

rayTracer.scene.append(
    Sphere(position=(2, -1.8, -4.5), radius=0.07, material=mirror())
)

rayTracer.scene.append(
    Cube(position=(1.7, -1.8, -4.4), size=(0.35, 0.12, 0.05), material=sapphire()) # Transparente
)

# Decoraciones
rayTracer.scene.append(
    Pyramid(position=(-0.85, -2.05, -4.4), width=0.25, height=0.25, lenght=0.25, material=gold()) # Figura extra
)

rayTracer.scene.append(
    Pyramid(position=(0.85, -2.05, -4.4), width=0.25, height=0.25, lenght=0.25, material=gold()) # Figura extra
)

# Lights
rayTracer.lights.append(
    Ambient(intensity=0.6)
)

rayTracer.lights.append(
    Directional(direction=(0, -1.5, -1), intensity=0.6)
)

rayTracer.lights.append(
    Point(position=(-1.7, -1.45, -4.45), intensity=1, color=(1, 1, 1))
)

rayTracer.lights.append(
    Point(position=(0, -1.45, -4.45), intensity=1, color=(1, 1, 1))
)

rayTracer.lights.append(
    Point(position=(1.7, -1.45, -4.45), intensity=1, color=(1, 1, 1))
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
pygame.image.save(sub, "outputs/output_proyecto.png")

pygame.quit()