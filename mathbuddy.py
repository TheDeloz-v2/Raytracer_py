# Libreria Matematica

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