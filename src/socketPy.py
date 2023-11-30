import pygame
import socketio
import game_window
sio = socketio.Client()

#font = pygame.font.Font('freesansbold.ttf', 20)
@sio.event
def best_lap_times(enemy, me):
    if me == None:
        me = 0.0
    if enemy == None:
        enemy = 0.0

    print("Your lap: ", me)
    print("Enemy play: ", enemy)
    font = pygame.font.Font('freesansbold.ttf', 20)

    game_window.fastestRoundME = str(me)[:-13]

    #game_window.fastestRoundME = font.render(fastestRound, 1, (255, 255, 255))
    game_window.fastestRoundEnemy = str(enemy)[:-13]
    #game_window.fastestRoundEnemy = font.render(enemyFastestRound, 1, (255, 255, 255))




# 1. Gegner Playername 2. meine schnellste Runde 3. gegnerische schnellste Runde 4. Boolean true = gewonnen
@sio.event
def end_game(enemy, fastest_lap, enemy_lap, boolean):
    pass

@sio.event
def connect():
    sio.emit('login', ("timo", "123456"))
    sio.emit('find_lobby')
    print("connected to server")

sio.connect("http://localhost:3000")


