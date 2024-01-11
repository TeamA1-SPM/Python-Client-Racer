
# Die Server Adresse um sich damit zu verbinden
URI = "https://racing-server-test.onrender.com"

# Funktionen die Parameter an den Server senden

SEND_REGISTER = "register"                 # player register function
SEND_LOGIN = "login"                       # player login function
SEND_LOGOUT = "logout"                     # player logout function
SEND_FIND_LOBBY = "find_lobby"             # player find lobby function
SEND_START_GAME = "game_rendered"          # client ready state
SEND_FINISH_RACE = "finished_race"         # client finished race
SEND_LAP_TIME = "lap_time"                 # client finished lap
SEND_POSITION = "display_player"           # send player position to server
SEND_LEAVE_LOBBY = "leave_lobby"           # send player position to server

# Funktionen um Daten von dem Server zu erhalten

GET_BEST_TRACK_TIMES = "best_track_times"
GET_BEST_LAP_TIMES = "best_lap_times"      # get enemy player lap time
GET_SERVER_COUNTDOWN = "countdown"         # get countdown from server
GET_POSITION = "epp"                       # get enemy position from server
GET_RESULT = "end_game"                    # get game results