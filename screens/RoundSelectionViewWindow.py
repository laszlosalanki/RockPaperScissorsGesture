from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from data import constants
from settings_file_helper import update_settings_file


def save_rounds(rounds):
    file_name_with_path = constants.ACT_GAME_SETTINGS_RELATIVE_PATH + constants.ACT_GAME_SETTINGS_FILE_NAME
    update_settings_file(file_name_with_path, constants.ROUNDS, rounds)


class Round3Button(Button):
    r = 0

    def set_rounds(self, rounds):
        self.r = rounds
        print(constants.LOG_TEMPLATE, constants.LOG_ROUNDS_SELECTED, self.r)
        save_rounds(self.r)


class Round5Button(Button):
    r = 0

    def set_rounds(self, rounds):
        self.r = rounds
        print(constants.LOG_TEMPLATE, constants.LOG_ROUNDS_SELECTED, self.r)
        save_rounds(self.r)


class Round7Button(Button):
    r = 0

    def set_rounds(self, rounds):
        self.r = rounds
        print(constants.LOG_TEMPLATE, constants.LOG_ROUNDS_SELECTED, self.r)
        save_rounds(self.r)


class Round9Button(Button):
    r = 0

    def set_rounds(self, rounds):
        self.r = rounds
        print(constants.LOG_TEMPLATE, constants.LOG_ROUNDS_SELECTED, self.r)
        save_rounds(self.r)


class RoundSelectionViewWindow(Screen):
    pass
