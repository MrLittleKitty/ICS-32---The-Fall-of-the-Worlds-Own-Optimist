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
        if self.faller.active:
            # If the faller had stopped last tick then check if it is still on solid ground
            if self.faller.state == FALLER_STOPPED:
                # If the faller is on solid ground then finalize it
                if self._is_solid(self.faller.get_row() + 1, self.faller.get_col()):
                    # If the top of the faller is out of bounds the game ends
                    if self.faller.get_row() - 2 < 0:
                        return True
                    # If all of the faller is in play then we solidify it
                    for i in range(3):
                        self._set_cell(self.faller.get_row()-i,self.faller.get_col(),self.faller.contents[i],OCCUPIED_CELL)
                    self.faller.active = False
                else:
                    self.faller.state = FALLER_MOVING
            else: # Faller is still moving



        # Match gems after that
        return False

    def spawn_faller(self, column: int, faller: [str, str, str]) -> None:
        if self.faller.active:
            return

        self.faller.active = True
        self.faller.contents = faller
        self.faller.set_row(0)
        self.faller.set_col(column - 1)
        self._set_cell(0, self.faller.get_col(), self.faller.contents[0], FALLER_MOVING_CELL)

    def rotate_faller(self) -> None:
        return

    def move_faller(self, direction: int) -> None:
        if not self.faller.active:
            return

        if not direction == RIGHT and not direction == LEFT:
            return

        targetColumn = self.faller.get_col() + direction
        # Here we are going to check if we can move the faller
        for row in range(self.faller.get_row(), self.faller.get_row() - 2):
            # If the check is going to check a row that is above the top, then we are clear to move the faller
            if row <= 0:
                break

            if self.get_cell_state(row, targetColumn) == OCCUPIED_CELL:
                return

        # If we get to here then it is ok to move the faller
        self.faller.set_col(targetColumn)
        for row in range(self.faller.get_row(), self.faller.get_row() - 2):
            # If we are going to go out of bounds then we are done moving
            if row <= 0:
                break

    def _set_cell(self, row: int, col: int, contents: str, state: str) -> None:
        self.boardRows[row][col] = contents
        self.boardStates[row][col] = state

    def get_cell_state(self, row: int, col: int) -> str:
        return self.boardStates[row][col]

    def get_cell_contents(self, row: int, col: int) -> str:
        return self.boardRows[row][col]

    def _is_solid(self, row: int, col: int) -> bool:
        # If the target is below the bottom row than it is solid
        if row >= self.get_columns():
            return True

        if self.get_cell_state(row, col) == OCCUPIED_CELL:
            return True

        return False

    def _move_faller_down(self) -> None:
        # If the faller cant move down then return
        if self._is_solid(self.faller.get_row() + 1, self.faller.get_col()):
            return

        # Move the bottom of the faller down
        self._move_cell(self.faller.get_row(), self.faller.get_col(), DOWN)
        # If the middle of the faller is in play then move it down
        if self.faller.get_row() - 1 >= 0:
            self._move_cell(self.faller.get_row() - 1, self.faller.get_col(), DOWN)
            # If the top of the faller is in play then move it down
            if self.faller.get_row() - 2 >= 0:
                self._move_cell(self.faller.get_row() - 2, self.faller.get_col(), DOWN)
            else:  # If the top of the faller wasnt in play then we set its location to be where the middle was
                self._set_cell(self.faller.get_row() - 1, self.faller.get_col(), self.faller.contents[2],
                               FALLER_MOVING_CELL)
        else:  # If the middle wasnt in play then spawn it where the fallers location was
            self._set_cell(self.faller.get_row(), self.faller.get_col(), self.faller.contents[1], FALLER_MOVING_CELL)

        self.faller.set_row(self.faller.get_row() + 1)

    def _move_cell(self, row: int, col: int, direction: int) -> None:
        oldValue = self.boardRows[row][col]
        oldState = self.boardStates[row][col]

        self.boardRows[row][col] = EMPTY
        self.boardStates[row][col] = EMPTY_CELL

        if direction == DOWN:
            targetRow = row + 1
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
        self.row = 0
        self.col = 0
        self.contents = [EMPTY, EMPTY, EMPTY]
        self.state = FALLER_MOVING

    def get_row(self) -> int:
        return self.row

    def get_col(self) -> int:
        return self.col

    def set_row(self, row: int) -> None:
        self.row = row

    def set_col(self, col: int) -> None:
        self.col = col
