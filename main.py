from cv2 import cv2
from kivy.app import App
from kivy.lang import Builder
from screens.MainMenuWindow import MainMenuWindow
from screens.GameWindow import GameWindow
from screens.ScoreboardWindow import ScoreboardWindow
from screens.SettingsWindow import SettingsWindow
from screens.WindowManager import WindowManager
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget


kv = Builder.load_file('kv/rockpaperscissor.kv')


class RockPaperScissorMainApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    RockPaperScissorMainApp().run()
