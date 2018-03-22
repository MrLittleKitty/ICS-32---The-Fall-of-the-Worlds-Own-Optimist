# State of a cell
EMPTY_CELL = 'EMPTY STATE'
FALLER_MOVING_CELL = 'FALLER_MOVING STATE'
FALLER_STOPPED_CELL = 'FALLER_STOPPED STATE'
OCCUPIED_CELL = 'OCCUPIED STATE'
MATCHED_CELL = 'MATCHED STATE'


# Helper method to tell if a cell is in a state that can be matched with other cells
def _is_matchable_state(state: str) -> bool:
    """
    Tells if the given state is a state that can be matched
    :param state: The state that will be checked
    :return: True if that given state can be matched. False otherwise
    """
    return state == OCCUPIED_CELL or state == MATCHED_CELL


# Directions
LEFT = -1
RIGHT = 1
_DOWN = 0
_DOWN_LEFT = 2

# Contents of a cell (the type of jewel or empty)
_NONE = 'NONE'
EMPTY = ' '
S = 'S'
T = 'T'
V = 'V'
W = 'W'
X = 'X'
Y = 'Y'
Z = 'Z'


class GameState:
    def __init__(self, rows: int, columns: int):
        """
        Constructs a new GameState with a board that is the given rows x the given columns
        :param rows: The number of rows that board will have
        :param columns: The number of columns that the board will have
        """
        super().__init__()
        self._rows = rows
        self._columns = columns
        self._boardRows = []
        self._boardStates = []
        self._faller = _Faller()
        for i in range(rows):
            row = []
            stateRow = []
            for j in range(columns):
                row.append(EMPTY)
                stateRow.append(EMPTY_CELL)
            self._boardRows.append(row)
            self._boardStates.append(stateRow)

    def set_board_contents(self, contents: [[str]]) -> None:
        """
        Sets the contents of the board to the given contents, then applies gravity and attempts matching
        :param contents: A list of rows from top of the board to bottom where each row is a list that represents each cell in that row
        """
        for row in range(self.get_rows()):
            for col in range(self.get_columns()):
                value = contents[row][col]
                if value is EMPTY:
                    self._set_cell(row, col, EMPTY, EMPTY_CELL)
                else:
                    self._set_cell(row, col, value, OCCUPIED_CELL)

        self._gem_gravity()
        self._matching()

    def tick(self) -> bool:
        """
        Ticks one time unit on the game. This causes fallers to move down and/or matching to occur
        :return: True if the game is over from a faller freezing out of bounds. False otherwise
        """
        # Handle the faller first
        if self._faller.active:
            # If the faller had stopped last tick then check if it is still on solid ground
            if self._faller.state == _FALLER_STOPPED:
                # Do an update on the faller state to see what state it is now in
                self._update_faller_state()
                # If the faller is still stopped after the update then solidify it
                if self._faller.state == _FALLER_STOPPED:
                    # Set a value for is part of this faller is solidified above the top of the game board
                    value = False
                    # If part of the faller is above the top of the game board then set the value to true
                    if self._faller.get_row() - 2 < 0:
                        value = True

                    # If all of the faller is in play then we solidify it
                    for i in range(3):
                        self._set_cell(self._faller.get_row() - i, self._faller.get_col(), self._faller.contents[i],
                                       OCCUPIED_CELL)
                    self._faller.active = False

                    # The game ends if part of this faller was solidified above the top of the game board
                    self._matching()
                    return value

            # If we get here then the faller isnt on solid ground for sure so move it down
            self._move_faller_down()
            # Update the faller now so it is in the correct state
            self._update_faller_state()

        # Handle matching and gem gravity
        self._matching()
        return False

    def spawn_faller(self, column: int, faller: [str, str, str]) -> None:
        """
        Spawns a faller in the given column (1,n) with the given contents
        :param column: A column number from 1 to the number of columns where the faller will spawn
        :param faller: The contents of the faller that will spawn. faller[0] is the first block of the faller to be visible
        """
        if self._faller.active:
            return

        self._faller.active = True
        self._faller.contents = faller
        self._faller.set_row(0)
        self._faller.set_col(column - 1)
        self._set_cell(0, self._faller.get_col(), self._faller.contents[0], FALLER_MOVING_CELL)

        # Check if the ground immediately under the faller is solid and if it is then update the fallers state
        self._update_faller_state()

    def has_faller(self) -> bool:
        """
        Returns whether or not this game state has a faller that is currently active (falling or stopped but not frozen)
        :return: True if there is an active faller on the game board. False otherwise
        """
        return self._faller.active

    def rotate_faller(self) -> None:
        """
        Rotates the faller so the first block becomes the last, the middle becomes the first, and the top becomes the middle
        """
        # Only works if there is an active faller
        if not self._faller.active:
            return

        one = self._faller.contents[0]
        two = self._faller.contents[1]
        three = self._faller.contents[2]

        self._faller.contents = [two, three, one]
        for i in range(3):
            self._set_cell_contents(self._faller.get_row() - i, self._faller.get_col(), self._faller.contents[i])
        self._update_faller_state()

    def move_faller_side(self, direction: int) -> None:
        """
        Moves the faller in the given direction if that direction is not blocked
        :param direction: The direction (LEFT or RIGHT) to move the faller in
        """
        # Only works if there is an active faller
        if not self._faller.active:
            return

        # They can only move left and right from this method
        if not direction == RIGHT and not direction == LEFT:
            return

        # They can't move passed the leftmost or rightmost column
        if (direction == LEFT and self._faller.get_col() == 0) or (
                direction == RIGHT and self._faller.get_col() == self.get_columns() - 1):
            return

        targetColumn = self._faller.get_col() + direction
        # Here we are going to check if we can move the faller
        for i in range(3):
            # If the check is going to check a row that is above the top, then we are clear to move the faller
            if self._faller.get_row() - i < 0:
                break

            if self.get_cell_state(self._faller.get_row() - i, targetColumn) == OCCUPIED_CELL:
                return

        # Move the faller to its new column
        for i in range(3):
            # If we are going to go out of bounds then we are done moving
            if self._faller.get_row() - i < 0:
                break
            # Move the cell to the new column
            self._move_cell(self._faller.get_row() - i, self._faller.get_col(), direction)

        # Set the new faller column
        self._faller.set_col(targetColumn)

        # Update the fallers state now that it has moved
        self._update_faller_state()

    def get_rows(self) -> int:
        """
        Gets the number of rows in this game board
        :return: An int that represents the number of rows in this game board
        """
        return self._rows

    def get_columns(self) -> int:
        """
        Gets the number of columns in this game board
        :return: An int that represents the number of columns in this game board
        """
        return self._columns

    def get_cell_state(self, row: int, col: int) -> str:
        """
        Gets the state of the cell identified by the given row and column
        :param row: The row of the cell to get the state for
        :param col: The column of the cell to get the state for
        :return: The state of the cell identified by the given row and column
        """
        return self._boardStates[row][col]

    def get_cell_contents(self, row: int, col: int) -> str:
        """
        Gets the content of the cell identified by the given row and column
        :param row: The row of the cell to get the content for
        :param col: The column of the cell to get the content for
        :return: The content of the cell identified by the given row and column
        """
        return self._boardRows[row][col]

    def _set_cell(self, row: int, col: int, contents: str, state: str) -> None:
        """
        Sets the content and state of the cell identified by the given row and column
        :param row: The row of the cell
        :param col: The column of the cell
        :param contents: The content to set the cell to
        :param state: The state to set the cell to
        """
        # Not allowed to set cells that fall above the board
        if row < 0:
            return
        self._set_cell_contents(row, col, contents)
        self._set_cell_state(row, col, state)

    def _set_cell_contents(self, row: int, col: int, contents: str) -> None:
        """
        Sets the content of the cell identified by the given row and column
        :param row: The row of the cell
        :param col: The column of the cell
        :param contents: The content to set the cell to
        """
        if row < 0:
            return
        self._boardRows[row][col] = contents

    def _set_cell_state(self, row: int, col: int, state: str) -> None:
        """
        Sets the state of the cell identified by the given row and column
        :param row: The row of the cell
        :param col: The column of the cell
        :param state: The state to set the cell to
        """
        if row < 0:
            return
        self._boardStates[row][col] = state

    def _gem_gravity(self) -> None:
        """
        Applies gem gravity to all frozen cells and moves them until the cell below them is solid
        """
        for col in range(self.get_columns()):
            for row in range(self.get_rows() - 1, -1, -1):
                state = self.get_cell_state(row, col)
                # Ignore the crawler when propagating gravity
                if state == FALLER_MOVING_CELL or state == FALLER_STOPPED_CELL:
                    continue
                if state == OCCUPIED_CELL:
                    i = 1
                    while not self._is_solid(row + i, col):
                        self._move_cell(row + i - 1, col, _DOWN)
                        i += 1

    def _matching(self) -> None:
        """
        Ticks the matching state on all cell.
        If cells are already marked as matching then they are destroyed and gravity is applied to all cells.
        After that all cells are compared for matching on the X, Y, and diagonal axes.
        """
        # First thing we do is get rid of any cells that are marked as matched from the previous tick
        for row in range(self.get_rows()):
            for col in range(self.get_columns()):
                if self.get_cell_state(row, col) == MATCHED_CELL:
                    self._set_cell(row, col, EMPTY, EMPTY_CELL)
        # Then we propagate gravity so everything moves down again
        self._gem_gravity()

        # Now we go through all the cells and flag all the matching ones
        # We start at the bottom left corner and move up and to the right while always looking for matches up and right
        #   so this way we never need to worry about looking in all directions. This is because any cell to the left
        #   and down will already have been checked because we moved from that cell
        self._match_x_axis()
        self._match_y_axis()
        self._match_diagonal()

    def _match_x_axis(self) -> None:
        """
        Attempts matching for all cells on the X-axis and then marks any of the cells that match (3 or more occurrences)
        """
        for currentRow in range(self.get_rows() - 1, -1, -1):
            matches = 0
            gem = _NONE
            for col in range(0, self.get_columns()):
                contents = self.get_cell_contents(currentRow, col)
                state = self.get_cell_state(currentRow, col)
                cellMatches = (contents == gem and _is_matchable_state(state))
                # This cell matches our current sequence
                if cellMatches:
                    matches += 1

                # This is the last column so we have to terminate the matching for this row
                if col == self.get_columns()-1:
                    if matches >= 3:
                        if cellMatches:
                            self._mark_matched_cells(currentRow, col, LEFT, matches)
                        else:
                            self._mark_matched_cells(currentRow, col-1, LEFT, matches)
                elif not cellMatches:
                    if matches >= 3:
                        self._mark_matched_cells(currentRow, col-1, LEFT, matches)

                    if _is_matchable_state(state):
                        gem = contents
                        matches = 1
                    else:
                        gem = _NONE
                        matches = 1

    def _match_y_axis(self) -> None:
        """
        Attempts matching for all cells on the Y-axis and then marks any of the cells that match (3 or more occurrences)
        """
        for currentCol in range(0, self.get_columns()):
            matches = 0
            gem = _NONE
            for row in range(self.get_rows() - 1, -1, -1):
                contents = self.get_cell_contents(row, currentCol)
                state = self.get_cell_state(row, currentCol)
                cellMatches = (contents == gem and _is_matchable_state(state))
                # This cell matches our current sequence
                if cellMatches:
                    matches += 1

                # This is the last column so we have to terminate the matching for this row
                if row == 0:
                    if matches >= 3:
                        if cellMatches:
                            self._mark_matched_cells(row, currentCol, _DOWN, matches)
                        else:
                            self._mark_matched_cells(row + 1, currentCol, _DOWN, matches)
                elif not cellMatches:
                    if matches >= 3:
                        self._mark_matched_cells(row + 1, currentCol, _DOWN, matches)

                    if _is_matchable_state(state):
                        gem = contents
                        matches = 1
                    else:
                        gem = _NONE
                        matches = 1

    def _match_diagonal(self) -> None:
        """
        Attempts matching for all cells on the diagonal-axis and then marks any of the cells that match (3 or more occurrences)
        """
        for currentRow in range(self.get_rows() - 1, -1, -1):
            for currentCol in range(0, self.get_columns()):
                matches = 0
                gem = _NONE
                rowCounter = 0
                colCounter = 0
                while True:
                    row = currentRow-rowCounter
                    col = currentCol+colCounter

                    contents = self.get_cell_contents(row, col)
                    state = self.get_cell_state(row, col)
                    cellMatches = (contents == gem and _is_matchable_state(state))
                    # This cell matches our current sequence
                    if cellMatches:
                        matches += 1

                    # This is the last column so we have to terminate the matching for this row
                    if col == self.get_columns()-1 or row == 0:
                        if matches >= 3:
                            if cellMatches:
                                self._mark_matched_cells(row, col, _DOWN_LEFT, matches)
                            else:
                                self._mark_matched_cells(row + 1, col - 1, _DOWN_LEFT, matches)
                    elif not cellMatches:
                        if matches >= 3:
                            self._mark_matched_cells(row + 1, col - 1, _DOWN_LEFT, matches)

                        if _is_matchable_state(state):
                            gem = contents
                            matches = 1
                        else:
                            gem = _NONE
                            matches = 1

                    rowCounter += 1
                    colCounter += 1

                    if currentRow-rowCounter < 0 or currentCol+colCounter >= self.get_columns():
                        break

    def _mark_matched_cells(self, row: int, col: int, direction: int, amount: int) -> None:
        """
        Marks the given number of cells in the given direction as matching cells
        :param row: The row of the starting cell
        :param col: The column of the starting cell
        :param direction: The direction to mark cells in
        :param amount: The amount of cells (start cell included) to mark as matching
        """
        if direction == LEFT:
            for targetCol in range(col, col - amount, -1):
                self._set_cell_state(row, targetCol, MATCHED_CELL)
        elif direction == _DOWN:
            for targetRow in range(row, row + amount):
                self._set_cell_state(targetRow, col, MATCHED_CELL)
        elif direction == _DOWN_LEFT:
            for i in range(amount):
                self._set_cell_state(row + i, col - i, MATCHED_CELL)

    def _update_faller_state(self) -> None:
        """
        Updates the state of the faller according to its current conditions.
        If the faller has ground below it then the state is set to FALLER_STOPPED.
        Otherwise the state is set to FALLER_MOVING.
        The cells of the faller on the board are updated accordingly.
        """
        state = None
        targetRow = self._faller.get_row() + 1
        if self._is_solid(targetRow, self._faller.get_col()):
            state = FALLER_STOPPED_CELL
            self._faller.state = _FALLER_STOPPED
        else:
            state = FALLER_MOVING_CELL
            self._faller.state = _FALLER_MOVING

        for i in range(3):
            row = self._faller.get_row() - i
            if row < 0:
                return
            self._set_cell(row, self._faller.get_col(), self._faller.contents[i], state)

    def _is_solid(self, row: int, col: int) -> bool:
        """
        Checks if the the cell of the given row and column is solid (a solid block or the bottom row)
        :param row: The row of the cell to check
        :param col: The column of the cell the check
        :return: True if the given cell is solid. False otherwise
        """
        # If the target is below the bottom row than it is solid
        if row >= self.get_rows():
            return True

        if self.get_cell_state(row, col) == OCCUPIED_CELL:
            return True

        return False

    def _move_faller_down(self) -> None:
        """
        Moves the faller down one space and updates all the necessary information
        """
        # If the faller cant move down then return
        if self._is_solid(self._faller.get_row() + 1, self._faller.get_col()):
            return

        # Move the bottom of the faller down
        self._move_cell(self._faller.get_row(), self._faller.get_col(), _DOWN)
        # If the middle of the faller is in play then move it down
        if self._faller.get_row() - 1 >= 0:
            self._move_cell(self._faller.get_row() - 1, self._faller.get_col(), _DOWN)
            # If the top of the faller is in play then move it down
            if self._faller.get_row() - 2 >= 0:
                self._move_cell(self._faller.get_row() - 2, self._faller.get_col(), _DOWN)
            else:  # If the top of the faller wasnt in play then we set its location to be where the middle was
                self._set_cell(self._faller.get_row() - 1, self._faller.get_col(), self._faller.contents[2],
                               FALLER_MOVING_CELL)
        else:  # If the middle wasnt in play then spawn it where the fallers location was
            self._set_cell(self._faller.get_row(), self._faller.get_col(), self._faller.contents[1], FALLER_MOVING_CELL)

        self._faller.set_row(self._faller.get_row() + 1)

    def _move_cell(self, row: int, col: int, direction: int) -> None:
        """
        Moves the given cell in the given direction
        :param row: The row of the cell to move
        :param col: The column of the cell to move
        :param direction: The direction to move the cell in (LEFT, RIGHT, DOWN)
        """
        oldValue = self._boardRows[row][col]
        oldState = self._boardStates[row][col]

        self._boardRows[row][col] = EMPTY
        self._boardStates[row][col] = EMPTY_CELL

        if direction == _DOWN:
            targetRow = row + 1
            self._boardRows[targetRow][col] = oldValue
            self._boardStates[targetRow][col] = oldState
        else:
            targetCol = col + direction
            self._boardRows[row][targetCol] = oldValue
            self._boardStates[row][targetCol] = oldState


_FALLER_STOPPED = 0
_FALLER_MOVING = 1


class _Faller:
    def __init__(self):
        """
        Constructs a new faller object and initializes all the values
        """
        self.active = False
        self._row = 0
        self._col = 0
        self.contents = [EMPTY, EMPTY, EMPTY]
        self.state = _FALLER_MOVING

    def get_row(self) -> int:
        """
        Gets the row value for this faller
        :return: An int that represents the row value
        """
        return self._row

    def get_col(self) -> int:
        """
        Gets the column value for this faller
        :return: An int that represents the column value
        """
        return self._col

    def set_row(self, row: int) -> None:
        """
        Sets the row value for this faller
        :param row: The row value that this faller will be set to
        """
        self._row = row

    def set_col(self, col: int) -> None:
        """
        Sets the column value for this faller
        :param col: The column value that this faller will be set to
        """
        self._col = col
