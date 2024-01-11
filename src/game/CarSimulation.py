from src.constants.Settings import PLAYER_Z, SEGMENT_LENGTH, STEP, MAX_SPEED, PLAYER_W
from src.constants.Car import Car


class CarSimulation:
    def __init__(self, car_list, max_position):
        self.car_list = car_list
        self.max_position = max_position
        self.is_running = False
        self.playerCar = None
        self.enemyCar = None

    # Fügt ein Auto, das die werte des Spielers hat, der Liste hinzu
    def add_Player(self, player):
        self.playerCar = Car(None, player.x, PLAYER_Z - SEGMENT_LENGTH, 0, PLAYER_W)
        self.car_list.append(self.playerCar)

    # Fügt ein Auto, mit den Werten des Gegenspielers, der Liste hinzu
    def addEnemy(self, enemy):
        if enemy is not None:

            self.enemyCar = Car(enemy.get_sprite_name(), enemy.playerX, PLAYER_Z, 0, PLAYER_W)
            self.car_list.append(self.enemyCar)

    # stellt die Hitbox da, diese muss sich mit dem Spieler mitbewegen
    def update_player_sprites(self, car, position, x):

        index = self.car_list.index(car)
        enemyCar = self.car_list[index]
        enemyCar.position = position
        enemyCar.offset = x

    def update(self, player, enemy):
        if not self.is_running:
            return
        if enemy is not None:
            self.update_player_sprites(self.enemyCar, (enemy.position + PLAYER_Z), enemy.playerX)

        for car in self.car_list:
            offset = car.offset
            offset += self.update_car_offset(car)
            car.offset = offset
            self.increase_npc_position(car)

    # gibt die Segmente aller Autos aus der Liste zurück, die sich zwischen dem Startpunkt und Endpunkt befinden
    def get_segment_cars(self, segment_start):
        return [car for car in self.car_list if segment_start <= car.position <= segment_start + SEGMENT_LENGTH]

    # erhöht die Position der NPC Autos
    def increase_npc_position(self, car):
        position = car.position
        position += STEP * car.speed
        if position >= self.max_position:
            position -= self.max_position
        car.position = position

    # ist dazu da um zu berechnen wann ein Auto gerendert werden soll
    def update_car_offset(self, car):
        position = car.position
        segment_start = position - (position % SEGMENT_LENGTH)
        result = 0

        for counter in range(1, 5):
            segment_start = (segment_start + SEGMENT_LENGTH) % self.max_position

            segment_cars = self.get_segment_cars(segment_start)

            for other_car in segment_cars:
                if car.speed > other_car.speed and self.overlap(car.offset, car.width, other_car.offset,
                                                                other_car.width):
                    if other_car.offset > 0.5:
                        result = -1
                    elif other_car.offset < -0.5:
                        result = 1
                    else:
                        result = 1 if car.offset > other_car.offset else -1
                    return result * 1 / counter * (car.speed - other_car.speed) / MAX_SPEED

        return 0.1 if car.offset < -0.9 else (-0.1 if car.offset > 0.9 else 0)

    def overlap(self, x1, w1, x2, w2):
        half = 1.2 / 2
        min1 = x1 - (w1 * half)
        max1 = x1 + (w1 * half)
        min2 = x2 - (w2 * half)
        max2 = x2 + (w2 * half)
        return not (max1 < min2 or min1 > max2)
