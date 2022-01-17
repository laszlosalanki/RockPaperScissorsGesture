from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from data import constants
from settings_file_helper import update_settings_file


def save_opponent(opponent):
    file_name_with_path = constants.ACT_GAME_SETTINGS_RELATIVE_PATH + constants.ACT_GAME_SETTINGS_FILE_NAME
    update_settings_file(file_name_with_path, constants.OPPONENT, opponent)
    # TODO: user can enter the username, a button should call save_username
    save_username()


def save_username(username=constants.USERNAME_DEFAULT_VALUE, username_2=constants.USERNAME_2_DEFAULT_VALUE):
    file_name_with_path = constants.ACT_GAME_SETTINGS_RELATIVE_PATH + constants.ACT_GAME_SETTINGS_FILE_NAME
    update_settings_file(file_name_with_path, constants.USERNAME, username)
    update_settings_file(file_name_with_path, constants.USERNAME_2, username_2)


class Computer(Button):
    op = 0

    def set_opponent(self, opponent):
        self.op = opponent
        print(constants.LOG_TEMPLATE, constants.LOG_OPPONENT_SELECTED, self.op)
        save_opponent(self.op)


class Other(Button):
    op = 0

    def set_opponent(self, opponent):
        self.op = opponent
        print(constants.LOG_TEMPLATE, constants.LOG_OPPONENT_SELECTED, self.op)
        save_opponent(self.op)


class OpponentSelectionViewWindow(Screen):
    pass
