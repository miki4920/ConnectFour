from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics import Color

from config import Config


class RootWidget(GridLayout):
    pass


class MainApp(App):
    def build(self):
        parent = GridLayout(cols=Config.width)
        for row in range(0, Config.width):
            for column in range(0, Config.height):
                parent.add_widget(Button(text='%s%s'%(row,column)))
        return parent


if __name__ == "__main__":
    MainApp().run()