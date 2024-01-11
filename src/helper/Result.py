class Result:

    # Initialisiert ein Result-Objekt mit dem übergebenen Spielernamen und Standardwerten für die besten Zeiten
    def __init__(self, playerName):
        self.playerName = playerName
        self.playerBestTime = 0
        self.playerWon = None
        self.enemyName = ""
        self.enemyBestTime = 0

    # Setzt die beste Zeit des Spielers basierend auf dem übergebenen Wert
    def set_Player_Best_Time(self, time):
        self.playerBestTime = self.object_to_float(time)

    # Setzt die beste Zeit des Gegners basierend auf dem übergebenen Wert
    def set_Enemy_Best_Time(self, time):
        self.enemyBestTime = self.object_to_float(time)

    # Konvertiert den übergebenen Wert in einen float-Wert, falls möglich, andernfalls wird 0.0 zurückgegeben
    def object_to_float(self, value):
        if not isinstance(value, (int, float)):
            return 0.0
        else:
            return float(value)