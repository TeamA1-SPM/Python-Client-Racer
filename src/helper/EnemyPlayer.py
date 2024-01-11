
# Initialisiert einen EnemyPlayer mit dem gegebenen Namen und Standardwerten für Position und Steuerung
class EnemyPlayer:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.playerX = 0
        self.steer = 0
        self.upDown = 0

    # Setzt die Position des EnemyPlayers basierend auf dem übergebenen Wert
    def set_position(self, value):
        self.position = self.object_to_float(value)

    # Setzt die X-Position des EnemyPlayers basierend auf dem übergebenen Wert
    def set_player_x(self, value):
        self.playerX = self.object_to_float(value)

    # Setzt die Lenkung des EnemyPlayers basierend auf dem übergebenen Wert
    def set_steer(self, value):
        self.steer = self.object_to_float(value)

    # Setzt die Auf- und Abbewegung des EnemyPlayers basierend auf dem übergebenen Wert
    def set_up_down(self, value):
        self.upDown = self.object_to_float(value)

    # Gibt den Sprite-Namen für die aktuelle Steuerung des EnemyPlayers zurück
    def get_sprite_name(self):
        if self.steer < 0:
            if self.upDown > 0:
                return "PLAYER_UPHILL_LEFT"
            return "PLAYER_LEFT"
        elif self.steer > 0:
            if self.upDown > 0:
                return "PLAYER_UPHILL_RIGHT"
            return "PLAYER_RIGHT"

        if self.upDown > 0:
            return "PLAYER_UPHILL_STRAIGHT"

        return "PLAYER_STRAIGHT"

    # Konvertiert den übergebenen Wert in einen float-Wert, falls möglich, andernfalls wird 0.0 zurückgegeben
    def object_to_float(self, value):
        if not isinstance(value, (int, float)):
            return 0.0
        else:
            return float(value)
