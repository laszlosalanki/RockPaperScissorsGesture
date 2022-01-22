from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.slider import Slider

from settings_file_helper import update_settings_file
from data import constants

filename_with_path = constants.SETTINGS_FILE_RELATIVE_PATH + constants.SETTINGS_FILE_NAME

settings = dict()


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

    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.read_settings_file, 1)

    def read_settings_file(self, dt):
        global settings
        with open(filename_with_path, 'r') as saved_settings_file:
            settings_lines = saved_settings_file.readlines()[1:]
            for line in settings_lines:
                line_parts = line.split(' ')
                line_parts[0] = line_parts[0] + ' '
                settings[line_parts[0]] = line_parts[1].strip()
            #
        #
        for key, value in settings.items():
            if key == constants.SETTINGS_MIN_DETECTION_CONFIDENCE_KEY:
                self.ids.min_det_conf.value = float(value)
            elif key == constants.SETTINGS_MIN_TRACKING_CONFIDENCE_KEY:
                self.ids.min_tra_conf.value = float(value)