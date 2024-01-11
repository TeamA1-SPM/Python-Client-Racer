import pygame, sys

from src.helper.button import Button
from src.helper.user_and_pw import TextInput
from constants import GameMode
from constants.GameState import GameState
from constants.Colors import Colors
from helper.Connection import Connection
from helper.GameSetup import GameSetup
from Game import GameLoop
from src.constants import Settings


class Lobby:
    def __init__(self):
        self.SCREEN = pygame.display.set_mode((980, 760))  # 980, 760
        pygame.init()
        pygame.display.set_caption("Menu")
        self.BG = pygame.transform.scale(pygame.image.load("images/lobby/LobbyBackground.png"),
                                         (Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
        self.server_Status = False
        self.connection = Connection(self)
        self.username = None
        self.gameSetup = GameSetup(GameMode.MULTI_PLAYER, 1, 3, self.username)
        self.rect_x = 0
        self.rect_y = 0
        self.rect_width = 280
        self.rect_height = 35
        self.server = "Server:"
        self.rectButton = pygame.transform.scale(pygame.image.load("images/lobby/rectButton.png"), (280, 60))
        self.rectName = pygame.transform.scale(pygame.image.load("images/lobby/rectButton.png"), (220, 50))
        self.gameState = None
        self.gameMode = None
        self.main_menu()

    def get_font(self, size, i=1):  # Returns Press-Start-2P in the desired size
        if i == 1:
            return pygame.font.Font("images/lobby/Calibri Bold.ttf", size)
        elif i == 2:
            return pygame.font.Font("images/lobby/font.ttf", size)
        elif i == 3:
            return pygame.font.Font(None, size)

    # Kontroll Menü welches die Steuerung anzeigt
    def Controls(self):
        while True:

            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            self.SCREEN.blit(self.BG, (0, 0))
            self.server_status()

            Controls_Text = self.get_font(65).render("CONTROLS", True, "Blue")
            Controls_Rect = Controls_Text.get_rect(center=(512, 110))
            self.SCREEN.blit(Controls_Text, Controls_Rect)

            Controls_Back = Button(self.rectButton, pos=(512, 405),
                                   text_input="BACK", font=self.get_font(40), base_color="Black",
                                   hovering_color="Green")

            arrowKeys = pygame.image.load("images/ArrowKeys.png").convert_alpha()
            self.SCREEN.blit(arrowKeys, (359, 145))

            Controls_Back.changeColor(OPTIONS_MOUSE_POS)
            Controls_Back.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if Controls_Back.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()

            pygame.display.update()

    # Wartebildschirm für den Fall, dass man auf einen zweiten Spieler wartet
    def findLobby(self):
        go = True
        while go:
            REGISTER_MOUSE_POS = pygame.mouse.get_pos()
            self.SCREEN.blit(self.BG, (0, 0))
            FINDLOBBY_TEXT = self.get_font(65).render("Waiting for another Player", True, "Blue")
            FINDLOBBY_RECT = FINDLOBBY_TEXT.get_rect(center=(512, 110))
            self.SCREEN.blit(FINDLOBBY_TEXT, FINDLOBBY_RECT)
            self.server_status()

            BACK_BUTTON = Button(self.rectButton, pos=(512, 330),
                                 text_input="Back", font=self.get_font(40), base_color=(0, 0, 0),
                                 hovering_color="White")

            BACK_BUTTON.changeColor(REGISTER_MOUSE_POS)
            BACK_BUTTON.update(self.SCREEN)

            if self.connection.game_start:
                mode = GameMode.MULTI_PLAYER
                enemyPlayer = self.connection.enemyPlayer
                enemyNumber = self.connection.enemyNumber
                self.gameSetup.set_multiplayer_parameters(enemyPlayer, enemyNumber)
                GameLoop(mode, GameState.READY, self.connection, self.gameSetup)
                go = False
                self.connection.game_start = False


            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.connection.logout()
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if BACK_BUTTON.checkForInput(REGISTER_MOUSE_POS):
                            self.connection.leave_lobby()
                            self.preLobby()

            pygame.display.update()
        self.preLobby()

    # Pre-lobby menü mit, Find lobby-, Logout- und Bestenliste button
    def preLobby(self):
        while True:
            REGISTER_MOUSE_POS = pygame.mouse.get_pos()
            self.SCREEN.blit(self.BG, (0, 0))
            FINDLOBBY_TEXT = self.get_font(65).render("PRE-LOBBY", True, "Blue")
            FINDLOBBY_RECT = FINDLOBBY_TEXT.get_rect(center=(512, 110))
            self.SCREEN.blit(FINDLOBBY_TEXT, FINDLOBBY_RECT)
            self.server_status()

            FINDLOBBY_BUTTON = Button(self.rectButton, pos=(512, 180),
                                      text_input="Find Lobby", font=self.get_font(40), base_color=(0, 0, 0),
                                      hovering_color="White")

            LOGOUT_BUTTON = Button(self.rectButton, pos=(512, 255),
                                   text_input="Logout", font=self.get_font(40), base_color="Black",
                                   hovering_color="White")

            BESTENLISTE_BUTTON = Button(self.rectButton, pos=(512, 330),
                                        text_input="Match History", font=self.get_font(40), base_color=(0, 0, 0),
                                        hovering_color="White")

            for button in [FINDLOBBY_BUTTON, BESTENLISTE_BUTTON, LOGOUT_BUTTON]:
                button.changeColor(REGISTER_MOUSE_POS)
                button.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.connection.logout()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if LOGOUT_BUTTON.checkForInput(REGISTER_MOUSE_POS):
                        self.connection.logout()
                        self.username = None
                        self.login()
                    if FINDLOBBY_BUTTON.checkForInput(REGISTER_MOUSE_POS):
                        self.connection.find_lobby()
                        self.findLobby()
                    if BESTENLISTE_BUTTON.checkForInput(REGISTER_MOUSE_POS):
                        self.bestenliste()
            pygame.display.update()

    def bestenliste(self):

        self.connection.best_track_times(1)
        while True:

            width = 600
            heights = 600

            x_start = (Settings.WINDOW_WIDTH - width) // 2
            y_start = 80

            self.draw_rect(x_start, y_start, width, heights, Colors.HUD_BACKGROUND, 160)
            self.draw_rect(x_start + 20, y_start + 65, width - 40, heights - 110, Colors.HUD_GREY, 150)

            font = self.get_font(30)
            REGISTER_MOUSE_POS = pygame.mouse.get_pos()
            self.SCREEN.blit(self.BG, (0, 0))
            Multiplayer_TEXT = self.get_font(65).render("LEADERBOARD", True, "Blue")
            Multiplayer_RECT = Multiplayer_TEXT.get_rect(center=(512, 60))
            self.SCREEN.blit(Multiplayer_TEXT, Multiplayer_RECT)
            self.server_status()

            BACK_BUTTON = Button(self.rectButton, pos=(512, 720),
                                 text_input="Back", font=self.get_font(40), base_color="Black", hovering_color="White")

            BACK_BUTTON.changeColor(REGISTER_MOUSE_POS)
            BACK_BUTTON.update(self.SCREEN)

            board_data = self.connection.scoreBoard

            names = board_data[::2]
            times = board_data[1::2]

            pos_x = 340
            pos_y = 150

            self.draw_rect(x_start, y_start, width, heights, Colors.HUD_BACKGROUND, 160)
            self.draw_rect(x_start + 20, y_start + 65, width - 40, heights - 110, Colors.HUD_GREY, 150)

            for i, (name, time) in enumerate(zip(names, times)):
                self.SCREEN.blit(font.render(f"{name}:", 1, (0, 0, 0)), (pos_x, pos_y))
                self.SCREEN.blit(font.render(f"{round(time, 3)}", 1, (0, 0, 0)), (pos_x + 200, pos_y))
                pos_y = pos_y + 50

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON.checkForInput(REGISTER_MOUSE_POS):
                        self.preLobby()
            pygame.display.update()

    # Multiplayer-Menü mit den button Login, Register und Back
    def multiplayer(self):
        while True:

            REGISTER_MOUSE_POS = pygame.mouse.get_pos()
            self.SCREEN.blit(self.BG, (0, 0))
            Multiplayer_TEXT = self.get_font(65).render("MULTIPLAYER", True, "Blue")
            Multiplayer_RECT = Multiplayer_TEXT.get_rect(center=(512, 110))
            self.SCREEN.blit(Multiplayer_TEXT, Multiplayer_RECT)
            self.server_status()

            LOGIN_BUTTON = Button(self.rectButton, pos=(512, 180),
                                  text_input="Login", font=self.get_font(40), base_color=(0, 0, 0),
                                  hovering_color="White")

            REGISTER_BUTTON = Button(self.rectButton, pos=(512, 255),
                                     text_input="Register", font=self.get_font(40), base_color=(0, 0, 0),
                                     hovering_color="White")

            BACK_BUTTON = Button(self.rectButton, pos=(512, 330),
                                 text_input="Back", font=self.get_font(40), base_color="Black", hovering_color="White")

            for button in [LOGIN_BUTTON, REGISTER_BUTTON, BACK_BUTTON]:
                button.changeColor(REGISTER_MOUSE_POS)
                button.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if LOGIN_BUTTON.checkForInput(REGISTER_MOUSE_POS):
                        self.login()
                    if REGISTER_BUTTON.checkForInput(REGISTER_MOUSE_POS):
                        self.register()
                    if BACK_BUTTON.checkForInput(REGISTER_MOUSE_POS):
                        self.main_menu()
                        self.gameSetup = None
            pygame.display.update()

    # Login-Menü mit den Textfeldern für das login und den button LOGIN und BACK
    def login(self):
        username = TextInput(x=512, y=150, font=self.get_font(40))
        password = TextInput(x=512, y=220, font=self.get_font(40), pw=True)

        input_boxes = [username, password]
        login_true_false = True

        while login_true_false:
            LOGIN_MOUSE_POS = pygame.mouse.get_pos()
            self.SCREEN.blit(self.BG, (0, 0))
            LOGIN_TEXT = self.get_font(65).render("LOGIN", True, "Blue")
            LOGIN_RECT = LOGIN_TEXT.get_rect(center=(512, 110))
            self.SCREEN.blit(LOGIN_TEXT, LOGIN_RECT)
            self.server_status()

            USERNAME = Button(self.rectName, pos=(392, 175),
                              text_input="Username:", font=self.get_font(40), base_color="Black",
                              hovering_color="Black")

            PASSWORD = Button(self.rectName, pos=(392, 245),
                              text_input="Password:", font=self.get_font(40), base_color="Black",
                              hovering_color="Black")

            PLAY_BUTTON = Button(self.rectButton, pos=(512, 330),
                                 text_input="Login", font=self.get_font(40), base_color=(0, 0, 0),
                                 hovering_color="White")

            OPTIONS_BACK = Button(self.rectButton, pos=(512, 405),
                                  text_input="Back", font=self.get_font(40), base_color="Black", hovering_color="White")

            for button in [PLAY_BUTTON, OPTIONS_BACK, USERNAME, PASSWORD]:
                button.changeColor(LOGIN_MOUSE_POS)
                button.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.connection.logout()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(LOGIN_MOUSE_POS):
                        if not username.active and not password.active:
                            self.connection.login(username.text, password.text)
                    if OPTIONS_BACK.checkForInput(LOGIN_MOUSE_POS):
                        self.connection.logout()
                        self.multiplayer()
                for box in input_boxes:
                    box.handle_event(event)
            for box in input_boxes:
                box.update()
                box.draw(self.SCREEN)
            if self.connection.is_login_successful == 1:
                self.connection.is_login_successful = 0
                self.username = username.text
                self.gameSetup.player_name = self.username
                self.gameSetup = GameSetup(GameMode.MULTI_PLAYER, 1, 1, self.username)
                self.preLobby()
            elif self.connection.is_login_successful == 2:
                REGISTER_TEXT = self.get_font(40).render("The user doesn't exist.", True, "Blue")
                REGISTER_RECT = REGISTER_TEXT.get_rect(center=(512, 292))
                self.SCREEN.blit(REGISTER_TEXT, REGISTER_RECT)

            pygame.display.update()

    # Register-Menü mit den Textfeldern für das registrieren und den button REGISTER und BACK
    def register(self):
        username = TextInput(x=512, y=150, font=self.get_font(40))
        password = TextInput(x=512, y=220, font=self.get_font(40), pw=True)

        input_boxes = [username, password]
        safeUserAndPW = True
        register_true_false = True
        while register_true_false:
            REGISTER_MOUSE_POS = pygame.mouse.get_pos()
            self.SCREEN.blit(self.BG, (0, 0))
            REGISTER_TEXT = self.get_font(65).render("REGISTER", True, "Blue")
            REGISTER_RECT = REGISTER_TEXT.get_rect(center=(490, 110))
            self.SCREEN.blit(REGISTER_TEXT, REGISTER_RECT)
            self.server_status()

            USERNAME = Button(self.rectName, pos=(392, 175),
                              text_input="Username:", font=self.get_font(40), base_color="Black",
                              hovering_color="Black")

            PASSWORD = Button(self.rectName, pos=(392, 245),
                              text_input="Password:", font=self.get_font(40), base_color="Black",
                              hovering_color="Black")

            PLAY_BUTTON = Button(self.rectButton, pos=(512, 330),
                                 text_input="Register", font=self.get_font(40), base_color="Black",
                                 hovering_color="White")

            OPTIONS_BACK = Button(self.rectButton, pos=(512, 405),
                                  text_input="Back", font=self.get_font(40), base_color="Black", hovering_color="White")

            if self.connection.is_register_successful == 1:
                REGISTER_TEXT = self.get_font(40).render("Registration successful!", True, "Blue")
                REGISTER_RECT = REGISTER_TEXT.get_rect(center=(512, 292))
                self.SCREEN.blit(REGISTER_TEXT, REGISTER_RECT)
            elif self.connection.is_register_successful == 2:
                REGISTER_TEXT = self.get_font(40).render("User aleready exists!", True, "Blue")
                REGISTER_RECT = REGISTER_TEXT.get_rect(center=(512, 292))
                self.SCREEN.blit(REGISTER_TEXT, REGISTER_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BACK, USERNAME, PASSWORD]:
                button.changeColor(REGISTER_MOUSE_POS)
                button.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.connection.logout()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(REGISTER_MOUSE_POS):
                        if not username.active and not password.active:
                            print(username.text)
                            print(password.text)
                            self.connection.register(username.text, password.text)
                    if OPTIONS_BACK.checkForInput(REGISTER_MOUSE_POS):
                        self.connection.logout()
                        self.multiplayer()
                for box in input_boxes:
                    box.handle_event(event)
            for box in input_boxes:
                box.update()
                box.draw(self.SCREEN)

            pygame.display.update()

    # Hauptmenü
    def main_menu(self):
        go = True
        while go:
            self.SCREEN.blit(self.BG, (0, 0))

            self.server_status()

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(65).render("MAIN MENU", True, "Blue")
            MENU_RECT = MENU_TEXT.get_rect(center=(512, 110))

            PLAY_BUTTON = Button(self.rectButton, pos=(512, 180),
                                 text_input="Play", font=self.get_font(40), base_color=(0, 0, 0),
                                 hovering_color="White")

            MULTIPLAYER_BUTTON = Button(self.rectButton, pos=(512, 255),
                                        text_input="Multiplayer", font=self.get_font(40), base_color=(0, 0, 0),
                                        hovering_color="White")

            CONTROL_BUTTON = Button(self.rectButton, pos=(512, 330),
                                    text_input="Control", font=self.get_font(40), base_color=(0, 0, 0),
                                    hovering_color="White")

            QUIT_BUTTON = Button(self.rectButton, pos=(512, 405),
                                 text_input="QUIT", font=self.get_font(40), base_color=(0, 0, 0),
                                 hovering_color="White")

            self.SCREEN.blit(MENU_TEXT, MENU_RECT)

            for button in [QUIT_BUTTON, PLAY_BUTTON, MULTIPLAYER_BUTTON, CONTROL_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.gameSetup.mode = GameMode.SINGLE_PLAYER
                        GameLoop(GameMode.SINGLE_PLAYER, GameState.READY, None, self.gameSetup)
                    if MULTIPLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.connection.best_track_times(1)
                        self.multiplayer()
                    if CONTROL_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.Controls()

            pygame.display.update()

    # Abfragen des Serverstatus im Menü
    def server_status(self):

        font = pygame.font.Font("images/lobby/font.ttf", 20)

        if self.server_Status:
            onOff = "ONLINE"
            self.SCREEN.blit(font.render(onOff, 1, Colors.HUD_GREEN), (172, 10))
        else:
            onOff = "OFFLINE"
            self.SCREEN.blit(font.render(onOff, 1, Colors.HUD_RED), (172, 10))

        self.SCREEN.blit(font.render(self.server, 1, Colors.HUD_FONT), (10, 10))

    def draw_rect(self, start_x, start_y, width, height, color, alpha=200):

        filled_rect = pygame.Surface((width, height), pygame.SRCALPHA)
        filled_rect.fill((color[0], color[1], color[2], alpha))
        self.SCREEN.blit(filled_rect, (start_x, start_y))
        pygame.draw.rect(self.SCREEN, Colors.HUD_FRAME, (start_x, start_y, width, height), 1)


if __name__ == "__main__":
    lobby_menu = Lobby()

