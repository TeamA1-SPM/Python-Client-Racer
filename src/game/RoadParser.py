import pygame

from src.constants.Car import Car
from src.constants.SpriteName import SpriteName
from src.helper.Segment import Segment
import json

dark_grass = pygame.Color(0, 154, 0)
light_grass = pygame.Color(16, 200, 16)
white_rumble = pygame.Color(255, 255, 255)
black_rumble = pygame.Color(0, 0, 0)
dark_road = pygame.Color(105, 105, 105)
light_road = pygame.Color(107, 107, 107)
start_line = pygame.Color(255, 255, 255)


# Initialisiert den RoadParser mit einem Sprites-Loader und leeren Listen für Straßensegmente und Autos
class RoadParser:
    def __init__(self, sprites_loader):
        self.sprites_loader = sprites_loader
        self.segment_list = []
        self.car_list = []

    # Diese Funktion bestimmt den Dateinamen der Strecke basierend auf der Streckennummer
    def get_track(self, number):
        file_name = {
            2: "track02.json",
            3: "track03.json",
            4: "track04.json",
            5: "track05.json",
            6: "track06.json",
            7: "track07.json",
            8: "track08.json",
            9: "track09.json",
            10: "track10.json"
        }.get(number, "track01.json")

        # Ruft die `parse`-Funktion auf und gibt die analysierten Streckendaten zurück
        return self.parse(file_name)

    # Analysiert die Streckendaten aus einer JSON-Datei und erstellt entsprechende Segment- und Autolisten
    def parse(self, file_name):
        self.segment_list = []
        try:
            # Liest die Streckendaten aus der JSON-Datei
            with open(f"./tracks/{file_name}", 'r') as file:
                data = json.load(file)

                # Iteriert über jedes JSON-Segment und erstellt entsprechende Segment-Objekte
                for i, json_segment in enumerate(data):
                    segment = Segment(i)

                    # Setzt die Weltkoordinaten von Punkt1 und Punkt2 des Segments
                    p1 = json_segment["p1"]
                    segment.p1world.y = float(p1[0])
                    segment.p1world.z = float(p1[1])

                    p2 = json_segment["p2"]
                    segment.p2world.y = float(p2[0])
                    segment.p2world.z = float(p2[1])

                    # Setzt die Krümmung des Segments
                    curve = float(json_segment["curve"])
                    segment.curve = curve

                    # Fügt Straßenseiten-Sprites zum Segment hinzu
                    for json_sprite in json_segment["roadside"]:
                        # name = self.get_sprite_name(json_sprite["sprite"])
                        name = json_sprite["sprite"]
                        offset = float(json_sprite["offset"])
                        segment.addRoadsideObj(name, offset, self.sprites_loader.get_sprite_width(name))

                    # Fügt Autos zum Segment hinzu
                    for json_car in json_segment["cars"]:
                        name = json_car["sprite"]

                        offset = float(json_car["offset"])
                        position = float(json_car["position"])
                        speed = float(json_car["speed"])
                        width = self.sprites_loader.get_sprite_width(name)

                        car = Car(name, offset, position, speed, width)
                        self.car_list.append(car)

                    # Ändert die Farben alle 3 Linien und setzt Lane-Informationen
                    segment.grass_color = light_grass if (i // 3) % 2 else dark_grass
                    segment.rumble_color = white_rumble if (i // 3) % 2 else black_rumble
                    segment.road_color = light_road if (i // 3) % 2 else dark_road
                    segment.isLane = True if (i // 3) % 2 else False
                    segment.road_color = start_line if (6 <= i <= 7) % 2 else segment.road_color

                    # Fügt das Segment zur Liste hinzu
                    self.segment_list.append(segment)

        # Gibt einen Fehler aus, wenn ein Problem beim Parsen auftritt
        except Exception as e:
            print(e)

        # Gibt die Liste der Straßensegmente zurück
        return self.segment_list

    # Mappung von JSON-Sprite-Namen zu internen Sprite-Namen
    def get_sprite_name(self, name):
        sprite_dict = {
            "BILLBOARD01": SpriteName.BILLBOARD01,
            "BILLBOARD02": SpriteName.BILLBOARD02,
            "BILLBOARD03": SpriteName.BILLBOARD03,
            "BILLBOARD04": SpriteName.BILLBOARD04,
            "BILLBOARD05": SpriteName.BILLBOARD05,
            "BILLBOARD06": SpriteName.BILLBOARD06,
            "BILLBOARD07": SpriteName.BILLBOARD07,
            "BILLBOARD08": SpriteName.BILLBOARD08,
            "BILLBOARD09": SpriteName.BILLBOARD09,
            "PALM_TREE": SpriteName.PALM_TREE,
            "TREE1": SpriteName.TREE1,
            "TREE2": SpriteName.TREE2,
            "DEAD_TREE1": SpriteName.DEAD_TREE1,
            "DEAD_TREE2": SpriteName.DEAD_TREE2,
            "BUSH1": SpriteName.BUSH1,
            "BUSH2": SpriteName.BUSH2,
            "CACTUS": SpriteName.CACTUS,
            "STUMP": SpriteName.STUMP,
            "BOULDER1": SpriteName.BOULDER1,
            "BOULDER2": SpriteName.BOULDER2,
            "BOULDER3": SpriteName.BOULDER3,
            "COLUMN": SpriteName.COLUMN,
            "SEMI": SpriteName.SEMI,
            "TRUCK": SpriteName.TRUCK,
            "CAR01": SpriteName.CAR01,
            "CAR02": SpriteName.CAR02,
            "CAR03": SpriteName.CAR03,
            "CAR04": SpriteName.CAR04,
        }
        # Gibt den entsprechenden internen Sprite-Namen zurück
        return sprite_dict.get(name, SpriteName.PLAYER_STRAIGHT)
