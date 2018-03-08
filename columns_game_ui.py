# Eric Wolfe 76946154 eawolfe@uci.edu
import columns_game as game
import pygame


def start_game() -> None:
    """
    The main entry point for the game. Starts the game.
    """
    rows = 13
    cols = 6
    state = game.GameState(rows, cols)
    pygame.init()

    surface = pygame.display.set_mode((700, 600))
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        surface.fill(pygame.Color(64, 64, 64))

        pygame.display.flip()

    pygame.quit()


# This makes it so this module is executable
if __name__ == '__main__':
    start_game()
