from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.switch import Switch
from os.path import exists
from data import constants
from settings_file_helper import create_settings_file, update_settings_file

settings = dict()
filename_with_path = constants.SETTINGS_FILE_RELATIVE_PATH + constants.SETTINGS_FILE_NAME

if exists(filename_with_path):
    with open(filename_with_path, 'r') as settings_file:
        settings_lines = settings_file.readlines()[1:]

        for line in settings_lines:
            settings[line.split(' ')[0]] = line.split(' ')[1]

        # TODO: set the switches
    #
else:
    create_settings_file(filename_with_path, constants.SETTINGS_HEADER)


class LoggingSwitch(Switch):
    def switch_callback(self, active):
        if active:
            update_settings_file(filename_with_path, constants.SETTINGS_IS_LOGGING_ENABLED_KEY,
                                 'True', constants.SETTINGS_HEADER)
            settings[constants.SETTINGS_IS_LOGGING_ENABLED_KEY] = 'True'
        else:
            update_settings_file(filename_with_path, constants.SETTINGS_IS_LOGGING_ENABLED_KEY,
                                 'False', constants.SETTINGS_HEADER)
            settings[constants.SETTINGS_IS_LOGGING_ENABLED_KEY] = 'False'


class BackAndSaveButton(Button):
    def save_settings(self):
        pass


class SettingsWindow(Screen):
    pass
