from typing import Optional
from src.constants.GameState import GameState
from src.constants import GameMode
from src.constants import Settings


class Race:

    def __init__(self, max_laps: int, track_length: float, connection, mode, game_state, result):
        self.connection = connection
        self.max_laps = max_laps
        self.track_mid = track_length / 2
        self.game_state = game_state
        self.countdown = 3
        self.current_lap_time = 0
        self.last_lap_time = 0
        self.best_lap_time = 0
        self.best_enemy_time = 0
        self.crossed_checkpoint = False
        self.lap = 1
        self.mode = mode
        self.result = result

    # aktualisiert das Rennen
    def update(self, player_position: float):

        if self.is_lap_finished(player_position):
            self.start_new_lap()

            if self.mode == GameMode.MULTI_PLAYER:
                self.connection.send_lap_time(self.last_lap_time)
            else:
                print(self.last_lap_time)
                if self.best_lap_time == 0 or self.last_lap_time < self.best_lap_time:
                    self.best_lap_time = self.last_lap_time
                    self.result.playerBestTime = self.best_lap_time

        if self.lap > self.max_laps:
            if self.mode == GameMode.MULTI_PLAYER:
                self.connection.send_finished_race()
            self.game_state = GameState.RESULT

        self.current_lap_time += Settings.STEP

    # prüft, eine letzte Runde gefahren wurde
    def is_lap_finished(self, player_position: float) -> bool:
        if self.track_mid < player_position < (self.track_mid + Settings.PLAYER_Z):
            self.crossed_checkpoint = True
        return self.crossed_checkpoint and player_position < Settings.PLAYER_Z

    # startet eine neue Runde sobald der Spieler über die Ziellinie gefahren ist
    def start_new_lap(self):
        self.last_lap_time = self.current_lap_time
        self.current_lap_time = 0
        self.crossed_checkpoint = False
        self.lap += 1


    def setGameState (self, gameState):
        self.game_state = gameState

    @staticmethod
    def get_formatted_time(time: float) -> float:
        time = int(time * 10000)
        return time / 10000

    @staticmethod
    def object_to_double(value) -> float:
        if not isinstance(value, (int, float)):
            return 0.0
        return float(value)

    def get_current_lap_time(self) -> float:
        return self.get_formatted_time(self.current_lap_time)

    def get_last_lap_time(self) -> float:
        return self.get_formatted_time(self.last_lap_time)

    def set_best_lap_time(self, best_lap_time) -> None:
        self.best_lap_time = self.object_to_double(best_lap_time)

    def set_best_enemy_time(self, best_enemy_time) -> None:
        self.best_enemy_time = self.object_to_double(best_enemy_time)

    # setzt den Countdown der am anfang des Spiels gerendert wird
    def set_countdown(self, countdown):

        print(countdown)
        if self.game_state == GameState.COUNTDOWN:
            result = int(self.object_to_double(countdown))
            if result <= 0:
                self.game_state = GameState.RUNNING
            else:
                self.countdown = result