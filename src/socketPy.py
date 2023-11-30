import socketio
import game_window
sio = socketio.Client()

@sio.event
def best_lap_times(py, java):
    print("Your lap: ", py)
    print("Enemy play: ", java)
    if py == None:
        py = 0.0
    if java == None:
        java = 0.0
    game_window.window_surface.blit(py, (450, 15))
    game_window.window_surface.blit(java, (800, 15))

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


