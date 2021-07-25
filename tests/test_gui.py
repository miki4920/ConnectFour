from config import Config
from gui import pick_colour, set_button, set_popup, button_board
from main import ConnectFour


def test_pick_colour():
    assert pick_colour(Config.player_one) == Config.player_one_colour
    assert pick_colour(Config.player_two) == Config.player_two_colour
    assert pick_colour("") == Config.blank_colour


def test_set_button():
    colour = Config.player_one_colour
    position = (0, 0)
    button = set_button(colour, position, abs)
    assert button.background_color == colour
    assert button.ids["position"] == position
    assert callable(button.on_release)


def test_set_popup():
    winner = Config.player_one_name
    assert set_popup(winner, abs).content.text == winner


def test_button_board():
    connect_four = ConnectFour()
    generate_board = button_board(connect_four.board, abs)
    for button in generate_board:
        assert button.background_color == Config.blank_colour
        assert type(button.ids["position"]) == tuple
        assert callable(button.on_release)
