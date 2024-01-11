import pygame

from src.constants.Settings import FPS


# Initialisiert die Game Loop-Zeitvariablen
class GameLoopTimer:
    def __init__(self):
        # Game loop Zeit variablen
        self.now = 0
        self.last = 0
        self.time_per_frame = 1000000000.0 / FPS

        self.countdown = 0

    # Überprüft, ob die nächste Aktualisierung des Game Loops bereit ist
    def is_ready(self):
        self.now = pygame.time.get_ticks() * 1000000  # Convert milliseconds to nanoseconds

        if self.now - self.last >= self.time_per_frame:
            if self.countdown >= 0:
                self.countdown -= self.time_per_frame
            self.last = self.now
            return True

        return False

    # Startet einen Countdown mit einer vordefinierten Zeit (in Nanosekunden)
    def start_countdown(self):
        self.countdown = 4000000000.0  # Adjust as needed

    # Gibt den aktuellen Countdown-Wert in Sekunden zurück
    def get_countdown(self):
        return int(self.countdown / 1000000000)
