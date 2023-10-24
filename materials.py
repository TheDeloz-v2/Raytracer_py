import pygame

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

class Material:
    def __init__(self, diffuse=(1, 1, 1), spec=1.0, ks=0.0, ior= 1.0,matType=OPAQUE, texture = None):
        self.diffuse = diffuse
        self.spec = spec
        self.ks = ks
        self.ior = ior
        self.matType = matType
        self.texture = texture


# Transparent materials
def glass():
    return Material(diffuse=(0.9, 0.9, 0.9), spec=128, ks=0.20, ior=2.417, matType=TRANSPARENT)

def diamond():
    return Material(diffuse=(0.6, 0.6, 0.9), spec=128, ks=0.20, ior=2.417, matType=TRANSPARENT)

def ruby():
    return Material(diffuse=(0.9, 0.1, 0.1), spec=128, ks=0.20, ior=1.77, matType=TRANSPARENT)

def esmerald():
    return Material(diffuse=(0.1, 0.9, 0.1), spec=128, ks=0.20, ior=1.58, matType=TRANSPARENT)

def sapphire():
    return Material(diffuse=(0.1, 0.1, 0.9), spec=128, ks=0.20, ior=1.77, matType=TRANSPARENT)


# Reflective materials
def mirror():
    return Material(diffuse=(0.9, 0.9, 0.9), spec=64, ks=0.1, matType=REFLECTIVE)

def gold():
    return Material(diffuse=(255/255,215/255,0), spec=128, ks=0.25, matType=REFLECTIVE)

def floor():
    return Material(diffuse=(0.6, 0.6, 0.6), spec=32, ks=0.5, matType=REFLECTIVE)


# Opaque materials
def moon():
    return Material(texture=pygame.image.load("textures/moon.jpg"))
        
def brick():
    return Material(diffuse=(1, 0.3, 0.2), spec=8, ks=0.01)

def grass():
    return Material(diffuse=(0.2, 0.8, 0.2), spec=32, ks=0.1)

def water():
    return Material(diffuse=(0.2, 0.2, 0.8), spec=256, ks=0.5)

def snow():
    return Material(diffuse=(240/255, 228/255, 204/255), spec=2, ks=0.01)

def coal():
    return Material(diffuse=(0.2, 0.2, 0.2), spec=64, ks=0.5)

def rock():
    return Material(diffuse=(101/255, 86/255, 81/255), spec=64, ks=0.5)

def carrot():
    return Material(diffuse=(253/255, 85/255, 53/255), spec=64, ks=0.5)

def white():
    return Material(diffuse=(1, 1, 1), spec=64, ks=0.5)

def brilliant_black():
    return Material(diffuse=(0, 0, 0), spec=256, ks=0.5)

def wall2():
    return Material(diffuse=(0.8, 0.8, 0.8), spec=32, ks=0.2)

def wall():
    return Material(diffuse=(0.7, 0.7, 0.7), spec=32, ks=0.2)

def cube():
    return Material(texture=pygame.image.load("textures/cube.jpg"))

def robot():
    return Material(texture=pygame.image.load("textures/robot.png"))

def pokeball():
    return Material(texture=pygame.image.load("textures/pokeball.jpg"))

def table():
    return Material(diffuse=(95/255, 134/255, 92/255), spec=32, ks=0.2)

def metal():
    return Material(diffuse=(72/255, 77/255, 72/255), spec=64, ks=0.5)