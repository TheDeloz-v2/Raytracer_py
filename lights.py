import mathbuddy as mb

class Light:
    def __init__(self, intensity=1, color=(1, 1, 1), lightType="Light"):
        self.intensity = intensity
        self.color = color
        self.type = lightType

    def getColor(self):
        return [self.color[0] * self.intensity,
                self.color[1] * self.intensity,
                self.color[2] * self.intensity]

    def getDiffuseColor(self, intercept):
        return None

    def getSpecularColor(self, intercept, viewPosition):
        return None


class Ambient(Light):
    def __init__(self, intensity=1, color=(1, 1, 1)):
        super().__init__(intensity, color, "Ambient")


def reflect(normal, direction):
    dot = mb.dot_product(normal, direction)
    scaled = mb.multiply_ve(normal, dot)
    reflectValue = mb.multiply_ve(scaled, 2)
    reflectValue = mb.subtract_vectors(reflectValue, direction)
    return mb.normalize(reflectValue)


class Directional(Light):
    def __init__(self, direction=(0, 1, 0), intensity=1, color=(1, 1, 1)):
        super().__init__(intensity, color, "Directional")
        self.direction =  mb.normalize(direction)

    def getDiffuseColor(self, intercept):
        direction = [i * -1 for i in self.direction]

        intensity = mb.dot_product(intercept.normal, direction) * self.intensity
        intensity = max(0, min(1, intensity))
        intensity *= 1 - intercept.obj.material.ks

        return [i * intensity for i in self.color]

    def getSpecularColor(self, intercept, viewPosition):
        direction = [i * -1 for i in self.direction]

        reflectDirection = reflect(intercept.normal, direction)

        viewDirection = mb.subtract_vectors(viewPosition, intercept.point)
        viewDirection =  mb.normalize(viewDirection)

        intensity = max(0, min(1, mb.dot_product(reflectDirection, viewDirection))) ** intercept.obj.material.spec
        intensity *= self.intensity
        intensity *= intercept.obj.material.ks

        return [i * intensity for i in self.color]


class Point(Light):
    def __init__(self, position=(0, 0, 0), intensity=1, color=(1, 1, 1)):
        super().__init__(intensity, color, "Point")
        self.position = position

    def getDiffuseColor(self, intercept):
        direction = mb.subtract_vectors(self.position, intercept.point)
        radius =  mb.normalize(direction)
        direction = direction / radius

        intensity = mb.dot_product(intercept.normal, direction) * self.intensity
        intensity *= 1 - intercept.obj.material.ks

        if radius != 0:
            intensity /= radius ** 2
        intensity = max(0, min(1, intensity))

        return [i * intensity for i in self.color]

    def getSpecularColor(self, intercept, viewPosition):
        direction = mb.subtract_vectors(self.position, intercept.point)
        radius = mb.normalize(direction)
        direction = direction / radius

        reflectDirection = reflect(intercept.normal, direction)

        viewDirection = mb.subtract_vectors(viewPosition, intercept.point)
        viewDirection =  mb.normalize(viewDirection)

        intensity = max(0, min(1, mb.dot_product(reflectDirection, viewDirection))) ** intercept.obj.material.spec
        intensity *= self.intensity
        intensity *= intercept.obj.material.ks

        if radius != 0:
            intensity /= radius ** 2
        intensity = max(0, min(1, intensity))

        return [i * intensity for i in self.color]