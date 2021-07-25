from config import Config
from board import generate_board, ConnectFour


def test_generate_board():
    board = generate_board(Config.width, Config.height)
    assert len(board) == Config.width
    assert len(board[0]) == Config.height
    assert not board[0][0]


def test_construction():
    connect_four = ConnectFour()
    assert connect_four.width == Config.width
    assert connect_four.height == Config.height
    assert connect_four.board
    assert connect_four.requirements
    assert connect_four.requirements < Config.width
    assert connect_four.requirements < Config.height


def test_reset_board():
    connect_four = ConnectFour()
    connect_four.board[0][0] = Config.player_one
    connect_four.reset_board()
    assert not connect_four.board[0][0]


def test_add_element():
    connect_four = ConnectFour()
    assert not connect_four.board[0][0]
    connect_four.add_element(0, True)
    assert connect_four.board[0][0] == Config.player_one
    assert not connect_four.board[1][0]
    assert not connect_four.board[0][1]


def test_check_column_winner():
    for row in range(0, Config.width):
        for i in range(0, (Config.height - Config.requirements) + 1):
            connect_four = ConnectFour()
            for _ in range(0, i):
                connect_four.add_element(row, False)
            for _ in range(0, Config.requirements):
                connect_four.add_element(row, True)
            assert connect_four.check_column_winner()


def test_check_row_winner():
    for column in range(0, Config.height):
        for displacement in range(0, (Config.width - Config.requirements) + 1):
            connect_four = ConnectFour()
            for position in range(0, Config.requirements):
                connect_four.board[position+displacement][column] = Config.player_one
            assert connect_four.check_row_winner()


def test_check_diagonal_winner():
    for column in range(0, (Config.height - Config.requirements) + 1):
        for row in range(0, (Config.width - Config.requirements) + 1):
            connect_four = ConnectFour()
            for i in range(0, Config.requirements):
                connect_four.board[i+row][-1-i-column] = Config.player_one
            assert connect_four.check_diagonal_winner()
            connect_four = ConnectFour()
            for i in range(0, Config.requirements):
                connect_four.board[Config.requirements-1-i+row][-1-i-column] = Config.player_one
            assert connect_four.check_diagonal_winner()
