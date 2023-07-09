import sys

import pygame


class Tetris:
    """Class managing game assets and behaviour"""

    def __init__(self) -> None:

        pygame.init

        # Game window size
        self.window_Height = 800
        self.window_Width = 800

        #
        self.screen = pygame.display.set_mode(
            (self.window_Height, self.window_Width))

        self.clock = pygame.time.Clock()

    def run_game(self):
        """Main loop of the game"""
        while True:
            # Event Check
            self.check_events()

            # Logic

            # window base
            self.screen.fill((255, 255, 255))

            # Graphics render

            # Refresh display at 60fps
            pygame.display.flip()
            self.clock.tick(60)

    def check_events(self):
        """Checks for player input - mouse and keyboard"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


game = Tetris()
game.run_game()
