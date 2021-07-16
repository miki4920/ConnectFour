from config import Config
from main import generate_board, ConnectFour


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


def test_add_element():
    connect_four = ConnectFour()
    assert not connect_four.board[0][0]
    connect_four.add_element(0, True)
    connect_four.add_element(0, False)
    assert connect_four.board[0][0] == Config.player_one
    assert connect_four.board[0][1] == Config.player_two


def test_check_column():
    connect_four = ConnectFour()
    assert connect_four.check_column(0)
    for _ in range(0, 6):
        connect_four.add_element(0, True)
    assert not connect_four.check_column(0)


def test_check_column_winner():
    for column in range(0, Config.width):
        for i in range(0, (Config.height-Config.requirements)+1):
            connect_four = ConnectFour()
            for _ in range(0, i):
                connect_four.add_element(column, False)
            for _ in range(0, Config.requirements):
                connect_four.add_element(column, True)
            assert connect_four.check_column_winner()
