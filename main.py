from cv2 import cv2
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy import Config
from win32api import GetSystemMetrics

from data import constants
from screens.MainMenuWindow import MainMenuWindow
from screens.NewGameWindow import NewGameWindow
from screens.OpponentSelectionViewWindow import OpponentSelectionViewWindow
from screens.RoundSelectionViewWindow import RoundSelectionViewWindow
from screens.GameWindow import GameWindow
from screens.ScoreboardWindow import ScoreboardWindow
from screens.SettingsWindow import SettingsWindow
from screens.UserNameInputScreen import UserNameInputScreen
from screens.help.HelpMain import HelpMain
from screens.WindowManager import WindowManager
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from os import remove
from os.path import exists
from settings_file_helper import create_settings_file, update_settings_file

kv = Builder.load_file(constants.KV_FILE)

screensize = GetSystemMetrics(0), GetSystemMetrics(1)
Window.size = screensize
Window.fullscreen = True


act_settings_file = constants.ACT_GAME_SETTINGS_RELATIVE_PATH + constants.ACT_GAME_SETTINGS_FILE_NAME
settings_file = constants.SETTINGS_FILE_RELATIVE_PATH + constants.SETTINGS_FILE_NAME


def create_settings_file_with_default_values():
    create_settings_file(settings_file,
                         constants.SETTINGS_HEADER)
    update_settings_file(settings_file,
                         constants.SETTINGS_MIN_DETECTION_CONFIDENCE_KEY,
                         constants.SETTINGS_MIN_DETECTION_CONFIDENCE_DEFAULT_VALUE,
                         constants.SETTINGS_HEADER)
    update_settings_file(settings_file,
                         constants.SETTINGS_MIN_TRACKING_CONFIDENCE_KEY,
                         constants.SETTINGS_MIN_TRACKING_CONFIDENCE_DEFAULT_VALUE,
                         constants.SETTINGS_HEADER)
    update_settings_file(settings_file,
                         constants.SETTINGS_CAMERA_DEVICE_KEY,
                         constants.SETTINGS_CAMERA_DEVICE_DEFAULT_VALUE,
                         constants.SETTINGS_HEADER)


class RockPaperScissorMainApp(App):
    def build(self):
        self.title = constants.TITLE
        return kv

    def on_start(self):
        create_settings_file(act_settings_file)

        if not exists(settings_file):
            create_settings_file_with_default_values()

    def on_stop(self):
        remove(constants.ACT_GAME_SETTINGS_RELATIVE_PATH + constants.ACT_GAME_SETTINGS_FILE_NAME)


if __name__ == '__main__':
    RockPaperScissorMainApp().run()
