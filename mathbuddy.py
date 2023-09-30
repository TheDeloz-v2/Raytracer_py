# Libreria Matematica
import math

# Funcion de operacion punto entre dos vectores
def dot_product(v1, v2):
    return sum((a * b) for a, b in zip(v1, v2))

# Funcion de operacion resta entre dos vectores de cualquier dimension
def subtract_vectors(v1, v2):
    return [x - y for x, y in zip(v1, v2)]

# Funcion de operacion normalizacion de un vector
def normalize(v):
    norm = (sum([x * x for x in v]))**0.5
    return [x / norm for x in v]

# Funcion de operacion suma entre dos vectores
def add_vectors(v1, v2):
    return [x + y for x, y in zip(v1, v2)]

# Funcion de operacion multiplicacion entre vector y escalar
def multiply_ve(v, k):
    return [x * k for x in v]

# Funcion de obtencion normal de un vector
def linalg_norm(vec):
    return (sum([x * x for x in vec]))**0.5

# Funcion para convertir una tupla a negativa
def negativeTuple(t):
    return (-t[0],-t[1],-t[2])

# Funcion para obtener la magnitud de un vector
def magVec(v):
    vectorList = list(v)
    return math.sqrt(sum(comp ** 2 for comp in vectorList))

# Funcion de division entre vector y escalar
def vectorDivEsc(v, s):
    result = [x / s for x in v]
    return result