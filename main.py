import sys
import pygame
import copy

from game_blocks import Block
from game_space import GameSpace
from settings import Settings
from button import Button
from tet_bot import TetBot


class Tetris:
    """Class managing game assets and behaviour"""

    def __init__(self) -> None:

        pygame.init()
        settings = Settings()
        # Game window size
        self.WINDOW_HEIGHT = settings.WINDOW_HEIGHT
        self.WINDOW_WIDTH = settings.WINDOW_WIDTH

        # intitalise game window
        self.screen = pygame.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("PJ's TETRIS")

        # temp!!!!!!!!!
        self.BOT = TetBot(self)

        # inicialise grid
        self.play_field = GameSpace(self)

        # initialise buttons
        self.play_button = Button(self, "PLAY")
        self.restart_button = Button(self, "RESTART")
        self.bot_button = Button(self, "RUN BOT (WIP)")
        self.quit_button = Button(self, "QUIT")
        # Button Array
        self.buttons = [self.play_button, self.restart_button,
                        self.bot_button, self.quit_button]
        # Button spawn location Array
        self.button_loc = [[660, 520], [660, 520], [660, 640], [660, 760]]

        # set user event to periodically lower the block and timer for block drop event
        self.drop_rate = settings.drop_rate
        self.accelerate_rate = settings.accelerate
        self.soft_drop_block = pygame.USEREVENT + 0
        pygame.time.set_timer(self.soft_drop_block, 0)
        self.clock = pygame.time.Clock()
        # Set UI font
        self.text_font = pygame.font.SysFont("arial", 30, True)

        # Set state booleans
        self.can_save = True
        self.can_use_saved = True

        # Initialise socre counter
        self.score = 0
        # Start application in game inactive state
        self.game_active = False

    def run_game(self):
        """Main loop of the game"""
        while True:
            # Event Check
            self.check_events()

            # window background and UI
            self.screen.fill((0, 0, 0))
            # Graphics render
            if self.game_active == True:
                # draw on-screen text
                self.draw_text()
                # draw game board (blocks placed)
                self.play_field.draw_board()
                # draw all blocks
                self.block.draw()
                self.next_block.draw_tetromino([120, 700])
                if self.saved_block:
                    self.saved_block.draw_tetromino([360, 700])
                # draw grid (grid lines)
                self.play_field.draw_grid()
                for pos, btn in enumerate(self.buttons):
                    if btn != self.play_button:
                        btn.draw(self.button_loc[pos], False)
            else:
                for pos, btn in enumerate(self.buttons):
                    if btn != self.restart_button:
                        btn.draw(self.button_loc[pos], False)

                self.draw_text()
                self.play_field.draw_board()
                self.play_field.draw_grid()

            # Refresh display at 60fps
            pygame.display.flip()
            self.clock.tick(60)

    def check_events(self):
        """Checks for player input - mouse and keyboard"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Keyboard events:
            # key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                if self.game_active:
                    # key presses:
                    if event.key == pygame.K_RIGHT:
                        self.block.move(1)
                    if event.key == pygame.K_LEFT:
                        self.block.move(-1)
                    if event.key == pygame.K_DOWN:
                        self._accelerate_block()
                    if event.key == pygame.K_UP:
                        self.block.rotate(True)
                    if event.key == pygame.K_SPACE:
                        self.drop_and_add_score()
                        self._new_block()
                    if event.key == pygame.K_v:
                        self.save_shape()
                    if event.key == pygame.K_b:
                        self.use_saved_shape()
                    # Restart
                    if event.key == pygame.K_r:
                        self.reset()
                    # FOR TESTING ONLY
                    if event.key == pygame.K_p:
                        self.BOT._evaluate_grid(self.play_field.grid)
                    if event.key == pygame.K_t:
                        self.BOT.generate_moves(
                            self.play_field.grid, self.block)
            # key releases:
            if event.type == pygame.KEYUP:
                if self.game_active:
                    if event.key == pygame.K_DOWN:
                        self._decelerate_block()
            # Mouse events:
            # Mouse hover:
            if event.type == pygame.MOUSEMOTION:
                for btn in self.buttons:
                    if btn.button.collidepoint(pygame.mouse.get_pos()):
                        btn.button_border = 0
                    else:
                        btn.button_border = 10
            # Mouse presses:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.button.collidepoint(event.pos):
                    self.play_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.restart_button.button.collidepoint(event.pos):
                    self.reset()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.bot_button.button.collidepoint(event.pos):
                    pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.quit_button.button.collidepoint(event.pos):
                    sys.exit()

            # block drop on timer (USEREVENT 0)
            if self.game_active:
                if event.type == self.soft_drop_block:
                    if not self.block.update():
                        self._add_to_grid()
                        self.score += self.play_field.check_clear()
                        self._new_block()
                        self.can_save = True
                        self.can_use_saved = True
                        #self.game_active = False

    def play_game(self):
        # initialise blocks
        self.block = Block(self)
        self.next_block = Block(self)
        self.saved_block = None
        pygame.time.set_timer(self.soft_drop_block, self.drop_rate)
        self.game_active = True

    def reset(self):
        """Resets the game state to start start state (Restart)"""
        self.play_field = GameSpace(self)
        self.block = Block(self)
        self.next_block = Block(self)
        self.saved_block = None
        self.score = 0
        self.can_save = True
        self.game_active = True

    def save_shape(self):
        """Saves the current block to be swapped in later"""
        if not self.saved_block and self.can_save == True:
            self.saved_block = self.block
            self._new_block()
            self.can_use_saved = False

    def use_saved_shape(self):
        """Takes the saved shape and puts it in play"""
        if self.saved_block and self.can_use_saved == True:
            self.block = self.saved_block
            self.saved_block = None
            self.block.set_start()
            self.can_save = False

    def draw_text(self):
        """ Draws all text based game elements"""
        # This needs work - WIP
        score_heading = self.text_font.render("SCORE:", True, (255, 255, 255))
        self.screen.blit(score_heading, (25, 25))

        score_text = self.text_font.render(
            f'{self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (25, 60))

        next_shape_heading = self.text_font.render(
            "Next Shape:", True, (255, 255, 255))
        self.screen.blit(next_shape_heading, (660, 30))
        saved_shape_heading = self.text_font.render(
            "Saved Shape:", True, (255, 255, 255))
        self.screen.blit(saved_shape_heading, (660, 270))

    def _add_to_grid(self):
        """Helper method updating the grid once the block lands"""
        for coor in self.block.shape:
            grid_row, grid_col = coor[0], coor[1]
            self.play_field.grid[grid_row][grid_col] = self.block.shape_color

    def _accelerate_block(self):
        """increases soft drop rate of the block"""
        pygame.time.set_timer(self.soft_drop_block, self.accelerate_rate)

    def _decelerate_block(self):
        """decreases soft drop rate to baseline"""
        pygame.time.set_timer(self.soft_drop_block, self.drop_rate)

    def drop_and_add_score(self):
        """Drops the block to the lowest possible position and tallies up the score if clear(s) achieved"""
        lines_dropped = self.block.hard_drop_block()
        self._add_to_grid()
        clear_score = self.play_field.check_clear()
        if clear_score > 0:
            self.score += clear_score + lines_dropped + 1
        self.can_save = True
        self.can_use_saved = True

    def _new_block(self):
        """Next_block goes into play and new next block is iniciated.\n
        If new block has no place to spawn, game ends"""
        self.block = self.next_block
        if not self.block._check_placed_collision(self.block.shape):
            self.game_active = False
            pygame.time.set_timer(self.soft_drop_block, 0)
        self.next_block = Block(self)


game = Tetris()
game.run_game()
