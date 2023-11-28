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


SCREEN = pygame.display.set_mode((980, 760))
pygame.display.set_caption("Menu")

BG = pygame.image.load("images/lobby/LobbyBackground.png")
username = TextInput(x=170, y=250, font=get_font(50, 3))
password = TextInput(x=490, y=250, font=get_font(50, 3), pw=True)



input_boxes = [username, password]


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

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


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(75).render("lobby", True, (0, 0, 0))
        MENU_RECT = MENU_TEXT.get_rect(center=(490, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("images/lobby/rectButton.png"), pos=(490, 400),
                             text_input="PLAY", font=get_font(75), base_color=(0,0,0), hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("images/lobby/rectButton.png"), pos=(490, 550),
                                text_input="OPTIONS", font=get_font(75), base_color=(0, 0, 0), hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("images/lobby/rectButton.png"), pos=(490, 700),
                             text_input="QUIT", font=get_font(75), base_color=(0, 0, 0), hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if username.completeText and password.completeText != "":
                        game_window.GameLoop.run(game_window.GameLoop())
                        print(username.text)
                        print("geben sie erst einen Usernamen und ein Password ein")
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
            for box in input_boxes:
                box.handle_event(event)
        for box in input_boxes:
            if username.completeText and password.completeText != "":
                box.visible = False
                box.active = False
                # username.completeText und password.completeText kann ab hier eingespeichert werden.

            box.update()
            box.draw(SCREEN)



        pygame.display.update()


if __name__ == "__main__":
    main_menu()