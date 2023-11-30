import math
import sys
import time
from typing import List
import pygame
import Line
import socketio
import socketPy
from socketPy import sio
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

pos = 0
playerX = 0
playerY = 1500
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


class GameLoop():

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Racing Pseudo 3D")
        #self.window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.last_time = time.time()
        self.dt = 0
        self.player_height = 0
        self.prev_height = 0

        # background
        self.background_image = pygame.image.load("images/background/background.png").convert_alpha()
        self.background_image = pygame.transform.scale(
        self.background_image, (WINDOW_WIDTH, self.background_image.get_height())
        )
        self.background_surface = pygame.Surface(
            (self.background_image.get_width() * 3, self.background_image.get_height())
        )
        self.background_surface.blit(self.background_image, (0, 0))
        self.background_surface.blit(
            self.background_image, (self.background_image.get_width(), 0)
        )
        self.background_surface.blit(
        self.background_image, (self.background_image.get_width() * 2, 0)
        )
        self.background_rect = self.background_surface.get_rect(
            topleft=(-self.background_image.get_width(), 0)
        )
        #self.window_surface.blit(self.background_surface, self.background_rect)
        window_surface.blit(self.background_surface, self.background_rect)



    def run(self):

        round = 1
        lastRoundTime = 0
        fastestRoundTime = 0

        round_start_time = time.time()
        font = pygame.font.Font('freesansbold.ttf', 20)
        # create road lines for each segment
        lines: List[Line.Line] = []
        for i in range(500):
            line = Line.Line(i)
            line.z = (
                    i * Line.segL + 0.00001
            )  # adding a small value avoids Line.project() errors

            # change color at every other 3 lines (int floor division)
            grass_color = Line.light_grass if (i // 3) % 2 else Line.dark_grass
            rumble_color = Line.white_rumble if (i // 3) % 2 else Line.black_rumble
            road_color = Line.light_road if (i // 3) % 2 else Line.dark_road
            road_color = Line.start_line if (i <=3) %2 else Line.light_road

            line.grass_color = grass_color
            line.rumble_color = rumble_color
            line.road_color = road_color

            # right curve
            if 300 < i < 700:
                #line.curve = 0.5
                line.curve = 0.0

            # uphill and downhill
            if i > 750:
                #line.y = math.sin(i / 30.0) * 1500
                line.y = 0

            # left curve
            if i > 1100:
               # line.curve = -0.7
                line.curve = 0

            lines.append(line)

        N = len(lines)
        pos = 0
        playerX = 0  # player start at the center of the road
        playerY = 1500  # camera height offset

        while True:

            self.dt = time.time() - self.last_time
            self.last_time = time.time()
            window_surface.fill((105, 205, 4))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            # Lade das Spielerbild
            if self.player_height > self.prev_height and self.player_height != 0:
                self.player_image = pygame.image.load("images/sprites/player_uphill_straight.png").convert_alpha()
            else:
                self.player_image = pygame.image.load("images/sprites/player_straight.png").convert_alpha()

            speed = 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                speed += Line.segL  # it has to be N integer times the segment length
            if keys[pygame.K_DOWN]:
                speed -= Line.segL  # it has to be N integer times the segment length
            if keys[pygame.K_RIGHT]:
                playerX += 50
                if self.player_height > self.prev_height and self.player_height != 0:
                    self.player_image = pygame.image.load("images/sprites/player_uphill_right.png").convert_alpha()
                else:
                    self.player_image = pygame.image.load("images/sprites/player_right.png").convert_alpha()
            if keys[pygame.K_LEFT]:
                playerX -= 50
                if self.player_height > self.prev_height and self.player_height != 0:
                    self.player_image = pygame.image.load("images/sprites/player_uphill_left.png").convert_alpha()
                else:
                    self.player_image = pygame.image.load("images/sprites/player_left.png").convert_alpha()
            if keys[pygame.K_w]:
                playerY += 100
            if keys[pygame.K_s]:
                playerY -= 100
            # avoid camera going below ground
            if playerY < 500:
                playerY = 500
            # turbo speed
            if keys[pygame.K_TAB]:
                speed *= 2  # it has to be N integer times the segment length
            # I-Abfrage für die schnellste Runde letzte Runde und die Rundenanzahl
            pos += speed
            if pos >= N * Line.segL:
                round += 1
                lastRoundTime = time.time() - round_start_time
                round_start_time = time.time()
                # I-Abfrage ob die jetzige Runde schneller war als die letzte
                sio.emit("lap_time", lastRoundTime)

                if round >3:
                    sio.emit("finished_race")
                    #TODO: Hier soll der Bildschirm angezeit werden

                #if fastestRoundTime == 0 or fastestRoundTime > lastRoundTime:
                    #fastestRoundTime = lastRoundTime


            self.prev_height = self.player_height  # Speichern Sie die Höhe des vorherigen Segments

            # LOOP der von start zu Finish die Position des Spielers auf 0 setzt
            while pos >= N * Line.segL:
                pos -= N * Line.segL
            while pos < 0:
                pos += N * Line.segL
            startPos = pos // Line.segL

            x = dx = 0.0  # curve offset on x axis

            self.player_height = lines[startPos].y
            camH = lines[startPos].y + playerY
            maxy = WINDOW_HEIGHT

            if speed > 0:
                self.background_rect.x -= lines[startPos].curve * 2
            elif speed < 0:
                self.background_rect.x += lines[startPos].curve * 2

            if self.background_rect.right < WINDOW_WIDTH:
                self.background_rect.x = -WINDOW_WIDTH
            elif self.background_rect.left > 0:
                self.background_rect.x = -WINDOW_WIDTH

            window_surface.blit(self.background_surface, self.background_rect)

            # draw road
            for n in range(startPos, startPos + Line.show_N_seg):
                current = lines[n % N]
                # loop the circut from start to finish = pos - (N * segL if n >= N else 0)
                current.project(playerX - x, camH, pos - (N * Line.segL if n >= N else 0))
                x += dx
                dx += current.curve

                current.clip = maxy

                # don't draw "above ground"
                if current.Y >= maxy:
                    continue
                maxy = current.Y

                prev = lines[(n - 1) % N]  # previous line

                Line.drawQuad(
                    window_surface,
                    current.grass_color,
                    0,
                    prev.Y,
                    WINDOW_WIDTH,
                    0,
                    current.Y,
                    WINDOW_WIDTH,
                )
                Line.drawQuad(
                    window_surface,
                    current.rumble_color,
                    prev.X,
                    prev.Y,
                    prev.W * 1.2,
                    current.X,
                    current.Y,
                    current.W * 1.2,
                )
                Line.drawQuad(
                    window_surface,
                    current.road_color,
                    prev.X,
                    prev.Y,
                    prev.W,
                    current.X,
                    current.Y,
                    current.W,

                )

            # Balken oben darstellen
            balken = pygame.image.load("images/background/ObereSpielanzeige.PNG").convert_alpha()
            balken = pygame.transform.scale(balken, (WINDOW_WIDTH, 50))
            window_surface.blit(balken, (0, 0))

            # Draw player with image
            self.player_image = pygame.transform.scale(self.player_image, (200, 150))  # Passe die Größe an
            player_rect = self.player_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
            window_surface.blit(self.player_image, player_rect)

            # Zeit angabe
            current_time = time.time()
            elapsed_time = current_time - round_start_time
            roundTime = str(elapsed_time)
            roundTime = roundTime[:-14]
            lastRound = str(lastRoundTime)[:-13]
            #fastestRound = str(fastestRoundTime)[:-13]

            #fastestRoundTimePrint = font.render(fastestRound, 1, (255, 255, 255))
            lastRoundTimePrint = font.render(lastRound, 1, (255, 255, 255))
            elapsed_time_text = font.render(roundTime, 1, (255, 255, 255))
            window_surface.blit(elapsed_time_text, (70, 15))
            window_surface.blit(lastRoundTimePrint, (250, 15))
            #window_surface.blit(fastestRoundTimePrint, (450, 15))

            # Runden
            currentRround = str(round)
            actuelRound = font.render(currentRround, 1, (255, 255, 255))
            window_surface.blit(actuelRound, (950, 15))
            pygame.display.update()

            # draw sprites
            for n in range(startPos + Line.show_N_seg, startPos + 1, -1):
                lines[n % N].drawSprite(window_surface)

            pygame.display.update()
            self.clock.tick(60)




