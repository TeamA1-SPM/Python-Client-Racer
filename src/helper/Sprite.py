from src.constants.SpriteName import SpriteName


# Initialisiert ein Sprite-Objekt mit den übergebenen Parametern, einschließlich Name, Offset, Position,
# Geschwindigkeit und Breite
class Sprite:
    def __init__(self, name: SpriteName, offset, position, speed, width):
        self.name = name
        self.offset = offset
        self.position = position
        self.speed = speed
        self.width = width
