import pygame
import game_window
from button import Button


def get_font(size, i=1):  # Returns Press-Start-2P in the desired size
    if i == 1:
        return pygame.font.Font("images/lobby/Overthink.ttf", size)
    elif i == 2:
        return pygame.font.Font("images/lobby/font.ttf", size)
    elif i == 3:
        return pygame.font.Font(None, size)
