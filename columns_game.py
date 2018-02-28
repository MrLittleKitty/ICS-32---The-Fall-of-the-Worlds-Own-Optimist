# Eric Wolfe 76946154 eawolfe@uci.edu

# State of a cell
EMPTY_CELL = ' '
FALLER_MOVING_CELL = '['
FALLER_STOPPED_CELL = '|'
OCCUPIED_CELL = 'X'
MATCHED_CELL = '*'

# Directions
LEFT = -1
RIGHT = 1
DOWN = 0

# Contents of a cell
EMPTY = ' '
S = 'S'
T = 'Y'
V = 'V'
W = 'W'
X = 'X'
Y = 'Y'
Z = 'Z'


class GameState:
    def __init__(self, rows: int, columns: int) -> None:
        super().__init__()
        self.rows = rows
        self.columns = columns
        self.boardRows = []
        self.boardStates = []
        self.faller = Faller()
        for i in range(rows):
            row = []
            stateRow = []
            for j in range(columns):
                row.append(EMPTY)
                stateRow.append(EMPTY_CELL)
            self.boardRows.append(row)
            self.boardStates.append(stateRow)

    def set_board_contents(self, contents: [[str]]) -> None:
        return

    def get_rows(self) -> int:
        return self.rows

    def get_columns(self) -> int:
        return self.columns

    def tick(self) -> bool:
        # Handle the faller first

        # Freeze the faller if necessary

        # Match gems after that
        return False

    def spawn_faller(self, column: int, faller: [str, str, str]) -> None:
        if self.faller.active:
            return

        self.faller.active = True
        self.faller.contents = faller
        self.faller.location = (0, column - 1)
        self.boardRows[0][self.faller.location[1]] = self.faller.contents[0]
        self.boardStates[0][self.faller.location[1]] = FALLER_MOVING_CELL

    def rotate_faller(self) -> None:
        return

    def move_faller(self, direction: int) -> None:
        if not self.faller.active:
            return

        targetColumn = self.faller.location[1] + direction
        # Here we are going to check if we can move the faller
        for row in range(self.faller.location[0], self.faller.location[0] - 2):
            # If the check is going to check a row that is above the top, then we are clear to move the faller
            if row <= 0:
                break

            if self.get_cell_state(row, targetColumn) == OCCUPIED_CELL:
                return

        # If we get to here then it is ok to move the faller
        self.faller.location[1] = targetColumn
        for row in range(self.faller.location[0], self.faller.location[0] - 2):
            # If we are going to go out of bounds then we are done moving
            if row <= 0:
                break

    def _set_cell(self, row: int, col: int, contents: str) -> None:
        self.boardRows[row][col] = contents

    def get_cell_state(self, row: int, col: int) -> str:
        return self.boardStates[row][col]

    def get_cell_contents(self, row: int, col: int) -> str:
        return self.boardRows[row][col]

    def _move_cell(self, row: int, col: int, direction: int) -> None:
        oldValue = self.boardRows[row][col]
        oldState = self.boardStates[row][col]

        self.boardRows[row][col] = EMPTY
        self.boardStates[row][col] = EMPTY_CELL

        if direction == DOWN:
            targetRow = row - 1
            self.boardRows[targetRow][col] = oldValue
            self.boardStates[targetRow][col] = oldState
        else:
            targetCol = row + direction
            self.boardRows[row][targetCol] = oldValue
            self.boardStates[row][targetCol] = oldState


FALLER_STOPPED = 0
FALLER_MOVING = 1


class Faller:
    def __init__(self) -> None:
        self.active = False
        self.location = [0, 0]  # Row, Column
        self.contents = [EMPTY, EMPTY, EMPTY]
        self.state = FALLER_MOVING
