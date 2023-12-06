import pygame
import socketio
import game_window
sio = socketio.Client()


@sio.event
def best_lap_times(enemy, me):
    if me == None:
        me = 0.0
    if enemy == None:
        enemy = 0.0

    print("Your lap: ", me)
    print("Enemy play: ", enemy)

    # Übergabe der schnellsten Zeiten von sich selbst und dem Gegner
    game_window.fastestRoundME = str(me)[:-13]
    game_window.fastestRoundEnemy = str(enemy)[:-13]





# 1. Gegner Playername 2. meine schnellste Runde 3. gegnerische schnellste Runde 4. Boolean true = gewonnen
@sio.event
def end_game(enemy, fastest_lap, enemy_lap, boolean):
    pass

@sio.event
def connect():
    sio.emit('login', ("lewin", "123456"))
    sio.emit('find_lobby')
    print("connected to server")

sio.connect("http://localhost:3000")


