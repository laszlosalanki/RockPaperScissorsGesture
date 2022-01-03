from cv2 import cv2
from kivy.app import App
from kivy.lang import Builder
from kivy import Config

from data import constants
from screens.MainMenuWindow import MainMenuWindow
from screens.NewGameWindow import NewGameWindow
from screens.DifficultySelectionViewWindow import DifficultySelectionViewWindow
from screens.OpponentSelectionViewWindow import OpponentSelectionViewWindow
from screens.GameWindow import GameWindow
from screens.ScoreboardWindow import ScoreboardWindow
from screens.SettingsWindow import SettingsWindow
from screens.WindowManager import WindowManager
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from os import remove
from settings_file_helper import create_settings_file


Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '768')
kv = Builder.load_file('kv/rockpaperscissor.kv')


class RockPaperScissorMainApp(App):
    def build(self):
        self.title = 'Rock Paper Scissor Gesture'
        return kv

    def on_start(self):
        create_settings_file(constants.ACT_GAME_SETTINGS_RELATIVE_PATH + constants.ACT_GAME_SETTINGS_FILE_NAME)

    def on_stop(self):
        remove(constants.ACT_GAME_SETTINGS_RELATIVE_PATH + constants.ACT_GAME_SETTINGS_FILE_NAME)
        print(constants.LOG_TEMPLATE, constants.LOG_ACT_GAME_SETTINGS_FILE_DELETED)


if __name__ == '__main__':
    RockPaperScissorMainApp().run()
