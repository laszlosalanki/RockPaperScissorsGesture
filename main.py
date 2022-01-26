from os import remove
from os.path import exists

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder

from screens.MainMenuWindow import MainMenuWindow
from screens.NewGameWindow import NewGameWindow
from screens.OpponentSelectionViewWindow import OpponentSelectionViewWindow
from screens.RoundSelectionViewWindow import RoundSelectionViewWindow
from screens.GameWindow import GameWindow
from screens.ScoreboardWindow import ScoreboardWindow
from screens.SettingsWindow import SettingsWindow
from screens.UserNameInputScreen import UsernameInputScreen
from screens.help.HelpMain import HelpMain
from screens.WindowManager import WindowManager

from data import constants
from settings_file_helper import create_settings_file, update_settings_file

kv = Builder.load_file(constants.KV_FILE)

settings = dict()

act_settings_file = constants.ACT_GAME_SETTINGS_RELATIVE_PATH + constants.ACT_GAME_SETTINGS_FILE_NAME
settings_file = constants.SETTINGS_FILE_RELATIVE_PATH + constants.SETTINGS_FILE_NAME


def create_settings_file_with_default_values():
    create_settings_file(settings_file,
                         constants.SETTINGS_HEADER)
    update_settings_file(settings_file,
                         constants.SETTINGS_IS_FIRST_START_KEY,
                         constants.SETTINGS_IS_FIRST_START_DEFAULT_VALUE,
                         constants.SETTINGS_HEADER)
    update_settings_file(settings_file,
                         constants.SETTINGS_FULLSCREEN_KEY,
                         constants.SETTINGS_FULLSCREEN_DEFAULT_VALUE,
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


def read_settings():
    global settings
    with open(settings_file, 'r') as saved_settings_file:
        settings_lines = saved_settings_file.readlines()[1:]
        for line in settings_lines:
            line_parts = line.split(' ')
            line_parts[0] = line_parts[0] + ' '
            settings[line_parts[0]] = line_parts[1].strip()
        #
    #


if not exists(settings_file):
    create_settings_file_with_default_values()

read_settings()

if settings[constants.SETTINGS_FULLSCREEN_KEY] == 'auto':
    Window.fullscreen = settings[constants.SETTINGS_FULLSCREEN_KEY]
elif settings[constants.SETTINGS_FULLSCREEN_KEY] == 'False':
    Window.fullscreen = False
    Window.size = (1360, 768)
    Window.minimum_width, Window.minimum_height = Window.size


class RockPaperScissorsMainApp(App):
    def build(self):
        self.title = constants.TITLE
        return kv

    def on_start(self):
        create_settings_file(act_settings_file)

        if settings[constants.SETTINGS_IS_FIRST_START_KEY] == 'True':
            update_settings_file(settings_file,
                                 constants.SETTINGS_IS_FIRST_START_KEY,
                                 False,
                                 constants.SETTINGS_HEADER)
            App.get_running_app().root.current = 'help'

    def on_stop(self):
        remove(constants.ACT_GAME_SETTINGS_RELATIVE_PATH + constants.ACT_GAME_SETTINGS_FILE_NAME)


if __name__ == '__main__':
    RockPaperScissorsMainApp().run()
