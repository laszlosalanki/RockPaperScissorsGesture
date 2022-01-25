import asynckivy as ak
from cv2 import cv2
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch

from data import constants
from settings_file_helper import update_settings_file

filename_with_path = constants.SETTINGS_FILE_RELATIVE_PATH + constants.SETTINGS_FILE_NAME

settings = dict()


class FullscreenSwitch(Switch):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.bind_active, 2)

    def bind_active(self, dt):
        self.bind(active=self.on_active_change)

    def on_active_change(self, instance, value):
        if value is True:
            to_save = 'auto'
        else:
            to_save = value
        update_settings_file(filename_with_path,
                             constants.SETTINGS_FULLSCREEN_KEY,
                             to_save,
                             constants.SETTINGS_HEADER)
        Window.fullscreen = to_save


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
        settings[constants.SETTINGS_CAMERA_DEVICE_KEY] = instance.text
        self.popupWindow.dismiss()

    def on_button_click(self):
        ak.start(self.find_camera_devices())
        box_layout = BoxLayout()
        for device in self.available_devices:
            btn = Button(text=str(device))
            btn.bind(on_press=self.save_cam_choice)
            box_layout.add_widget(btn)
        self.popupWindow = Popup()
        self.popupWindow.title = constants.SETTINGS_SELECT_CAMERA_DEVICE
        self.popupWindow.size_hint = (None, None)
        self.popupWindow.size = (400, 100)
        self.popupWindow.content = box_layout
        self.popupWindow.open()


class SettingsWindow(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.read_settings_file)

    def keep_up_to_date(self, dt):
        self.ids.cam_device_label.text = constants.SETTINGS_SELECTED_CAMERA + \
                                         settings[constants.SETTINGS_CAMERA_DEVICE_KEY]

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
            if key == constants.SETTINGS_FULLSCREEN_KEY:
                act_val = None
                if value == 'auto':
                    act_val = True
                elif value == 'False':
                    act_val = False
                if act_val is not None:
                    self.ids.fullscreen_switch.active = act_val
            elif key == constants.SETTINGS_MIN_DETECTION_CONFIDENCE_KEY:
                self.ids.min_det_conf.value = float(value)
            elif key == constants.SETTINGS_MIN_TRACKING_CONFIDENCE_KEY:
                self.ids.min_tra_conf.value = float(value)
            elif key == constants.SETTINGS_CAMERA_DEVICE_KEY:
                self.keep_up_to_date_schedule = Clock.schedule_interval(self.keep_up_to_date, 2)

    def on_pre_leave(self, *args):
        Clock.unschedule(self.keep_up_to_date_schedule)
