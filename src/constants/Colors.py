import pygame


# Farben, für die Darstellung der Gegenstände im Spiel wie z.B. Straßen Segmente etc ...
class Colors:
    # Farben für die Strecke
    START = pygame.Color(255, 255, 255)
    FINISH = pygame.Color(0, 0, 0)
    LANE = pygame.Color(204, 204, 204)
    FOG = pygame.Color(0, 81, 8)
    ROAD_LIGHT = pygame.Color(107, 107, 107)
    ROAD_DARK = pygame.Color(105, 105, 105)
    GRASS_LIGHT = pygame.Color(16, 170, 16)
    GRASS_DARK = pygame.Color(0, 154, 0)
    RUMBLE_LIGHT = pygame.Color(85, 85, 85)
    RUMBLE_DARK = pygame.Color(187, 187, 187)

    # Farben für die Anzeige
    HUD_BACKGROUND = pygame.Color(150, 0, 0, 100)
    HUD_GREY = pygame.Color(255, 255, 255, 150)
    HUD_YELLOW = pygame.Color(255, 200, 0, 150)
    HUD_FRAME = pygame.Color(0, 0, 0)
    HUD_FONT = pygame.Color(0, 0, 0)
    HUD_RED = pygame.Color(255, 0, 0)
    HUD_GREEN = pygame.Color(0, 255, 0)
