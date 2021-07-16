from typing import List

from config import Config


def generate_board(width: int, height: int) -> List:
    board = [[""] * height] * width
    return board


class ConnectFour:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.board = generate_board(width, height)

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
