# Eric Wolfe 76946154 eawolfe@uci.edu

LEFT = -1
RIGHT = 1

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
        for i in range(rows):
            row = []
            for j in range(columns):
                row.append(EMPTY)
            self.boardRows.append(row)

    def set_board_contents(self, contents: [[str]]) -> None:
        return

    def get_rows(self) -> int:
        return self.rows

    def get_columns(self) -> int:
        return self.columns

    def tick(self) -> None:
        return

    def spawn_faller(self):
        return

    def rotate_faller(self):
        return

    def move_faller(self, direction: int):
        return

    def game_over(self) -> bool:
        return