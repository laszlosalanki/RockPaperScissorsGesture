from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from data import constants
from settings_file_helper import update_settings_file


def save_difficulty(difficulty):
    file_name_with_path = constants.ACT_GAME_SETTINGS_RELATIVE_PATH + constants.ACT_GAME_SETTINGS_FILE_NAME
    update_settings_file(file_name_with_path, constants.DIFFICULTY, difficulty)


class EasyButton(Button):
    diff = 0

    def set_difficulty(self, difficulty):
        self.diff = difficulty
        print(constants.LOG_TEMPLATE, constants.LOG_DIFFICULTY_SELECTED, self.diff)
        save_difficulty(self.diff)


class NormalButton(Button):
    diff = 0

    def set_difficulty(self, difficulty):
        self.diff = difficulty
        print(constants.LOG_TEMPLATE, constants.LOG_DIFFICULTY_SELECTED, self.diff)
        save_difficulty(self.diff)


class HardButton(Button):
    diff = 0

    def set_difficulty(self, difficulty):
        self.diff = difficulty
        print(constants.LOG_TEMPLATE, constants.LOG_DIFFICULTY_SELECTED, self.diff)
        save_difficulty(self.diff)


class DifficultySelectionViewWindow(Screen):
    pass
