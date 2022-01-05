from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput

from settings_file_helper import update_settings_file
from data import constants

filename_with_path = constants.SETTINGS_FILE_RELATIVE_PATH + constants.SETTINGS_FILE_NAME


# TODO: replace the log buttons with a switch, then update the states
# TODO: set the slider values to the ones from the settings file

class LoggingOffButton(Button):
    def log_off_click(self):
        update_settings_file(filename_with_path,
                             constants.SETTINGS_IS_LOGGING_ENABLED_KEY,
                             False,
                             constants.SETTINGS_HEADER)


class LoggingOnButton(Button):
    def log_on_click(self):
        update_settings_file(filename_with_path,
                             constants.SETTINGS_IS_LOGGING_ENABLED_KEY,
                             True,
                             constants.SETTINGS_HEADER)


class MinDetectionConfidenceSwitch(Slider):
    def save_value_on_touch_up(self):
        update_settings_file(filename_with_path,
                             constants.SETTINGS_MIN_DETECTION_CONFIDENCE_KEY,
                             self.value,
                             constants.SETTINGS_HEADER)


class MinTrackingConfidenceSwitch(Slider):
    def save_value_on_touch_up(self):
        update_settings_file(filename_with_path,
                             constants.SETTINGS_MIN_TRACKING_CONFIDENCE_KEY,
                             self.value,
                             constants.SETTINGS_HEADER)


class SettingsWindow(Screen):
    pass
