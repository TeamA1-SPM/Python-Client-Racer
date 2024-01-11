import pygame
from pygame.locals import *
from src.constants import SpriteName
from src.constants import Settings


# Initialisiert den SpriteLoader mit einer Fensteroberfläche, einem Taktgeber und Ladeinformationen für Sprites
class SpriteLoader:

    def __init__(self, window_surface):
        pygame.init()
        self.window_surface = window_surface
        self.clock = pygame.time.Clock()

        # Initialisiert den SpriteLoader mit einer Fensteroberfläche, einem Taktgeber und Ladeinformationen für Sprites
        self.sprites_map = {}
        self.path = "../src/images/allSprites.png"
        self.image = None
        self.image_icon = None

        # Fügt die Koordinaten der Sprites zum Dictionary hinzu
        self.add_coordinates()
        # Lädt die Bild-Map
        self.load_image(self.path)

    # Fügt die Koordinaten der Sprites zum Dictionary hinzu: Name -> (x, y, width, height)
    def add_coordinates(self):
        # x, y , weight, height
        self.sprites_map = {
            "BILLBOARD01": (625, 375, 300, 170),
            "BILLBOARD02": (245, 1262, 215, 220),
            "BILLBOARD03": (5, 1262, 230, 220),
            "BILLBOARD04": (1205, 310, 268, 170),
            "BILLBOARD05": (5, 897, 298, 190),
            "BILLBOARD06": (488, 555, 298, 190),
            "BILLBOARD07": (313, 897, 298, 190),
            "BILLBOARD08": (230, 5, 385, 265),
            "BILLBOARD09": (150, 555, 328, 282),

            "PALM_TREE": (5, 5, 215, 540),
            "TREE1": (625, 5, 360, 360),
            "TREE2": (1205, 5, 282, 295),
            "DEAD_TREE1": (5, 555, 135, 332),
            "DEAD_TREE2": (1205, 490, 150, 260),
            "BUSH1": (5, 1097, 240, 155),
            "BUSH2": (255, 1097, 232, 152),
            "CACTUS": (929, 897, 235, 118),
            "STUMP": (995, 330, 195, 140),
            "BOULDER1": (1205, 760, 168, 248),
            "BOULDER2": (621, 897, 298, 140),
            "BOULDER3": (230, 280, 320, 220),
            "COLUMN": (995, 5, 200, 315),

            "SEMI": (1365, 490, 122, 144),
            "TRUCK": (1365, 644, 100, 78),
            "CAR01": (1205, 1018, 80, 56),
            "CAR02": (1383, 825, 80, 59),
            "CAR03": (1383, 760, 88, 55),
            "CAR04": (1383, 894, 80, 57),

            "PLAYER_UPHILL_LEFT": (1383, 961, 80, 45),
            "PLAYER_UPHILL_STRAIGHT": (1295, 1018, 80, 45),
            "PLAYER_UPHILL_RIGHT": (1385, 1018, 80, 45),
            "PLAYER_LEFT": (995, 480, 80, 41),
            "PLAYER_STRAIGHT": (1085, 480, 80, 41),
            "PLAYER_RIGHT": (995, 531, 80, 41),

            "COUNTDOWN_ONE": (1212, 1370, 77, 106),
            "COUNTDOWN_TWO": (1291, 1370, 92, 106),
            "COUNTDOWN_THREE": (1382, 1370, 96, 106),

            "PAUSE_MENU": (1088, 1372, 106, 104),
            "RESULT": (944, 1372, 112, 25),
            "PRESS_ENTER": (919, 1425, 157, 25),
            "WAITING": (747, 1440, 107, 37),
            "WIN": (744, 1373, 138, 25),
            "LOSE": (744, 1402, 157, 25)
        }

    # Lädt die Bild-Map und konvertiert sie ins Alpha-Format
    def load_image(self, path):
        self.image_icon = pygame.image.load(path).convert_alpha()
        # self.image = pygame.transform.scale(image_icon, (50, 50))

    # Gibt die Breite des Sprites basierend auf dem Dictionary zurück
    def get_sprite_width(self, name):

        return self.sprites_map[name][2] * Settings.SPRITE_SCALE

    # Rendert ein Sprite auf der Fensteroberfläche mit angegebener Skalierung und Position
    def render(self, window_Surface, name, scale, dest_x, dest_y, offset_x, offset_y, clip_y):

        if name is None:
            return

        width_mid = Settings.WINDOW_WIDTH / 2.0
        sC = self.sprites_map[name]

        dest_w = (sC[2] * scale * width_mid) * (Settings.SPRITE_SCALE * Settings.ROAD_WIDTH)
        dest_h = (sC[3] * scale * width_mid) * (Settings.SPRITE_SCALE * Settings.ROAD_WIDTH)

        dest_x = dest_x + (dest_w * offset_x)
        dest_y = dest_y + (dest_h * offset_y)

        clip_h = 0
        if clip_y != 0:
            clip_h = dest_y + dest_h - clip_y

        if clip_h < dest_h:
            x = sC[0]
            y = sC[1]
            w = sC[2]
            h = sC[3]
            h -= h * clip_h / dest_h
            image = (self.image_icon.subsurface(x, y, w, h))
            image = pygame.transform.scale(image, (dest_w, dest_h - clip_h)).convert_alpha()
            window_Surface.blit(image, (dest_x, dest_y))
