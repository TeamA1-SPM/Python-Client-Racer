import pygame

from src.constants import Settings
from src.constants.Settings import ROAD_WIDTH, WINDOW_WIDTH, CAMERA_DEPTH, SEGMENT_LENGTH, DRAW_DISTANCE


class Road:
    def __init__(self, roadParser, gameSetup):
        self.road = roadParser.get_track(gameSetup.track_nr)
        self.trackLength = Settings.SEGMENT_LENGTH * len(self.road)
        self.roadParser = roadParser
        self.car_list = roadParser.car_list

    # aktualisiert die Liste der Autos die sich in dem Spiel befinden
    def update(self, carList):
        self.car_list = carList

    # gibt das Segment an der übergebenen (pos) Position wieder
    def findSegment(self, pos):
        index = (pos / Settings.SEGMENT_LENGTH) % len(self.road)
        return self.road[int(index)]

    def percentRemaining(self, n):
        return (n % Settings.SEGMENT_LENGTH) / Settings.SEGMENT_LENGTH

    def interpolate(self, a, b, percent):
        return a + (b - a) * percent

    def project(self, pWorld, pCamera, pScreen, cameraX, cameraY, cameraZ):
        width = Settings.WINDOW_WIDTH / 2
        height = Settings.WINDOW_HEIGHT / 2

        pCamera.x = pWorld.x - cameraX
        pCamera.y = pWorld.y - cameraY
        pCamera.z = pWorld.z - cameraZ

        scale = 0
        if (pCamera.z != 0):
            scale = Settings.CAMERA_DEPTH / pCamera.z

        pScreen.x = round(width + (scale * pCamera.x * width))
        pScreen.y = round(height - (scale * pCamera.y * height))
        pScreen.z = round(scale * Settings.ROAD_WIDTH * width)

    def drawSegment(self, window_surface, segment):
        # Extrahiere die Bildschirmkoordinaten und Breiteninformationen der Straßensegmentpunkte
        x1 = int(segment.p1screen.x)
        y1 = int(segment.p1screen.y)
        w1 = int(segment.p1screen.z)
        x2 = int(segment.p2screen.x)
        y2 = int(segment.p2screen.y)
        w2 = int(segment.p2screen.z)

        # Zeichne den Grasbereich
        pygame.draw.polygon(window_surface, segment.grass_color, [
            (0, y1),
            (0, y2),
            (Settings.WINDOW_WIDTH, y2),
            (Settings.WINDOW_WIDTH, y1)
        ])

        # Zeichne die Unebenheiten am Straßenrand ("rumble")
        r1 = w1 / max(6, 2 * Settings.LANES)
        r2 = w2 / max(6, 2 * Settings.LANES)
        pygame.draw.polygon(window_surface, segment.rumble_color, [
            (x1 - w1 - r1, y1),
            (x1 - w1, y1),
            (x2 - w2, y2),
            (x2 - w2 - r2, y2)
        ])
        pygame.draw.polygon(window_surface, segment.rumble_color, [
            (x1 + w1 + r1, y1),
            (x1 + w1, y1),
            (x2 + w2, y2),
            (x2 + w2 + r2, y2)
        ])

        # Zeichne die Straße
        pygame.draw.polygon(window_surface, segment.road_color, [
            (x1 - w1, y1),
            (x1 + w1, y1),
            (x2 + w2, y2),
            (x2 - w2, y2)
        ])
        # Zeichne Fahrspuren, wenn vorhanden
        if segment.isLane:
            l1 = w1 / max(32, 8 * Settings.LANES)
            l2 = w2 / max(32, 8 * Settings.LANES)
            lanew1 = w1 * 2 / Settings.LANES
            lanew2 = w2 * 2 / Settings.LANES
            lanex1 = x1 - w1 + lanew1
            lanex2 = x2 - w2 + lanew2

            for lane in range(Settings.LANES - 1):
                pygame.draw.polygon(window_surface, segment.line_color, [
                    (lanex1 - l1 / 2, y1),
                    (lanex1 + l1 / 2, y1),
                    (lanex2 + l2 / 2, y2),
                    (lanex2 - l2 / 2, y2)
                ])
                lanex1 += lanew1
                lanex2 += lanew2

    def render(self, window_surface, player):
        # Finde das Basis-Segment und den Prozentanteil innerhalb dieses Segments
        baseSegment = self.findSegment(player.pos)
        basePercent = self.percentRemaining(player.pos)

        # Finde das Spieler-Segment und den Prozentanteil innerhalb dieses Segments
        playerSegment = self.findSegment(player.pos + Settings.PLAYER_Z)
        playerPercent = self.percentRemaining(player.pos + Settings.PLAYER_Z)

        # Interpoliere die Spielerposition auf der vertikalen Achse
        player.y = self.interpolate(playerSegment.p1world.y, playerSegment.p2world.y, playerPercent)
        maxy = Settings.WINDOW_HEIGHT

        x = 0
        dx = -(baseSegment.curve * basePercent)

        # Schleife über die zu zeichnenden Straßensegmente
        for n in range(Settings.DRAW_DISTANCE):
            segment = self.road[(baseSegment.i + n) % len(self.road)]
            segment.isLooped = segment.i < baseSegment.i
            segment.clip = maxy

            # Berechne Kamerakoordinaten
            cameraX = (player.x * Settings.ROAD_WIDTH) - x
            cameraY = Settings.CAMERA_HEIGHT + player.y
            cameraZ = player.pos
            if segment.isLooped:
                cameraZ -= self.trackLength

            # Projiziere Weltkoordinaten auf Bildschirmkoordinaten
            self.project(segment.p1world, segment.p1camera, segment.p1screen, cameraX, cameraY, cameraZ)
            self.project(segment.p2world, segment.p2camera, segment.p2screen, cameraX - dx, cameraY, cameraZ)

            x += dx
            dx += segment.curve

            # Überspringe unsichtbare oder außerhalb des Fensters liegende Segmente
            if (segment.p1camera.z <= Settings.CAMERA_DEPTH
                    or segment.p2screen.y >= segment.p1screen.y
                    or segment.p2screen.y >= maxy):
                continue

            # Zeichne das aktuelle Straßensegment
            self.drawSegment(window_surface, segment)
            maxy = segment.p2screen.y

        # Rendere Straßensprites und NPC-Autos
        for n in range(DRAW_DISTANCE - 150, 4, -1):
            index = (baseSegment.i + n) % len(self.road)
            segment = self.road[index]
            segmentcar_list = self.get_segment_cars(index)

            # Rendere Autos
            for car in segmentcar_list:
                percent = self.percentRemaining(car.position)
                sprite_scale = self.interpolate(CAMERA_DEPTH / segment.p1camera.z,
                                                CAMERA_DEPTH / segment.p2camera.z, percent)
                sprite_x = self.interpolate(segment.p1screen.x, segment.p2screen.x, percent) + (
                        sprite_scale * car.offset * ROAD_WIDTH * WINDOW_WIDTH / 2)
                sprite_y = self.interpolate(segment.p1screen.y, segment.p2screen.y, percent)
                self.roadParser.sprites_loader.render(window_surface, car.name, sprite_scale, sprite_x, sprite_y, -0.5,
                                                      -1,
                                                      segment.clip)

            # Rendere Objekte am Straßenrand
            for obj in segment.roadside_list:
                sprite_scale = CAMERA_DEPTH / segment.p1camera.z
                sprite_x = segment.p1screen.x + (
                        sprite_scale * obj.offset * ROAD_WIDTH * WINDOW_WIDTH / 2)
                sprite_y = segment.p1screen.y
                offset = -1 if obj.offset < 0 else 0
                self.roadParser.sprites_loader.render(window_surface, obj.name, sprite_scale, sprite_x, sprite_y,
                                                      offset, -1, segment.clip)

    def get_segment_cars(self, index):
        segment_cars = []
        start_position = index * SEGMENT_LENGTH
        for car in self.car_list:
            car_position = car.position
            if start_position <= car_position <= start_position + SEGMENT_LENGTH:
                segment_cars.append(car)

        return segment_cars
