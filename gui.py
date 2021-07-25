from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from typing import List, Tuple, Callable, Generator

from config import Config
from main import ConnectFour


def pick_colour(element: str) -> List[float]:
    if element:
        return Config.player_one_colour if element == Config.player_one else Config.player_two_colour
    return Config.blank_colour


def set_button(colour: List[float], position: Tuple[int, int], function: Callable) -> Button:
    button = Button(background_color=colour)
    button.ids['position'] = position
    button.bind(on_release=function)
    return button


def set_popup(winner: str, function: Callable) -> Popup:
    popup = Popup(title='Winner!',
                  content=Label(text=winner),
                  size_hint=(None, None), size=(100, 100))
    popup.bind(on_dismiss=function)
    return popup


def button_board(board: List[List[str]], function: Callable) -> Generator[Button, None, None]:
    for column in range(0, Config.height):
        for row in range(0, Config.width):
            element = board[row][-1 - column]
            colour = pick_colour(element)
            position = (row, -1 - column)
            button = set_button(colour, position, function)
            yield button


class MainApp(App):
    def __init__(self):
        super().__init__()
        self.connect_four = ConnectFour()
        self.grid_layout = GridLayout(cols=Config.width)
        self.current_player = True

    def create_board(self):
        board = button_board(self.connect_four.board, self.add_element_gui)
        for button in board:
            self.grid_layout.add_widget(button)

    def reset_board(self, instance=None, soft_reset=False):
        if not soft_reset:
            self.connect_four.reset_board()
        self.grid_layout.clear_widgets()
        self.create_board()

    def add_element_gui(self, instance: Button):
        if instance.background_color in (Config.player_one_colour, Config.player_two_colour):
            return
        position = instance.ids["position"]
        self.connect_four.add_element(position[0], self.current_player)
        self.current_player = not self.current_player
        self.reset_board(soft_reset=True)
        if winner := self.connect_four.check_winner():
            popup = set_popup(winner, self.reset_board)
            popup.open()

    def build(self):
        self.create_board()
        return self.grid_layout


if __name__ == "__main__":
    MainApp().run()
