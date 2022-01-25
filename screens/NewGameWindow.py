from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from data import constants
from settings_file_helper import update_settings_file


def save_game_mode(game_mode):
    file_name_with_path = constants.ACT_GAME_SETTINGS_RELATIVE_PATH + constants.ACT_GAME_SETTINGS_FILE_NAME
    update_settings_file(file_name_with_path, constants.GAME_MODE, game_mode)


class GameMode1(Button):
    gm = 0

    def set_game_mode(self, game_mode):
        self.gm = game_mode
        print(constants.LOG_TEMPLATE, constants.LOG_GAME_MODE_SELECTED, self.gm)
        save_game_mode(self.gm)


class GameMode2(Button):
    gm = 0

    def set_game_mode(self, game_mode):
        self.gm = game_mode
        print(constants.LOG_TEMPLATE, constants.LOG_GAME_MODE_SELECTED, self.gm)
        save_game_mode(self.gm)


class GameMode3(Button):
    gm = 0

    def set_game_mode(self, game_mode):
        self.gm = game_mode
        print(constants.LOG_TEMPLATE, constants.LOG_GAME_MODE_SELECTED, self.gm)
        save_game_mode(self.gm)


class NewGameWindow(Screen):
    pass
