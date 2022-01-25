from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from data import constants
from settings_file_helper import update_settings_file


class TextInputP1(TextInput):
    max_characters = NumericProperty(11)

    def insert_text(self, substring, from_undo=False):
        if len(self.text) > self.max_characters:
            substring = ""
        TextInput.insert_text(self, substring, from_undo)


class TextInputP2(TextInput):
    max_characters = NumericProperty(11)

    def insert_text(self, substring, from_undo=False):
        if len(self.text) > self.max_characters:
            substring = ""
        TextInput.insert_text(self, substring, from_undo)


class NextButton(Button):
    def save_username(self, username, username_2):
        if username == '' and username_2 == '':
            username = constants.USERNAME_DEFAULT_VALUE
            username_2 = constants.USERNAME_2_DEFAULT_VALUE
        elif username == '':
            username = constants.USERNAME_DEFAULT_VALUE
        elif username_2 == '':
            username_2 = constants.USERNAME_2_DEFAULT_VALUE

        file_name_with_path = constants.ACT_GAME_SETTINGS_RELATIVE_PATH + constants.ACT_GAME_SETTINGS_FILE_NAME
        update_settings_file(file_name_with_path, constants.USERNAME, username)
        update_settings_file(file_name_with_path, constants.USERNAME_2, username_2)


class UsernameInputScreen(Screen):
    def on_pre_enter(self, *args):
        Clock.schedule_once(self.reset_fields)

    def reset_fields(self, dt):
        self.ids.player1_username.text = ''
        self.ids.player2_username.text = ''
