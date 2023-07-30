import pygame
from settings import Settings


class Button():
    def __init__(self, tet_game: object, text: str) -> None:
        """Class creating game buttons"""
        # game window from main:
        self.screen = tet_game.screen

        # Variables from settings:
        settings = Settings()
        self.BUTTON_WIDTH = settings.BUTTON_WIDTH
        self.BUTTON_HEIGHT = settings.BUTTON_HEIGHT

        # text to display on the button:
        self.text = text
        self.text_font = pygame.font.SysFont("arial", 25, True)
        self.text_colour = (255, 255, 255)

        # concept - change colour if mouse over the button
        self.button_border = 10

        # create button rect object:
        self.button = pygame.Rect(0, 0, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)

    def draw(self, coordinate: list, centered: bool):
        """Draws the button at an indicated coordinate.\n
        centered = True: button is drawn centered at the coordinate. \n
        centered = False: button is drawn with coordinate as top left corner.\n
        coordinate needs [left, top] eqivelent to [x, y]"""
        if centered == True:
            self.button.center = coordinate
        else:
            self.button.topleft = coordinate

        pygame.draw.rect(self.screen, (120, 120, 120),
                         self.button, self.button_border)
        self._text_render_init()
        self.screen.blit(self.text_image, self.text_image_rect)

    def _text_render_init(self):
        """Renders text as an image to be placed on top of the button"""
        self.text_image = self.text_font.render(
            self.text, True, self.text_colour, None)
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.center = self.button.center
