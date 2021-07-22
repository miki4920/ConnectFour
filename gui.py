from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from typing import List, Tuple, Callable

from config import Config
from main import ConnectFour


# TODO: Swap GUI and Main around
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
                  size_hint=(None, None), size=(400, 400))
    popup.bind(on_dismiss=function)
    return popup


class MainApp(App):
    def __init__(self):
        super().__init__()
        self.connect_four = ConnectFour()
        self.grid_layout = GridLayout(cols=Config.width)
        self.current_player = True

    # TODO: Make this function static
    def create_board(self):
        for column in range(0, Config.height):
            for row in range(0, Config.width):
                element = self.connect_four.board[row][-1 - column]
                colour = pick_colour(element)
                position = (row, -1 - column)
                button = set_button(colour, position, self.add_element_gui)
                self.grid_layout.add_widget(button)

    # TODO: Find a more elegant solution to instance
    def reset_board(self, instance=None, soft_reset=False):
        if not soft_reset:
            self.connect_four.reset_board()
        self.grid_layout.clear_widgets()
        self.create_board()

    def check_winner(self):
        winner = self.connect_four.check_winner()
        if winner:
            popup = set_popup(winner, self.reset_board)
            popup.open()

    # TODO: Look for simplifications
    def add_element_gui(self, instance: Button):
        if instance.background_color == Config.player_one_colour or instance.background_color == Config.player_two_colour:
            return
        position = instance.ids["position"]
        self.connect_four.add_element(position[0], self.current_player)
        self.current_player = not self.current_player
        self.reset_board(soft_reset=True)
        self.check_winner()

    def build(self):
        self.create_board()
        return self.grid_layout


if __name__ == "__main__":
    MainApp().run()
