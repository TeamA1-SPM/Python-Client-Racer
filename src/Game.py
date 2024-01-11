import sys
import time
import pygame

from src.constants import Settings
from src.game.Background import Background
from src.game.CarSimulation import CarSimulation
from src.game.Player import Player
from src.game.Road import Road
from src.game.RoadParser import RoadParser
from src.constants.GameState import GameState
from src.constants import GameMode
from src.game.Race import Race
from src.game.Physics import Physics
from src.game import SpriteLoader
from src.game import HUD
from src.helper.GameLoopTimer import GameLoopTimer
from src.helper.EnemyPlayer import EnemyPlayer

from src.helper.Result import Result


class GameLoop:

    def __init__(self, gameMode, gameState, connection, gameSetup):
        pygame.init()
        pygame.display.set_caption("Racing Pseudo 3D")
        self.count = 0
        self.window_surface = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
        self.background = Background()
        self.timer = GameLoopTimer()
        self.spride_loader = SpriteLoader.SpriteLoader(self.window_surface)
        self.gameState = gameState
        self.gameMode = gameMode
        self.gameSetup = gameSetup

        if self.gameMode == GameMode.MULTI_PLAYER:
            self.connection = connection
            if connection is not None:
                self.setup_socket_events()

            self.enemy = EnemyPlayer(self.gameSetup.enemy_name)
            self.enemy.set_player_x(self.gameSetup.get_start_position() * -1)
        else:
            self.connection = None

        self.roadParser = RoadParser(self.spride_loader)
        self.road = Road(self.roadParser, self.gameSetup)
        self.result = Result(self.gameSetup.player_name)
        self.race = Race(3, self.road.trackLength, self.connection, self.gameMode, self.gameState, self.result)
        self.player = Player(self.road.trackLength, self.race)
        self.maxPosition = self.road.trackLength
        self.carSim = CarSimulation(self.roadParser.car_list, self.maxPosition)
        self.isRunning = True
        self.gamePhysics = Physics(self.player, self.road)
        self.hud = HUD.HUD(self.window_surface, self.race, self.gameSetup, self.result)
        self.run()

    # zum Updaten anderer Klassen bei passendem GameState (Wird im Gameloop aufgerufen)
    def update(self):

        player_segment = self.road.findSegment(self.player.pos + Settings.PLAYER_Z)
        carSegment = self.road.get_segment_cars(player_segment.i)

        if self.race.game_state == GameState.RUNNING:

            self.background.update(player_segment.curve, self.player.speed)

            # setting inputs
            self.player.update()
            # updates collision
            self.gamePhysics.update(player_segment, carSegment)

            if self.gameMode == GameMode.MULTI_PLAYER:
                self.count = self.count + 1
                if self.count % 10 == 0:
                    try:
                        self.connection.display_player(self.player.pos, self.player.x, self.player.steer,
                                                       self.player.upDown)
                    except Exception as e:
                        print(e)

            if self.gameMode == GameMode.SINGLE_PLAYER:
                self.result.playerWon = True

            self.carSim.is_running = True
            self.carSim.update(self.player, self.enemy)
            # update laps and lap time
            self.race.update(self.player.pos)

        elif self.race.game_state == GameState.COUNTDOWN:

            if self.gameMode == GameMode.SINGLE_PLAYER:
                self.enemy = None
                self.race.set_countdown(self.timer.get_countdown())

            if self.race.countdown == 2:
                self.carSim.is_running = True

            # simuliert die Bewegung der NPC Autos
            self.carSim.update(self.player, self.enemy)

            # erneuert die NPC Autos auf der Strecke
            self.road.update(self.carSim.car_list)


        elif self.race.game_state == GameState.RESULT:

            if self.gameMode == GameMode.MULTI_PLAYER:
                self.result.playerBestTime = self.race.best_lap_time

            self.hud.result = self.result

            self.carSim.update(self.player, self.enemy)
            self.road.update(self.carSim.car_list)


        elif self.race.game_state == GameState.PAUSE:
            if self.gameMode == GameMode.MULTI_PLAYER:
                self.carSim.update(self.player, self.enemy)
                self.road.update(self.carSim.car_list)
                self.race.update(self.player.pos)

            # TODO: wenn man einmal Escape klickt, dann pausiert das spiel und geht direkt weiter.
            #       dies liegt daran, dass die Update Funktion so schnell aufgerufen wird das ein Klick auf den Escape-Button für beides zählt (pause und resume)
            # for event in pygame.event.get():
            # if event.type == pygame.QUIT:
            # pygame.QUIT
            # sys.exit()

        # keys = pygame.key.get_pressed()

        # if keys[pygame.K_ESCAPE]:
        # self.resumeGame()

        playerSegment = self.road.findSegment(self.player.pos + Settings.PLAYER_Z)

    # Aufrufen der rendermethoden anderer Klassen (Wird im Gameloop aufgerufen)
    def render(self):

        self.window_surface.fill((105, 205, 4))
        self.background.render(self.window_surface)
        self.road.render(self.window_surface, self.player)
        self.player.render_player(self.window_surface, self.spride_loader)

        self.hud.render(self.window_surface, self.race, self.player.speed, self.spride_loader, self.gameSetup)
        pygame.display.flip()  # refresh screen

    def setup_socket_events(self):
        if self.connection is not None:
            @self.connection.socket.event
            def best_lap_times(my_time, enemy_time):
                # args (my_time, enemy_time)

                self.race.set_best_lap_time(my_time)
                self.race.set_best_enemy_time(enemy_time)

            @self.connection.socket.event
            def countdown(i):
                # args (countdown)
                self.race.set_countdown(i)

            @self.connection.socket.event
            def epp(position, playerX, steer, gradient):
                # args (position, playerX, steer, gradient)

                self.enemy.set_steer(steer)
                self.enemy.set_up_down(gradient)
                self.enemy.set_position(position)
                self.enemy.set_player_x(playerX)

            @self.connection.socket.event
            def end_game(enemy_name, my_best_lap, enemy_best_lap, won_bool):
                # args (enemy_name, my_best_lap, enemy_best_lap, won_bool)
                self.result.enemyName = enemy_name
                self.result.playerBestTime = my_best_lap
                self.result.enemyBestTime = enemy_best_lap
                self.result.playerWon = won_bool

                self.race.game_state = GameState.RESULT

    # lässt das Spiel weiterlaufen, nachdem ESCAPE gedrückt wurde
    def resumeGame(self):
        self.carSim.is_running = True
        self.race.game_state = GameState.RUNNING

    # Gameloop
    def run(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT
                sys.exit()

        self.player.x = self.gameSetup.get_start_position()
        self.race.setGameState(GameState.COUNTDOWN)

        # self.carSim.add_Player(self.player)

        if self.gameMode == GameMode.SINGLE_PLAYER:
            self.timer.start_countdown()

        elif self.gameMode == GameMode.MULTI_PLAYER:
            self.carSim.addEnemy(self.enemy)

        while self.gameState is not GameState.END:

            if self.timer.is_ready():
                self.update()
                self.render()

            self.gameState = self.race.game_state
