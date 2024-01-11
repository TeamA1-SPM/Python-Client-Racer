import math

# Settings die in den einzelnen Klassen verwendet werden
# Die Datei dient dazu Variablen die in verschiedenen Klassen immer wieder gebraucht werden in einer Datei zu speichern

# Fenster
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
STEP = 1 / 60

# Einstellungen für das Spiel
FPS = 60.0
STEP = 1/FPS

# Kamera Einstellungen
FOV = 100
DRAW_DISTANCE = 300
CAMERA_HEIGHT = 1000
CAMERA_DEPTH = 1 / (math.tan((FOV / 2) * math.pi / 180))
PLAYER_Z = CAMERA_HEIGHT * CAMERA_DEPTH

# Strecken Einstellungen
ROAD_WIDTH = 2000
SEGMENT_LENGTH = 200
RUMBLE_LENGTH = 3
LANES = 3
SPRITE_SCALE = 0.3 / 80

# Spieler Einstellungen
MAX_SPEED = SEGMENT_LENGTH / STEP
CENTRIFUGAL = 0.3
ACCEL = MAX_SPEED / 5
BREAKING = -MAX_SPEED
DECEL = -MAX_SPEED / 5
OFF_ROAD_DECEL = -MAX_SPEED / 2
OFF_ROAD_LIMIT = MAX_SPEED / 4
PLAYERX_LIMIT = 2
PLAYER_W = 80 * SPRITE_SCALE
