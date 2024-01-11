from src.constants import Settings
from src.helper.Segment import Segment


class Physics:
    def __init__(self, player, CarSegment):
        self.player = player
        self.playerSegment = player
        self.carSegment = CarSegment

    # Aktualisierung der Spieler Physik
    def update(self, playerSegment, carSegment):
        self.playerSegment = playerSegment
        self.carSegment = carSegment

        # Spieler x Position
        self.player_x_position()

        # Spieler Bewegung nach vorne
        self.player_velocity()

        # Abfrage, ob bergauf oder runter gefahren wird
        self.player_up_down()

        # Kollision mit den anderen Objekten an der Straße
        self.road_side_collision()

        # Kollision mit den anderen Autos
        self.car_collision()

    # Abfrage, ob bergauf oder runter gefahren wird
    def player_up_down(self):
        self.player.upDown = (self.playerSegment.p2world.y - self.playerSegment.p1world.y)

    # Spieler x Position
    def player_x_position(self):

        speed = self.player.speed
        speed_percent = speed / Settings.MAX_SPEED

        player_x = self.player.x
        dx = Settings.STEP * 2 * speed_percent

        # Spieler physik in den Kurven
        player_x -= dx * speed_percent * Settings.CENTRIFUGAL * self.playerSegment.curve
        self.player.set_player_x(player_x)

        # Spielerbewegung nach rechts und links
        steer = self.player.steer
        if steer == 1:
            self.player.set_player_x(player_x + dx)
        elif steer == -1:
            self.player.set_player_x(player_x - dx)

        # Prüft ob der Spieler von der Straße runterfährt
        if (player_x < -1) or (player_x > 1):
            if speed > Settings.OFF_ROAD_LIMIT:
                self.player.accel = Settings.OFF_ROAD_DECEL

    # Spielerbewegung nach vorne
    def player_velocity(self):
        position = self.player.pos
        speed = self.player.speed

        # player speed update
        speed += self.player.accel * Settings.STEP
        self.player.set_speed(speed)
        # player position update
        position += speed * Settings.STEP
        self.player.set_position(position)
        # reset acceleration
        self.player.accel = 0

    # Kollision mit den anderen Objekten an der Straße
    def road_side_collision(self):
        player_x = self.player.x

        if (player_x < -1) or (player_x > 1):
            road_side_sprites = self.playerSegment.roadside_list
            for sprite in road_side_sprites:
                print(sprite)
                sprite_w = sprite.width
                if self.overlap(player_x, Settings.PLAYER_W,
                                (sprite.offset + sprite_w / 2 * (1 if sprite.offset > 0 else -1)), sprite_w, 0.0):
                    self.player.speed = (Settings.MAX_SPEED / 5)
                    self.player.pos = (self.playerSegment.p1world.z - Settings.PLAYER_Z)
                    break

    # Kollision mit den anderen Autos
    def car_collision(self):
        car_list = self.carSegment
        for car in car_list:
            if self.player.speed > car.speed:
                if self.overlap(self.player.x, Settings.PLAYER_W, car.offset, car.width, 0.8):
                    car_speed = car.speed
                    self.player.speed = car_speed * (car_speed / self.player.speed)
                    self.player.pos = car.position - Settings.PLAYER_Z


    # Kalkulation ob die Bilder überlappen
    def overlap(self, x1, w1, x2, w2, percent):
        half = percent / 2 if percent != 0 else 1 / 2
        min1 = x1 - (w1 * half)
        max1 = x1 + (w1 * half)
        min2 = x2 - (w2 * half)
        max2 = x2 + (w2 * half)

        return not (max1 < min2 or min1 > max2)
