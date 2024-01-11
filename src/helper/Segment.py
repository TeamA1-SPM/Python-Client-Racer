import pygame
from src.constants.RoadSideObject import RoadSideObject
from src.helper.Point import Point

# Initialisiert ein Segment-Objekt mit der übergebenen Indexnummer und leeren Punkten für die Welt-, Kamera- und
# Bildschirmkoordinaten
class Segment:
    def __init__(self, i):
        self.i = i

        self.p1world = Point()
        self.p1camera = Point()
        self.p1screen = Point()

        self.p2world = Point()
        self.p2camera = Point()
        self.p2screen = Point()

        self.curve = 0.0
        self.clip = 0.0
        self.isLooped = False
        self.isLane = False

        # Standardfarben für Gras, Rumble (Straßenrand), Straße und Straßenmarkierung
        self.grass_color: pygame.Color = "black"
        self.rumble_color: pygame.Color = "black"
        self.road_color: pygame.Color = "black"
        self.line_color: pygame.Color = "white"

        # Liste für Objekte am Straßenrand
        self.roadside_list = []

    def addRoadsideObj(self, name, offset, width):
        # Fügt ein Objekt am Straßenrand zur Liste hinzu
        self.roadside_list.append(RoadSideObject(name, offset, width))








