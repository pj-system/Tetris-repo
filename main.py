import sys
import pygame

from game_blocks import Block


class Tetris:
    """Class managing game assets and behaviour"""

    def __init__(self) -> None:

        pygame.init

        # Game window size
        self.WINDOW_HEIGHT = 880
        self.WINDOW_WIDTH = 800

        # intitalise game window
        self.screen = pygame.display.set_mode(
            (self.WINDOW_HEIGHT, self.WINDOW_WIDTH))
        pygame.display.set_caption("TETRIS")

        self.clock = pygame.time.Clock()

    def run_game(self):
        """Main loop of the game"""
        while True:
            # Event Check
            self.check_events()

            # Game Logic
            # tbc

            # window background and UI
            self.screen.fill((0, 0, 0))

            # Graphics render
            # tbc

            # Refresh display at 60fps
            pygame.display.flip()
            self.clock.tick(60)

    def check_events(self):
        """Checks for player input - mouse and keyboard"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()


game = Tetris()
game.run_game()
