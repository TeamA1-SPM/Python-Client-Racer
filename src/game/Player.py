import sys
import random

import pygame
from src.constants import Settings
from src.constants.GameState import GameState


class Player:
    def __init__(self, maxPos, race):
        self.pos = 0
        self.maxPos = maxPos
        self.x = 0
        self.speed = 0
        self.steer = 0
        self.accel = 0
        self.upDown = 0
        self.player_height = 0
        self.prev_height = 0
        # Bilder für das Auto des Spielers
        self.image_up = pygame.image.load("../src/images/sprites/player_straight.png").convert_alpha()
        self.image_up_hill = pygame.image.load("../src/images/sprites/player_uphill_straight.png").convert_alpha()
        self.image_left = pygame.image.load("../src/images/sprites/player_left.png").convert_alpha()
        self.image_left_hill = pygame.image.load("../src/images/sprites/player_uphill_left.png").convert_alpha()
        self.image_right = pygame.image.load("../src/images/sprites/player_right.png").convert_alpha()
        self.image_right_hill = pygame.image.load("../src/images/sprites/player_uphill_right.png").convert_alpha()
        self.player_image = self.image_up
        self.race = race


    # Aktualisierung, Spielerbewegung und der Geschwindigkeit
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if self.speed > 0:
                self.steer = -1
        elif keys[pygame.K_RIGHT]:
            if self.speed > 0:
                self.steer = 1
        if keys[pygame.K_UP]:
            self.accel = Settings.ACCEL
        elif keys[pygame.K_DOWN]:
            if self.speed > 0:
                self.accel = Settings.BREAKING
            else:
                self.steer = 0
        elif keys[pygame.K_ESCAPE]:
            self.race.game_state = GameState.PAUSE
        else:
            if self.speed > 0:
                self.accel = Settings.DECEL

    # Darstellung des Spielers
    def render_player(self, screen, sprites_loader):
        sprite_name = self.get_player_sprite_name()

        scale = Settings.CAMERA_DEPTH / Settings.PLAYER_Z
        dest_x = Settings.WINDOW_WIDTH / 2
        dest_y = Settings.WINDOW_HEIGHT - 6

        sprites_loader.render(screen, sprite_name, scale, dest_x, dest_y + self.calc_bounce(), -0.5, -1, 0)
        self.steer = 0


    def calc_bounce(self):
        rnd_double = random.random()

        sign = random.choice([-1, 1])
        rnd_double *= sign

        return (1.5 * random.random() * self.speed / Settings.MAX_SPEED * Settings.WINDOW_WIDTH / Settings.WINDOW_HEIGHT) * rnd_double

    # gibt den Namen des Bildes wieder, je nachdem wie er sich verhält
    def get_player_sprite_name(self):
        if self.steer < 0:
            sprite = "PLAYER_LEFT"
            if self.upDown > 0:
                sprite = "PLAYER_UPHILL_LEFT"
        elif self.steer > 0:
            sprite = "PLAYER_RIGHT"
            if self.upDown > 0:
                sprite = "PLAYER_UPHILL_RIGHT"
        else:
            sprite = "PLAYER_STRAIGHT"
            if self.upDown > 0:
                sprite = "PLAYER_UPHILL_STRAIGHT"

        return sprite


    # setzt den x Wert für den Spieler
    def set_player_x(self, player_x):
        PLAYER_X_LIMIT = 2  # Ersetzen Sie 10 durch den tatsächlichen Wert für PLAYER_X_LIMIT

        if -PLAYER_X_LIMIT <= player_x <= PLAYER_X_LIMIT:
            self.x = player_x

    # setzt die Position des Spielers
    def set_position(self, position):
        if position >= self.maxPos:
            self.pos = position - self.maxPos
        elif position < 0:
            self.pos = position + self.maxPos
        else:
            self.pos = position

    # setzt die Geschwindigkeit des Spielers
    def set_speed(self, speed):
        if speed > Settings.MAX_SPEED:
            speed = Settings.MAX_SPEED
        elif speed < 0:
            speed = 0
        self.speed = speed




