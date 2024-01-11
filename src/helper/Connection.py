import socketio
from src.constants import Server


# Initialisiert die Verbindung mit einem Lobby-Menü und anderen Statusvariablen
class Connection:
    def __init__(self, lobby_menu):
        self.lobby = lobby_menu
        self.is_login_successful = 0
        self.is_register_successful = 0
        self.game_start = False
        self.socket = None
        self.enemyPlayer = None
        self.enemyNumber = None
        self.scoreBoard = None
        self.connect()

    # Verbindet sich mit dem Socket.IO-Server und definiert Event-Handler
    def connect(self):
        try:
            self.socket = socketio.Client()

            # Event-Handler für erfolgreiche Verbindung zum Server
            @self.socket.event
            def connect():

                self.lobby.server_Status = True

            # Event-Handler für Trennung vom Server
            @self.socket.event
            def disconnect():
                self.lobby.server_Status = False

            # Event-Handler für erfolgreichen Login
            @self.socket.event
            def login_success(login_bool):
                if login_bool:
                    self.is_login_successful = 1
                    print("logggg")
                else:
                    self.is_login_successful = 2
                    print("nologg")

            # Event-Handler für erfolgreiche Registrierung
            @self.socket.event
            def register_success(register_bool):
                if register_bool:
                    self.is_register_successful = 1
                    print("Reeegg")
                else:
                    self.is_register_successful = 2
                    print("noRegg")

            # Event-Handler für Spielstart
            @self.socket.event
            def start_game(playername, player):
                print(playername)
                print(player)
                self.enemyPlayer = playername
                self.enemyNumber = player
                self.ready()
                self.game_start = True

            # Event-Handler für das Scoreboard
            @self.socket.event
            def score_board(score_board_array):

                self.scoreBoard = score_board_array
                print(score_board_array)

            self.socket.connect('https://racing-server.onrender.com')

        except Exception as e:
            print(e)

    # Gibt das aktuelle Socket-Objekt zurück
    def get_socket(self):
        return self.socket

    # Sendet eine Registrierungsanfrage an den Server
    def register(self, username, password):
        if self.socket:
            data = {
                "username": username,
                "passwort": password,
                "loggedIn": "false"
            }
            self.socket.emit(Server.SEND_REGISTER, data)

    # Sendet eine Login-Anfrage an den Server
    def login(self, username, password):
        if self.socket:
            self.socket.emit(Server.SEND_LOGIN, (username, password))

    # Sendet eine Logout-Anfrage an den Server
    def logout(self):
        if self.socket:
            self.socket.emit(Server.SEND_LOGOUT)

    # Sendet eine Anfrage zum Finden einer Lobby an den Server
    def find_lobby(self):
        if self.socket:
            self.socket.emit(Server.SEND_FIND_LOBBY)

    # Sendet eine Anfrage zum Verlassen einer Lobby an den Server
    def leave_lobby(self):
        if self.socket:
            self.socket.emit(Server.SEND_LEAVE_LOBBY)

    # Sendet die Rundenzeit an den Server
    def send_lap_time(self, lap_time):
        if self.socket:
            self.socket.emit(Server.SEND_LAP_TIME, lap_time)

    # Sendet eine Meldung, dass das Rennen beendet wurde, an den Server
    def send_finished_race(self):
        if self.socket:
            self.socket.emit(Server.SEND_FINISH_RACE)

    # Sendet eine Meldung, dass der Spieler bereit ist, an den Server
    def ready(self):
        if self.socket:
            self.socket.emit(Server.SEND_START_GAME)

    # Sendet die aktuelle Position und Steuerungsinformationen an den Server
    def display_player(self, position, playerX, steer, gradient):
        if self.socket:
            self.socket.emit('display_player', (position, playerX, steer, gradient))

    # Sendet eine Anfrage für die besten Rundenzeiten auf einer Strecke an den Server
    def best_track_times(self, track):
        if self.socket:
            self.socket.emit(Server.GET_BEST_TRACK_TIMES, track)
