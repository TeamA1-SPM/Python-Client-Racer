import sys

from src.constants import Settings
from src.game import Race
from src.constants import Colors
from src.helper.button import Button
from src.constants import GameMode
import pygame


class HUD:
    def __init__(self, window_Surface, race, gameSetup, result):
        self.font = ("Universal Light", "bold", 14)
        self.hud_width = Settings.WINDOW_WIDTH
        self.hud_height = int(Settings.WINDOW_HEIGHT * 0.12)
        self.window_Surface = window_Surface
        self.padding = 15
        self.elem_height = self.hud_height - 48
        self.race = race
        self.result = result
        self.pausePosition = None
        self.rectButton = pygame.transform.scale(pygame.image.load("images/lobby/rectButton.png"), (280, 60))
        self.gameSetup = None

    # Darstellung des HUD's

    def render(self, g2d, race, speed, sprites_loader, gameSetup):
        self.gameSetup = gameSetup
        self.window_Surface = g2d

        if race.game_state == Race.GameState.RUNNING:
            self.render_stats(race, speed)
        elif race.game_state == Race.GameState.COUNTDOWN:
            self.render_overlay(self.race.countdown, sprites_loader, self.window_Surface)
        elif race.game_state == Race.GameState.RESULT:
            self.render_result(sprites_loader)
        elif race.game_state == Race.GameState.PAUSE:
            self.renderPauseMenu()

    # Darstellung des Countdowns am Anfang des Spiels
    def render_overlay(self, countdown, sprites_loader, window_surface):

        if self.gameSetup.mode == GameMode.MULTI_PLAYER:
            font = self.get_font(20)

            start_x = ((Settings.WINDOW_WIDTH * 1 / 3) - 50)
            start_x2 = (Settings.WINDOW_WIDTH * 2 / 3)
            start_y = ((Settings.WINDOW_HEIGHT / 4))
            player = self.gameSetup.player_name
            enemy = self.gameSetup.enemy_name

            self.draw_rect(0, start_y - 40, Settings.WINDOW_WIDTH, 60, Colors.Colors.HUD_BACKGROUND)
            window_surface.blit(font.render(player, 1, (0, 0, 0)), (start_x, start_y - 20))
            window_surface.blit(font.render(enemy, 1, (0, 0, 0)), (start_x2, start_y - 20))
            window_surface.blit(font.render("VS", 1, (0, 0, 0)), (Settings.WINDOW_WIDTH / 2, start_y - 20))

        if countdown == 3:
            sprites_loader.render(self.window_Surface, "COUNTDOWN_THREE", 0.0005, float(Settings.WINDOW_WIDTH) / 2,
                                  float(Settings.WINDOW_HEIGHT) / 2, -0.5, -0.7, 0)
        elif countdown == 2:
            sprites_loader.render(self.window_Surface, "COUNTDOWN_TWO", 0.0005, float(Settings.WINDOW_WIDTH) / 2,
                                  float(Settings.WINDOW_HEIGHT) / 2, -0.5, -0.7, 0)
        elif countdown == 1:
            sprites_loader.render(self.window_Surface, "COUNTDOWN_ONE", 0.0005, float(Settings.WINDOW_WIDTH) / 2,
                                  float(Settings.WINDOW_HEIGHT) / 2, -0.5, -0.7, 0)

    # Darstellung der Ergebnisanzeige am Ende des Spiels
    def render_result(self, sprites_loader):
        width = 300
        height = 400
        print(self.gameSetup.mode)
        if self.gameSetup.mode == GameMode.MULTI_PLAYER:
            width = 600

        x_start = (Settings.WINDOW_WIDTH - width) // 2
        y_start = (Settings.WINDOW_HEIGHT - height) // 2

        self.draw_rect(x_start, y_start, width, height, Colors.Colors.HUD_BACKGROUND, 160)
        self.draw_rect(x_start + 20, y_start + 65, width - 40, height - 110, Colors.Colors.HUD_GREY, 150)

        # Titel
        sprites_loader.render(self.window_Surface, "RESULT", 0.0005, Settings.WINDOW_WIDTH / 2,
                              Settings.WINDOW_HEIGHT / 2, -0.5, -3.9, 0)

        if self.result.playerWon is None:
            # Wartet darauf das der Gegenspieler das Spiel beendet
            sprites_loader.render(self.window_Surface, "WAITING", 0.0005, Settings.WINDOW_WIDTH / 2,
                                  Settings.WINDOW_HEIGHT / 2, -0.5, -0.5, 0)
        else:
            if self.gameSetup.mode == GameMode.MULTI_PLAYER:

                self.renderPlayerResult(self.gameSetup.player_name, self.result.playerBestTime, Settings.WINDOW_WIDTH // 3,
                                        self.result.playerWon)
                self.renderPlayerResult(self.race.connection.enemyPlayer, self.result.enemyBestTime,
                                        (Settings.WINDOW_WIDTH * 2) // 3,
                                        not self.result.playerWon)


            else:
                self.renderPlayerResult(self.result.playerName, self.result.playerBestTime, Settings.WINDOW_WIDTH // 2,
                                        self.result.playerWon)


            if self.result.playerWon:
                # Zeigt welcher Spieler gewonnen hat

                sprites_loader.render(self.window_Surface, "WIN", 0.0004, Settings.WINDOW_WIDTH / 2,
                                      Settings.WINDOW_HEIGHT / 2, -0.5, 2.5, 0)
            elif not self.result.playerWon:
                # Zeigt welcher Spieler verloren hat
                sprites_loader.render(self.window_Surface, "LOSE", 0.0004, Settings.WINDOW_WIDTH / 2,
                                      Settings.WINDOW_HEIGHT / 2, -0.5, 2.5, 0)

        sprites_loader.render(self.window_Surface, "PRESS_ENTER", 0.0003, Settings.WINDOW_WIDTH / 2,
                              Settings.WINDOW_HEIGHT / 2, -0.5, 5.8, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT
                sys.exit()

        keys = pygame.key.get_pressed()

        if self.race.game_state == Race.GameState.RESULT:
            if keys[pygame.K_RETURN or pygame.K_KP_ENTER]:
                self.race.game_state = Race.GameState.END
                if self.race.game_state == Race.GameMode.MULTI_PLAYER:
                    self.race.connection.leave_lobby()

    # Wird in render_result aufgerufen
    def renderPlayerResult(self, name, bestTime, axis, win):

        fontSize = 28
        font = pygame.font.SysFont("comicsansms", fontSize, bold=True)
        text_surface = font.render(name, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(axis, Settings.WINDOW_HEIGHT // 2 - 70))
        self.window_Surface.blit(text_surface, text_rect)

        bestLapTitle = "best lap:"
        text_surface = font.render(bestLapTitle, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(axis, Settings.WINDOW_HEIGHT // 2 - 10))
        self.window_Surface.blit(text_surface, text_rect)

        if win:
            font_color = (17, 87, 17)
        else:
            font_color = (70, 2, 2)

        if bestTime is not None:
            time_str = self.time_to_string(bestTime)
            text_surface = font.render(time_str, True, font_color)
            text_rect = text_surface.get_rect(center=(axis, Settings.WINDOW_HEIGHT // 2 + 40))
            self.window_Surface.blit(text_surface, text_rect)

    # Darstellung der Rundenzeiten
    def render_stats(self, race, speed):
       # self.window_Surface.font = self.font
        self.draw_background()
        self.draw_time(race.get_current_lap_time())
        self.draw_last_lap(race.get_last_lap_time())
        self.draw_fastest_lap(self.race.best_lap_time)
        self.draw_enemy_lap(self.race.best_enemy_time)
        self.draw_speed(speed)
        self.draw_round(self.race.lap, self.race.max_laps)

    def draw_background(self):
        self.draw_rect(0, 0, self.hud_width, self.hud_height - 20, Colors.Colors.HUD_BACKGROUND)

    def draw_time(self, time):
        self.draw_rect(15, self.padding, 120, self.elem_height, Colors.Colors.HUD_GREY)
        text = f"Time: {self.time_to_string(time)}"
        self.draw_text(20, text)

    def draw_last_lap(self, time):
        self.draw_rect(145, self.padding, 180, self.elem_height, Colors.Colors.HUD_YELLOW)
        text = f"Last Lap: {self.time_to_string(time)}"
        self.draw_text(150, text)

    def draw_fastest_lap(self, time):
        self.draw_rect(335, self.padding, 180, self.elem_height, Colors.Colors.HUD_YELLOW)
        text = f"Fastest Lap: {self.time_to_string(time)}"
        self.draw_text(340, text)

    def draw_enemy_lap(self, time):
        self.draw_rect(525, self.padding, 180, self.elem_height, Colors.Colors.HUD_YELLOW)
        text = f"Enemy Lap: {self.time_to_string(time)}"
        self.draw_text(530, text)

    def draw_speed(self, speed):
        self.draw_rect(715, self.padding, 120, self.elem_height, Colors.Colors.HUD_GREY)
        text = f"MPH: {int(speed / 100)}"
        self.draw_text(725, text)

    def draw_round(self, round, max_rounds):
        self.draw_rect(845, self.padding, 120, self.elem_height, Colors.Colors.HUD_GREY)
        text = f"Round: {round} / {max_rounds}"
        self.draw_text(850, text)

    def time_to_string(self, time):
        result = ""
        minutes = int(time / 60)
        time %= 60
        seconds = int(time)
        time %= 1
        milliseconds = int(time * 1000)

        if minutes > 0:
            result += f"{minutes}."

        return f"{result}{seconds}.{milliseconds}"


    def get_font(self, size, i=1):  # Returns Press-Start-2P in the desired size
        if i == 1:
            return pygame.font.Font("images/lobby/Calibri Bold.ttf", size)
        elif i == 2:
            return pygame.font.Font("images/lobby/font.ttf", size)
        elif i == 3:
            return pygame.font.Font(None, size)

    # Darstellung des Pause-bildschirms
    def renderPauseMenu(self):
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        pause_Text = self.get_font(65).render("PAUSE", True, "Red")
        pause_Rect = pause_Text.get_rect(center=(512, 100))

        self.window_Surface.blit(pause_Text, pause_Rect)

        pause_Resume = Button(self.rectButton, pos=(512, 300), text_input="RESUME", font=self.get_font(40), base_color="Black", hovering_color="Green")
        pause_Resume.changeColor(OPTIONS_MOUSE_POS)
        pause_Resume.update(self.window_Surface)

        pause_Quit = Button(self.rectButton, pos=(512, 500), text_input="Quit", font=self.get_font(40),
                              base_color="Black", hovering_color="Green")

        pause_Quit.changeColor(OPTIONS_MOUSE_POS)
        pause_Quit.update(self.window_Surface)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_Resume.checkForInput(OPTIONS_MOUSE_POS):
                    self.race.game_state = Race.GameState.RUNNING
                elif pause_Quit.checkForInput(OPTIONS_MOUSE_POS):
                    self.race.game_state = Race.GameState.END
                    if self.race.connection is not None:
                        self.race.connection.leave_lobby()




    def draw_rect(self, start_x, start_y, width, height, color, alpha = 200):
        filled_rect = pygame.Surface((width, height), pygame.SRCALPHA)
        filled_rect.fill((color[0], color[1], color[2], alpha))
        self.window_Surface.blit(filled_rect, (start_x, start_y))
        pygame.draw.rect(self.window_Surface, Colors.Colors.HUD_FRAME, (start_x, start_y, width, height), 1)

    def draw_text(self, start_x, text):
        font = pygame.font.Font('freesansbold.ttf', 15)
        text_surface = font.render(text, 1, (0, 0, 0))
        text_rect = text_surface.get_rect(topleft=(start_x, self.hud_height - 60))
        self.window_Surface.blit(text_surface, text_rect)
