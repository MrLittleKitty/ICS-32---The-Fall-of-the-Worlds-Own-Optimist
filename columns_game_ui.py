import columns_game as game
import pygame
import random

_ROWS = 13
_COLS = 6
_FPS = 12

_JEWELS = ['S', 'T', 'V', 'W', 'X', 'Y', 'Z']


def _get_jewel_color(jewel: str) -> (int, int, int):
    """
    Gets the color of a given jewel as a tuple
    :param jewel: The jewel to get the color of
    :return: A tuple where the first value is the Red, the second value is the Green, and the third value is the Blue.
    """
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
        """
        Constructs a new instance of the Game class and initializes all fields to their default values
        """
        self._state = game.GameState(_ROWS, _COLS)

        self._tick_counter = _FPS
        self._running = True

        # Black
        self._backgroundColor = pygame.Color(0, 0, 0)
        # Brown
        self._boxColor = pygame.Color(102, 51, 0)

        # We use 0.05 as the buffer around the top and bottom for the jewels
        self._jewelBufferY = 0.04
        self._jewelSize = (1.0 - self._jewelBufferY) / self._state.get_rows()
        self._jewelBufferX = (1.0 - (self._jewelSize * self._state.get_columns()))

    def start_game(self) -> None:
        """
        Starts the game loop and displays the game's graphics.
        """
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
        """
        Ticks the game's state (ticks matching, falling, etc.). Spawns a faller if one is not already on the board.
        """
        self._running = not self._state.tick()

        if not self._state.has_faller():
            contents = random.sample(_JEWELS, 3)
            column = random.randint(1, _COLS)
            self._state.spawn_faller(column, contents)

    def _create_surface(self, size: (int, int)) -> None:
        """
        Creates the surface that we will draw the game board on
        :param size: The size of the game board. A tuple where the 1st value is the width and the 2nd value is the height
        """
        self._surface = pygame.display.set_mode(size, pygame.RESIZABLE)

    def _handle_events(self) -> None:
        """
        Handles events from pygame by dispatching them to the correct method. This includes key press events.
        """
        for event in pygame.event.get():
            self._handle_event(event)

        self._handle_keys()

    def _handle_event(self, event: pygame.event.EventType) -> None:
        """
        Handles the pygame.QUIT event and the pygame.VIDEORESIZE event
        :param event: The event that we want to handle. Nothing will happen unless this is QUIT or VIDEORESIZE
        """
        if event.type == pygame.QUIT:
            self._stop_running()
        elif event.type == pygame.VIDEORESIZE:
            self._create_surface(event.size)

    def _handle_keys(self) -> None:
        """
        Handles key press events by taking the correct action based on the key that is pressed
        Fallers will be moved by handling the Left or Right arrow keys.
        Fallers will be rotated by handling the Spacebar.
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self._state.move_faller_side(game.LEFT)

        if keys[pygame.K_RIGHT]:
            self._state.move_faller_side(game.RIGHT)

        if keys[pygame.K_SPACE]:
            self._state.rotate_faller()

    def _stop_running(self) -> None:
        """
        Sets the game to stop running by changing the running state.
        The game will exit on the next frame after this is called.
        :return:
        """
        self._running = False

    def _draw_frame(self) -> None:
        """
        Draws a frame of the game. This draws every aspect of the current game state. (background, jewels, states, etc.)
        """
        self._surface.fill(self._backgroundColor)
        self._draw_game_objects()
        pygame.display.flip()

    def _draw_game_objects(self) -> None:
        """
        Draws all of the game objects and their states onto the drawing surface.
        This draws the game box in its given color and then draws each of the individual jewels
        :return:
        """
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
        """
        This draws a specified jewel and its current state onto the drawing surface.
        If the jewel is EMPTY then nothing will be drawn.
        If the jewel is in a cell that has been matched, the jewel will be drawn in WHITE.
        If the jewel is not in a matched cell then it will be drawn with its jewel-specific color.
        If the jewel is currently part of a faller that is about to freeze, it will be drawn with a WHITE outline.
        :param row: The row of the jewel to draw
        :param col: The column of the jewel to draw
        """
        jewel = self._state.get_cell_contents(row, col)
        if jewel is game.EMPTY:
            return

        rawColor = None
        state = self._state.get_cell_state(row, col)
        if state == game.MATCHED_CELL:
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

        if state == game.FALLER_STOPPED_CELL:
            pygame.draw.rect(self._surface, pygame.Color(255, 255, 255), rect, 2)

    def _frac_x_to_pixel_x(self, frac_x: float) -> int:
        """
        Converts a fractional x value to its corresponding x pixel value
        :param frac_x: The fractional location on the x axis. (0.0 - 1.0)
        :return: An int that is the pixel value on the x axis
        """
        return self._frac_to_pixel(frac_x, self._surface.get_width())

    def _frac_y_to_pixel_y(self, frac_y: float) -> int:
        """
        Converts a fractional y value to its corresponding y pixel value
        :param frac_y: The fractional location on the y axis. (0.0 - 1.0)
        :return: An int that is the pixel value on the y axis
        """
        return self._frac_to_pixel(frac_y, self._surface.get_height())

    def _frac_to_pixel(self, frac: float, max_pixel: int) -> int:
        """
        Converts a fractional value to an integer value from the given max pixel value
        :param frac: The fractional value to be converted to a pixel value (0.0 - 1.0)
        :param max_pixel: The max pixel range that the fractional value should be converted from
        :return: An int that is the pixel value corresponding to the given fractional value
        """
        return int(frac * max_pixel)


# This makes it so this module is executable
if __name__ == '__main__':
    Game().start_game()
