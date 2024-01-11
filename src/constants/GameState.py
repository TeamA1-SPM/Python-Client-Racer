from enum import Enum


# Enum um den Status des Spiels zu zeigen
class GameState(Enum):
    LOADING = "LOADING"
    READY = "READY"
    COUNTDOWN = "COUNTDOWN"
    RUNNING = "RUNNING"
    PAUSE = "PAUSE"
    RESULT = "RESULT"
    END = "END"
