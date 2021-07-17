

from typing import List

from config import Config


def generate_board(width: int, height: int) -> List[List[str]]:
    board = [["" for _ in range(0, height)] for _ in range(0, width)]
    return board


class ConnectFour:
    def __init__(self):
        self.width = Config.width
        self.height = Config.height
        self.board = generate_board(self.width, self.height)
        self.requirements = Config.requirements

    def check_column(self, position: int):
        column = self.board[position]
        for i in range(0, len(column)):
            if not column[i]:
                return True
        return False

    def add_element(self, position: int, player: bool):
        column = self.board[position]
        for i in range(0, len(column)):
            if not column[i]:
                self.board[position][i] = Config.player_one if player else Config.player_two
                break

    def check_column_winner(self) -> bool:
        for column in self.board:
            string_column = "".join(column)
            if string_column.find(Config.player_one * self.requirements) >= 0 or string_column.find(
                    Config.player_two * self.requirements) >= 0:
                return True
        return False

    def check_row_winner(self) -> bool:
        for i in range(0, self.height):
            string_row = ""
            for column in self.board:
                string_row += column[i]
            if string_row.find(Config.player_one * self.requirements) >= 0 or string_row.find(
                    Config.player_two * self.requirements) >= 0:
                return True
        return False
