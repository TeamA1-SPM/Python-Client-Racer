from src.constants import GameMode


# Initialisiert die Spielsetup-Parameter, einschließlich Spielmodus, Streckennummer, Rundenanzahl und Spielername
class GameSetup:
    def __init__(self, mode, track_nr, laps, player_name):
        self.mode = mode
        self.track_nr = track_nr
        self.laps = laps
        self.player_name = player_name
        self.enemy_name = None
        self.player_number = None

    # Gibt die Startposition des Spielers basierend auf dem Spielmodus und der Spielerzahl zurück
    def get_start_position(self):
        if self.mode == GameMode.MULTI_PLAYER:
            if self.player_number == "player1":
                return -0.5
            elif self.player_number == "player2":
                return 0.5
        return 0

    # Setzt die Parameter für Mehrspielermodus, einschließlich des gegnerischen Namens und der Spielerzahl
    def set_multiplayer_parameters(self, enemy_name, player_number):
        self.enemy_name = enemy_name
        self.player_number = player_number
