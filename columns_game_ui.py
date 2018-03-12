# Eric Wolfe 76946154 eawolfe@uci.edu
import columns_game as game
import pygame
import random

_ROWS = 13
_COLS = 6
_FPS = 30

_JEWELS = ['S', 'Y', 'V', 'W', 'X', 'Y', 'Z']


class Game:

    def __init__(self):
        self._state = game.GameState(_ROWS, _COLS)
        self._tick_counter = _FPS
        self._running = True

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
            column = random.randint(1, _ROWS)
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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self._bark()

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
        self._surface.fill(pygame.Color(255, 255, 255))
        self._draw_game()
        pygame.display.flip()

    def _draw_game(self) -> None:
        tl_frac_x, tl_frac_y = self._state.player().top_left()
        width_frac = self._state.player().width()
        height_frac = self._state.player().height()

        tl_pixel_x = self._frac_x_to_pixel_x(tl_frac_x)
        tl_pixel_y = self._frac_y_to_pixel_y(tl_frac_y)
        width_pixel = self._frac_x_to_pixel_x(width_frac)
        height_pixel = self._frac_y_to_pixel_y(height_frac)

        player_rect = pygame.Rect(tl_pixel_x, tl_pixel_y, width_pixel, height_pixel)

        #        pygame.draw.rect(self._surface, pygame.Color(0, 0, 128), player_rect)

        self._surface.blit(
            pygame.transform.scale(
                self._player_image, (width_pixel, height_pixel)),
            (tl_pixel_x, tl_pixel_y))

    def _frac_x_to_pixel_x(self, frac_x: float) -> int:
        return self._frac_to_pixel(frac_x, self._surface.get_width())

    def _frac_y_to_pixel_y(self, frac_y: float) -> int:
        return self._frac_to_pixel(frac_y, self._surface.get_height())

    def _frac_to_pixel(self, frac: float, max_pixel: int) -> int:
        return int(frac * max_pixel)


# This makes it so this module is executable
if __name__ == '__main__':
    Game().start_game()
