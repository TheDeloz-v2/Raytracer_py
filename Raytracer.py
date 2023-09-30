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

# REFLECTIVE 1
rayTracer.scene.append(
    Sphere(position=(-2, 1, -5), radius=0.6, material=mirror())
)

# OPAQUE 1
rayTracer.scene.append(
    Sphere(position=(0, 1, -5), radius=0.6, material=moon())
)

# TRANSAPARENT 1
rayTracer.scene.append(
    Sphere(position=(2, 1, -5), radius=0.6, material=glass())
)

# REFLECTIVE 2
rayTracer.scene.append(
    Sphere(position=(-2, -1, -5), radius=0.6, material=gold())
)

# OPAQUE 2
rayTracer.scene.append(
    Sphere(position=(0, -1, -5), radius=0.6, material=water())
)

# TRANSAPARENT 2
rayTracer.scene.append(
    Sphere(position=(2, -1, -5), radius=0.6, material=diamond())
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

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

rect = pygame.Rect(0, 0, width, height)
sub = screen.subsurface(rect)
pygame.image.save(sub, "outputs/output.png")

pygame.quit()