from typing import List

from config import Config


def generate_board(width: int, height: int) -> List[List[str]]:
    board = [[""] * height] * width
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
                column[i] = Config.player_one if player else Config.player_two
                break

    def check_column_winner(self):
        for column in range(0, self.width):
            for row in range(0, (self.height-self.requirements)+1):
                column_slice = self.board[column][0+row:0+row+self.requirements]
                if all(map(lambda symbol: symbol == Config.player_one, column_slice)) or all(map(lambda symbol: symbol == Config.player_two, column_slice)):
                    return True
        return False
