from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from data import constants
from settings_file_helper import update_settings_file


class NextButton(Button):
    def save_username(self, username, username_2):
        if username == '':
            username = constants.USERNAME_DEFAULT_VALUE
        elif username_2 == '':
            username_2 = constants.USERNAME_2_DEFAULT_VALUE
        elif username == '' and username_2 == '':
            username = constants.USERNAME_DEFAULT_VALUE
            username_2 = constants.USERNAME_2_DEFAULT_VALUE
        file_name_with_path = constants.ACT_GAME_SETTINGS_RELATIVE_PATH + constants.ACT_GAME_SETTINGS_FILE_NAME
        update_settings_file(file_name_with_path, constants.USERNAME, username)
        update_settings_file(file_name_with_path, constants.USERNAME_2, username_2)


class UserNameInputScreen(Screen):
    pass
