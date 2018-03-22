import columns_game as game


def start_game() -> None:
    """
    The main entry point for the game. Starts the game.
    """
    rows = get_int()
    cols = get_int()
    state = game.GameState(rows, cols)

    line = next_line()
    if line == 'CONTENTS':
        rowList = []
        for i in range(rows):
            row = []
            line = raw_next_line()
            for index in range(cols):
                row.append(line[index])
            rowList.append(row)
        state.set_board_contents(rowList)

    while True:
        _display_board(state)
        line = next_line()
        if line == 'Q':
            return
        if line == '':
            if state.tick():
                _display_board(state)
                break
        else:
            _process_command(line, state)
    print('GAME OVER')


def _process_command(command: str, state: game.GameState) -> None:
    """
    Processes a command that is read in from the console and then performs that action on the given GameState
    :param command: The command that will be performed
    :param state: The GameState that the given command will be performed on
    """
    if command == 'R':
        state.rotate_faller()
    elif command == '<':
        state.move_faller_side(game.LEFT)
    elif command == '>':
        state.move_faller_side(game.RIGHT)
    elif command[0] == 'F':
        try:
            args = command.split(' ')
            columnNumber = int(args[1])
            faller = [args[4], args[3], args[2]]
            state.spawn_faller(columnNumber, faller)
        except:
            return


def _display_board(state: game.GameState) -> None:
    """
    Displays the board of the given GameState in the console
    :param state: The GameState that will be displayed in the console
    """
    for row in range(state.get_rows()):
        rowString = "|"
        for col in range(state.get_columns()):
            cellValue = state.get_cell_contents(row, col)
            cellState = state.get_cell_state(row, col)
            if cellState == game.EMPTY_CELL:
                rowString += '   '
            elif cellState == game.OCCUPIED_CELL:
                rowString += (' ' + cellValue + ' ')
            elif cellState == game.FALLER_MOVING_CELL:
                rowString += ('[' + cellValue + ']')
            elif cellState == game.FALLER_STOPPED_CELL:
                rowString += ('|' + cellValue + '|')
            elif cellState == game.MATCHED_CELL:
                rowString += ('*' + cellValue + '*')
        rowString += '|'
        print(rowString)
    finalLine = ' '
    for col in range(state.get_columns()):
        finalLine += '---'
    finalLine += ' '
    print(finalLine)


def get_int() -> int:
    """
    Gets a lone integer from the console (the integer is on its own line)
    :return: The int value that was read in from the console
    """
    line = input().strip()
    return int(line)


def next_line() -> str:
    """
    Gets a line from the console and returns it with the leading/trailing whitespace stripped
    :return: The line that was retrieved from the console
    """
    return input().strip()


def raw_next_line() -> str:
    """
    Gets a completely raw line from the console
    :return: The line that was retrieved from the console
    """
    return input()


# This makes it so this module is executable
if __name__ == '__main__':
    start_game()
