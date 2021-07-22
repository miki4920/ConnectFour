from kivy.uix.button import Button

from config import Config
from gui import pick_colour, set_button, set_popup


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

