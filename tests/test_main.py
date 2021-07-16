from config import Config
from main import generate_board, ConnectFour


def test_generate_board():
    board = generate_board(Config.width, Config.height)
    assert len(board) == Config.width
    assert len(board[0]) == Config.height
    assert not board[0][0]


def test_construction():
    connect_four = ConnectFour(Config.width, Config.height)
    assert connect_four.width == Config.width
    assert connect_four.height == Config.height
    assert connect_four.board


def test_check_column():
    connect_four = ConnectFour(Config.width, Config.height)
    assert connect_four.check_column(0)
    for _ in range(0, 6):
        connect_four.add_element(0, True)
    assert not connect_four.check_column(0)


def test_add_element():
    connect_four = ConnectFour(Config.width, Config.height)
    assert not connect_four.board[0][0]
    connect_four.add_element(0, True)
    connect_four.add_element(0, False)
    assert connect_four.board[0][0] == Config.player_one
    assert connect_four.board[0][1] == Config.player_two
