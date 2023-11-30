import pygame

class TextInput:
    def __init__(self, initial_text="", font=None, x=200, y=150, pw=False):
        self.text = initial_text
        self.font = font
        self.pw = pw
        self.visible = True
        self.completeText = False

        # Lade das Hintergrundbild
        self.background_image = pygame.image.load("images/lobby/rectInput.png")

        # Erstelle eine Rect, basierend auf der Größe des Hintergrundbildes
        self.input_rect = self.background_image.get_rect(topleft=(x, y))

        self.color = pygame.Color((255, 0, 0))
        self.active = False
        self.text_surface = self.font.render(initial_text, True, self.color)
        self.width = max(300, 40)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.active = not self.active
            elif len(self.text) > 4:
                self.active = False
                self.completeText = True
            else:
                self.active = False
        if self.active and self.visible:
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN and len(self.text) > 4:
                        self.active = False
                        self.completeText = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        # Prüfe, ob die Länge des Textes 10 überschreitet
                        if len(self.text) < 10:
                            self.text += event.unicode
                    if self.pw:
                        hidePW = len([char for char in self.text if char.isalpha()]) * "*"
                        self.text_surface = self.font.render(hidePW, True, self.color)
                    else:
                        self.text_surface = self.font.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.width)
        self.input_rect.w = width

    def draw(self, screen):
        if self.visible:
            # Zeichne das Hintergrundbild
            screen.blit(self.background_image, self.input_rect)

            # Hier zeichnest du die Texteingabe auf den Hintergrund
            screen.blit(self.text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
