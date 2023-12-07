import pygame, sys
import game_window
from button import Button
from user_and_pw import TextInput


def get_font(size, i=1):  # Returns Press-Start-2P in the desired size
    if i == 1:
        return pygame.font.Font("images/lobby/Overthink.ttf", size)
    elif i == 2:
        return pygame.font.Font("images/lobby/font.ttf", size)
    elif i == 3:
        return pygame.font.Font(None, size)


pygame.init()

SCREEN = pygame.display.set_mode((980, 760))  # 980, 760
pygame.display.set_caption("Menu")

BG = pygame.image.load("images/lobby/LobbyBackground.png")
username = TextInput(x=170, y=250, font=get_font(50, 3))
password = TextInput(x=490, y=250, font=get_font(50, 3), pw=True)


input_boxes = [username, password]


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(490, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(490, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()
def findLobby():
    while True:
        REGISTER_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))
        LOGIN_TEXT = get_font(45).render("This is the FINDLOBBY screen.", True, "Black")
        LOGIN_RECT = LOGIN_TEXT.get_rect(center=(490, 160))
        SCREEN.blit(LOGIN_TEXT, LOGIN_RECT)


        FINDLOBBY_BUTTON = Button(image=pygame.image.load("images/lobby/rectButton.png"), pos=(490, 400),
                             text_input="FINDLOBBY", font=get_font(75), base_color=(0, 0, 0), hovering_color="White")

        BESTENLISTE_BUTTON = Button(image=pygame.image.load("images/lobby/rectButton.png"), pos=(490, 550),
                                  text_input="BEST.LIst", font=get_font(75), base_color=(0, 0, 0), hovering_color="White")

        LOGOUT_BUTTON = Button(image=pygame.image.load("images/lobby/rectButton.png"), pos=(490, 700),
                             text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        for button in [FINDLOBBY_BUTTON, BESTENLISTE_BUTTON, LOGOUT_BUTTON]:
            button.changeColor(REGISTER_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LOGOUT_BUTTON.checkForInput(REGISTER_MOUSE_POS):
                    main_menu()
                if FINDLOBBY_BUTTON.checkForInput(REGISTER_MOUSE_POS):
                    game_window.GameLoop.run(game_window.GameLoop())
        pygame.display.update()

def login ():
    safeUserAndPW = True
    while True:
        LOGIN_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))
        LOGIN_TEXT = get_font(45).render("This is the LOGIN screen.", True, "Black")
        LOGIN_RECT = LOGIN_TEXT.get_rect(center=(490, 160))
        SCREEN.blit(LOGIN_TEXT, LOGIN_RECT)


        PLAY_BUTTON = Button(image=pygame.image.load("images/lobby/rectButton.png"), pos=(490, 400),
                             text_input="PLAY", font=get_font(75), base_color=(0, 0, 0), hovering_color="White")

        OPTIONS_BACK = Button(image=pygame.image.load("images/lobby/rectButton.png"), pos=(490, 550),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        for button in [PLAY_BUTTON, OPTIONS_BACK]:
            button.changeColor(LOGIN_MOUSE_POS)
            button.update(SCREEN)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(LOGIN_MOUSE_POS):
                    if username.completeText and password.completeText:
                        print(username.text)
                        print("geben sie erst einen Usernamen und ein Password ein")
                        findLobby()
                        #TODO: Server muss abfragen ob das PW/Benutzer passt
                if OPTIONS_BACK.checkForInput(LOGIN_MOUSE_POS):
                    main_menu()
            for box in input_boxes:
                box.handle_event(event)
        for box in input_boxes:
            if safeUserAndPW:
                if username.completeText and password.completeText:
                    print(box.text)
                    box.visible = False
                    box.active = False
                    # username.Text und password.Text kann ab hier eingespeichert werden.
                else:
                    box.update()
                    box.draw(SCREEN)
        if username.completeText and password.completeText:
            safeUserAndPW = False

        pygame.display.update()
def register():
    safeUserAndPW = True
    while True:
        REGISTER_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))
        LOGIN_TEXT = get_font(45).render("This is the REGISTER screen.", True, "Black")
        LOGIN_RECT = LOGIN_TEXT.get_rect(center=(490, 160))
        SCREEN.blit(LOGIN_TEXT, LOGIN_RECT)


        PLAY_BUTTON = Button(image=pygame.image.load("images/lobby/rectButton.png"), pos=(490, 400),
                             text_input="PLAY", font=get_font(75), base_color=(0, 0, 0), hovering_color="White")

        OPTIONS_BACK = Button(image=pygame.image.load("images/lobby/rectButton.png"), pos=(490, 550),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        for button in [PLAY_BUTTON, OPTIONS_BACK]:
            button.changeColor(REGISTER_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(REGISTER_MOUSE_POS):
                    if username.completeText and password.completeText:
                        print(username.text)
                        print("geben sie erst einen Usernamen und ein Password ein")
                        findLobby()
                        # TODO: Server muss abfragen ob das PW/Benutzer passt
                if OPTIONS_BACK.checkForInput(REGISTER_MOUSE_POS):
                    main_menu()
            for box in input_boxes:
                box.handle_event(event)
        for box in input_boxes:
            if safeUserAndPW:
                if username.completeText and password.completeText:
                    print(box.text)
                    box.visible = False
                    box.active = False
                    # username.Text und password.Text kann ab hier eingespeichert werden.
                else:
                    box.update()
                    box.draw(SCREEN)
        if username.completeText and password.completeText:
            safeUserAndPW = False

        pygame.display.update()

def endScreen(): # Parameter enemyName, myFastestLap, enemyFastestLap, winOrLoss
    while True:
        REGISTER_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))
        END_TEXT = get_font(45).render("This is the END screen.", True, "Black")
        END_RECT = END_TEXT.get_rect(center=(490, 160))
        SCREEN.blit(END_TEXT, END_RECT)

        enemyLapBalken = pygame.image.load("images/lobby/rectInput.png").convert_alpha()
        myLapBalken = pygame.image.load("images/lobby/rectInput.png").convert_alpha()

        SCREEN.blit(enemyLapBalken, (550, 400))
        SCREEN.blit(myLapBalken, (150, 400))

        QUIT_BUTTON = Button(image=pygame.image.load("images/lobby/rectButton.png"), pos=(490, 700),
                             text_input="QUIT", font=get_font(75), base_color=(0, 0, 0), hovering_color="White")

        QUIT_BUTTON.changeColor(REGISTER_MOUSE_POS)
        QUIT_BUTTON.update(SCREEN)

        if True:
            WIN_TEXT = get_font(45).render("Du hast gewonnen", True, "Black")
            Win_RECT = END_TEXT.get_rect(center=(550, 260))
            SCREEN.blit(WIN_TEXT, Win_RECT)
        else:
            LOSS_TEXT = get_font(45).render("hat gewonnen", True, "Black")
            LOSS_RECT = END_TEXT.get_rect(center=(550, 260))
            SCREEN.blit(LOSS_TEXT, LOSS_RECT)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(REGISTER_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def main_menu():
    safeUserAndPW = True
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(75).render("lobby", True, (0, 0, 0))
        MENU_RECT = MENU_TEXT.get_rect(center=(490, 100))

        #PLAY_BUTTON = Button(image=pygame.image.load("images/lobby/rectButton.png"), pos=(490, 400),
                             #text_input="PLAY", font=get_font(75), base_color=(0,0,0), hovering_color="White")

        #OPTIONS_BUTTON = Button(image=pygame.image.load("images/lobby/rectButton.png"), pos=(490, 550),
                                #text_input="OPTIONS", font=get_font(75), base_color=(0, 0, 0), hovering_color="White")

        LOGIN_BUTTON = Button(image=pygame.image.load("images/lobby/rectButton.png"), pos=(490, 400),
                             text_input="LOGIN", font=get_font(75), base_color=(0,0,0), hovering_color="White")

        REGISTER_BUTTON = Button(image=pygame.image.load("images/lobby/rectButton.png"), pos=(490, 550),
                             text_input="REGISTER", font=get_font(75), base_color=(0,0,0), hovering_color="White")

        QUIT_BUTTON = Button(image=pygame.image.load("images/lobby/rectButton.png"), pos=(490, 700),
                             text_input = "QUIT", font = get_font(75), base_color = (0, 0, 0), hovering_color = "White")




        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [QUIT_BUTTON, LOGIN_BUTTON, REGISTER_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    #options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                if LOGIN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    #login()
                    endScreen()
                if REGISTER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    register()


        pygame.display.update()



if __name__ == "__main__":
    main_menu()
    #game_window.GameLoop.run(game_window.GameLoop())