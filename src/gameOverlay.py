import time
import game_window
import pygame

def gameOverlayPrint():
    game_window.balkenOben = pygame.image.load("images/background/ObereSpielanzeige.PNG").convert_alpha()
    game_window.balkenOben = pygame.transform.scale(game_window.balkenOben, (game_window.WINDOW_WIDTH, 50))
    game_window.window_surface.blit(game_window.balkenOben, (0,0))

def roundStart(i):
    if i:
        game_window.lastRoundTime = 0
        game_window.round_start_time = time.time()
    else:
        game_window.lastRoundTime = time.time() - game_window.round_start_time
        game_window.round_start_time = time.time()

def printCurrentAndLastTime():
    # aktuelle Zeit printen
    font = pygame.font.Font('freesansbold.ttf', 20)
    current_time = time.time()
    game_window.aktuelleZeit = str(current_time - game_window.round_start_time)[:-13]
    game_window.window_surface.blit(font.render(game_window.aktuelleZeit, 1, (255, 255, 255)), (70, 15))

    #letzte Runde printen
    letzteRunde = str(game_window.lastRoundTime)[:-13]
    game_window.window_surface.blit(font.render(letzteRunde, 1, (255, 255, 255)), (250, 15))

def currentRound(i):
    # Runde um eins erhöhen
    if i:
        game_window.round = game_window.round + 1

    # Runde ausgeben
    else:
        font = pygame.font.Font('freesansbold.ttf', 20)
        round = str(game_window.round)
        game_window.window_surface.blit(font.render(round, 1, (255, 255, 255)), (950, 15))


