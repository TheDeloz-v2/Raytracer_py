class Material:
    def __init__(self, diffuse=(1, 1, 1), spec=1.0, ks=0.0):
        self.diffuse = diffuse
        self.spec = spec
        self.ks = ks
        
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
