

from typing import List, Union

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

    def reset_board(self):
        self.board = generate_board(self.width, self.height)

    def print_board(self):
        for i in range(0, self.height):
            row = "" if i != 0 else "\n"
            for column in self.board:
                row += column[-1-i] if column[-1-i] else Config.blank
            print(row)

    def add_element(self, position: int, player: bool):
        column = self.board[position]
        for i in range(0, len(column)):
            if not column[i]:
                self.board[position][i] = Config.player_one if player else Config.player_two
                return True

    def check_column_winner(self) -> str:
        for column in self.board:
            string_column = "".join(column)
            if string_column.find(Config.player_one * self.requirements) >= 0:
                return Config.player_one_name
            elif string_column.find(Config.player_two * self.requirements) >= 0:
                return Config.player_two_name
        return ""

    def check_row_winner(self) -> str:
        for i in range(0, self.height):
            string_row = ""
            for column in self.board:
                string_row += column[i] if column[i] else Config.blank
            if string_row.find(Config.player_one * self.requirements) >= 0:
                return Config.player_one_name
            elif string_row.find(Config.player_two * self.requirements) >= 0:
                return Config.player_two_name
        return ""

    def check_diagonal_winner(self) -> str:
        for column in range(0, (Config.height - Config.requirements) + 1):
            for row in range(0, (Config.width - Config.requirements) + 1):
                diagonal_left = ""
                diagonal_right = ""
                for i in range(0, Config.requirements):
                    diagonal_left += self.board[i + row][-1 - i - column]
                    diagonal_right += self.board[Config.requirements - 1 - i + row][-1 - i - column]
                if Config.player_one*Config.requirements in (diagonal_left, diagonal_right):
                    return Config.player_one_name
                if Config.player_two*Config.requirements in (diagonal_left, diagonal_right):
                    return Config.player_two_name
        return ""

    def check_winner(self) -> str:
        row = self.check_row_winner()
        column = self.check_column_winner()
        diagonal = self.check_diagonal_winner()
        if row:
            return row
        if column:
            return column
        if diagonal:
            return diagonal
        return ""