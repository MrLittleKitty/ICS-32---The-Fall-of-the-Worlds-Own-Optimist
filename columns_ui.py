# Eric Wolfe 76946154 eawolfe@uci.edu
import game_state as game


def start_game() -> None:
    rows = get_int()
    cols = get_int()
    state = game.GameState(rows, cols)

    line = next_line()
    if line == 'CONTENTS':
        rowList = []
        for i in range(rows):
            row = []
            line = next_line()
            for index in range(cols):
                row.append(line[i])
            rowList.append(row)
        state.set_board_contents(rowList)

    while not state.game_over():
        display_board(state)
        line = next_line()
        if line == 'Q':
            return
    print('GAME OVER')


def process_command(command: str, state: game.GameState) -> None:
    if command == '':
        state.tick()
    elif command == 'R':
        state.rotate_faller()
    elif command == '<':
        state.move_faller(game.LEFT)
    elif command == '>':
        state.move_faller(game.RIGHT)


def display_board(state: game.GameState) -> None:
    return


def get_int() -> int:
    line = input().strip()
    return int(line)


def next_line() -> str:
    return input().strip()


if __name__ == '__main__':
    start_game()
