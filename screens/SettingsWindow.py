from cv2 import cv2
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.slider import Slider
import asynckivy as ak
from kivy.uix.stacklayout import StackLayout

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


class CameraSelectionButton(Button):
    async def find_camera_devices(self):
        self.available_devices = list()
        dev_id = 0
        while True:
            cap = cv2.VideoCapture(dev_id)
            if cap.isOpened():
                self.available_devices.append(dev_id)
                cap.release()
            else:
                break
            dev_id += 1

    def save_cam_choice(self, instance):
        update_settings_file(filename_with_path,
                             constants.SETTINGS_CAMERA_DEVICE_KEY,
                             instance.text,
                             constants.SETTINGS_HEADER)
        self.popupWindow.dismiss()

    def on_button_click(self):
        ak.start(self.find_camera_devices())
        box_layout = BoxLayout()
        for device in self.available_devices:
            btn = Button(text=str(device))
            btn.bind(on_press=self.save_cam_choice)
            box_layout.add_widget(btn)
        self.popupWindow = Popup()
        self.popupWindow.title = 'Select your camera device:'
        self.popupWindow.size_hint = (None, None)
        self.popupWindow.size = (600, 400)
        self.popupWindow.content = box_layout
        self.popupWindow.open()


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
