# Eric Wolfe 76946154 eawolfe@uci.edu
import columns_game as game
import pygame
import random

_ROWS = 13
_COLS = 6
_FPS = 12

_JEWELS = ['S', 'T', 'V', 'W', 'X', 'Y', 'Z']


def _get_jewel_color(jewel: str) -> (int, int, int):
    if jewel == 'S':  # Red
        return (255, 0, 0)
    elif jewel == 'T':  # Green
        return (0, 255, 0)
    elif jewel == 'V':  # Blue
        return (0, 0, 255)
    elif jewel == 'W':  # Yellow
        return (255, 255, 0)
    elif jewel == 'X':  # Orange
        return (255, 128, 0)
    elif jewel == 'Y':  # Purple
        return (102, 0, 204)
    elif jewel == 'Z':  # Teal
        return (51, 255, 255)


class Game:

    def __init__(self):
        self._state = game.GameState(_ROWS, _COLS)

        self._tick_counter = _FPS
        self._running = True

        self._backgroundColor = pygame.Color(0, 0, 0)
        self._boxColor = pygame.Color(102, 51, 0)

        # We use 0.05 as the buffer around the top and bottom for the jewels
        self._jewelBufferY = 0.05
        self._jewelSize = (1.0 - self._jewelBufferY) / self._state.get_rows()
        self._jewelBufferX = (1.0 - (self._jewelSize * self._state.get_columns()))

    def start_game(self) -> None:
        pygame.init()

        try:
            clock = pygame.time.Clock()

            self._create_surface((600, 600))

            while self._running:
                clock.tick(_FPS)

                self._handle_events()

                self._tick_counter -= 1

                if self._tick_counter == 0:
                    self._tick_game()
                    self._tick_counter = _FPS

                self._draw_frame()

        finally:
            pygame.quit()

    def _tick_game(self) -> None:
        self._running = not self._state.tick()

        if not self._state.has_faller():
            contents = random.sample(_JEWELS, 3)
            column = random.randint(1, _COLS)
            self._state.spawn_faller(column, contents)

    def _create_surface(self, size: (int, int)) -> None:
        self._surface = pygame.display.set_mode(size, pygame.RESIZABLE)

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            self._handle_event(event)

        self._handle_keys()

    def _handle_event(self, event) -> None:
        if event.type == pygame.QUIT:
            self._stop_running()
        elif event.type == pygame.VIDEORESIZE:
            self._create_surface(event.size)

    def _handle_keys(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self._state.move_faller_side(game.LEFT)

        if keys[pygame.K_RIGHT]:
            self._state.move_faller_side(game.RIGHT)

        if keys[pygame.K_SPACE]:
            self._state.rotate_faller()

    def _stop_running(self) -> None:
        self._running = False

    def _draw_frame(self) -> None:
        self._surface.fill(self._backgroundColor)
        self._draw_game()
        pygame.display.flip()

    def _draw_game(self) -> None:

        # buffer = 0.003
        # topLeftX = self._frac_x_to_pixel_x((self._jewelBufferX / 2) - buffer)
        # topLeftY = self._frac_y_to_pixel_y((self._jewelBufferY / 2) - buffer)
        #
        # width = self._frac_x_to_pixel_x((self._jewelSize * self._state.get_columns()) + (buffer * 2) - 0.002)
        # height = self._frac_y_to_pixel_y((self._jewelSize * self._state.get_rows()) + buffer * 2 - 0.002)

        topLeftX = self._frac_x_to_pixel_x((self._jewelBufferX / 2))
        topLeftY = self._frac_y_to_pixel_y((self._jewelBufferY / 2))

        width = self._frac_x_to_pixel_x((self._jewelSize * self._state.get_columns()) - 0.001)
        height = self._frac_y_to_pixel_y((self._jewelSize * self._state.get_rows()))

        # Draw the outline box for the game
        outlineRect = pygame.Rect(topLeftX, topLeftY, width, height)
        pygame.draw.rect(self._surface, self._boxColor, outlineRect, 0)

        # Draw each of the individual jewels
        for row in range(self._state.get_rows()):
            for col in range(self._state.get_columns()):
                self._draw_jewel(row, col)

    def _draw_jewel(self, row: int, col: int) -> None:
        jewel = self._state.get_cell_contents(row, col)
        if jewel is game.EMPTY:
            return

        rawColor = None
        if self._state.get_cell_state(row, col) == game.MATCHED_CELL:
            rawColor = (255, 255, 255)
        else:
            rawColor = _get_jewel_color(jewel)
        color = pygame.Color(rawColor[0], rawColor[1], rawColor[2])

        jewelX = (col * self._jewelSize) + (self._jewelBufferX / 2)
        jewelY = (row * self._jewelSize) + (self._jewelBufferY / 2)

        topLeftX = self._frac_x_to_pixel_x(jewelX)
        topLeftY = self._frac_y_to_pixel_y(jewelY)

        width = self._frac_x_to_pixel_x(self._jewelSize)
        height = self._frac_y_to_pixel_y(self._jewelSize)

        rect = pygame.Rect(topLeftX, topLeftY, width, height)

        pygame.draw.rect(self._surface, color, rect, 0)

    def _frac_x_to_pixel_x(self, frac_x: float) -> int:
        return self._frac_to_pixel(frac_x, self._surface.get_width())

    def _frac_y_to_pixel_y(self, frac_y: float) -> int:
        return self._frac_to_pixel(frac_y, self._surface.get_height())

    def _frac_to_pixel(self, frac: float, max_pixel: int) -> int:
        return int(frac * max_pixel)


# This makes it so this module is executable
if __name__ == '__main__':
    Game().start_game()
