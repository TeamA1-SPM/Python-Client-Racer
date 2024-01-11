import pygame
import os
from src.constants import Settings


# Klasse um den Hintergrund darzustellen
class Background:
    def __init__(self):
        self.sky = None
        self.hills = None
        self.trees = None

        self.sky_offset = 0
        self.hill_offset = 0
        self.tree_offset = 0

        self.SKY_SPEED = 0.006
        self.HILL_SPEED = 0.009
        self.TREE_SPEED = 0.02

        self.image_height = 0
        self.image_width = 0

        self.sky_height = 480
        self.sky_width = 1280

        self.load_images()
        self.scale_images()

    # Skalierung des Himmels
    def scale_images(self):

        ratio_height = Settings.WINDOW_HEIGHT / self.sky_height
        ratio_width = Settings.WINDOW_WIDTH / self.sky_width
        self.image_height = int(self.sky_height * ratio_height)
        self.image_width = int(self.sky_width * ratio_width)

    # Funktion, um die einzelnen Bilder für den Himmel, die Berge und die Bäume zu laden
    def load_images(self):
        sky_path = os.path.join("images", "background", "sky.png")
        self.sky = pygame.image.load(sky_path).convert_alpha()
        # self.sky = pygame.transform.scale(self.sky, (Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))

        hills_path = os.path.join("images", "background", "hills.png")
        self.hills = pygame.image.load(hills_path).convert_alpha()
        self.hills = pygame.transform.scale(self.hills, (1280, 480))

        trees_path = os.path.join("images", "background", "trees.png")
        self.trees = pygame.image.load(trees_path).convert_alpha()
        self.trees = pygame.transform.scale(self.trees, (Settings.WINDOW_WIDTH * 1.5, Settings.WINDOW_HEIGHT))

    def update(self, curve, speed):
        factor = curve * speed / 100

        self.sky_offset += int(self.SKY_SPEED * factor)
        if self.sky_offset >= self.image_width:
            self.sky_offset -= self.image_width
        elif self.sky_offset <= -self.image_width:
            self.sky_offset += self.image_width

        self.hill_offset += int(self.HILL_SPEED * factor)
        if self.hill_offset >= self.image_width:
            self.hill_offset -= self.image_width
        elif self.hill_offset <= -self.image_width:
            self.hill_offset += self.image_width

        self.tree_offset += int(self.TREE_SPEED * factor)
        if self.tree_offset >= self.image_width:
            self.tree_offset -= self.image_width
        elif self.tree_offset <= -self.image_width:
            self.tree_offset += self.image_width

    # Zeichnen, des Hindergrundes auf dem Bildschirm, mithilfe der parallax Funktion
    def render(self, screen):

        self.render_parallax(screen, self.sky, self.sky_offset)
        self.render_parallax(screen, self.hills, self.hill_offset)
        self.render_parallax(screen, self.trees, self.tree_offset)

    # laden von zwei Bildern, damit sich der Hintergrund verschieben kann
    def render_parallax(self, screen, image, offset_x):

        screen.blit(image, (offset_x, 0, self.image_width, self.image_height))

        if offset_x > 0:
            screen.blit(image, (offset_x - self.image_width, 0, self.image_width, self.image_height))

        if offset_x < 0:
            screen.blit(image, (offset_x + self.image_width, 0, self.image_width, self.image_height))
