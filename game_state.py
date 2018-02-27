# Eric Wolfe 76946154 eawolfe@uci.edu
class GameState:
    def __init__(self, rows: int, columns: int) -> None:
        super().__init__()
        self.rows = rows
        self.columns = columns

    def get_rows(self) -> int:
        return self.rows

    def get_columns(self) -> int:
        return self.columns

    def tick(self) -> None:
        return
