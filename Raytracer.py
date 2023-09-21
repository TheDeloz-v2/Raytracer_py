import pygame
from pygame.locals import *

from figures import *
from lights import *
from rt import Raytracer
from materials import *

width = 400
height = 400

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

rayTracer = Raytracer(screen)
rayTracer.rtClearColor(56/255, 75/255, 116/255)
rayTracer.rtColor(1, 1, 1)

def cuerpo():
  rayTracer.scene.append(
      Sphere(position=(0, -2, -7), radius=1.5, material=snow())
  )

  rayTracer.scene.append(
      Sphere(position=(0, 0.2, -7), radius=1.3, material=snow())
  )

  rayTracer.scene.append(
      Sphere(position=(0, 2.2, -7), radius=1, material=snow())
  )

  rayTracer.scene.append(
      Sphere(position=(0, -1.3, -5.6), radius=0.3, material=coal())
  )

  rayTracer.scene.append(
      Sphere(position=(0, -0.3, -5.8), radius=0.2, material=coal())
  )

  rayTracer.scene.append(
      Sphere(position=(0, 0.7, -5.8), radius=0.2, material=coal())
  )

def boca():
  rayTracer.scene.append(
      Sphere(position=(-0.12, 1.6, -6.2), radius=0.06, material=rock())
  )

  rayTracer.scene.append(
      Sphere(position=(0.12, 1.6, -6.2), radius=0.06, material=rock())
  )

  rayTracer.scene.append(
      Sphere(position=(-0.36, 1.7, -6.2), radius=0.06, material=rock())
  )

  rayTracer.scene.append(
      Sphere(position=(0.36, 1.7, -6.2), radius=0.06, material=rock())
  )

def nariz():
  rayTracer.scene.append(
      Sphere(position=(0, 1.95, -6), radius=0.2, material=carrot())
  )

def ojos():
  rayTracer.scene.append(
      Sphere(position=(-0.2, 2.3, -6.1), radius=0.13, material=white())
  )
  
  rayTracer.scene.append(
      Sphere(position=(-0.2, 2.33, -6), radius=0.06, material=brilliant_black())
  )

  rayTracer.scene.append(
      Sphere(position=(0.2, 2.3, -6.1), radius=0.13, material=white())
  )
  
  rayTracer.scene.append(
      Sphere(position=(0.2, 2.33, -6), radius=0.06, material=brilliant_black())
  )

cuerpo()
boca()
nariz()
ojos()

rayTracer.lights.append(
    Ambient(intensity=0.7)
)
rayTracer.lights.append(
    Directional(direction=(-1, -1.5, -2), intensity=0.3)
)

isRunning = True

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    rayTracer.rtClear()
    rayTracer.rtRender()
    pygame.display.flip()

pygame.quit()