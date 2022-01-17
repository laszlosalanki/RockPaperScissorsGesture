from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from time import sleep
from data import constants
from hand_detection import HandDetection, get_coordinates_by_hand, recognise_hand_gesture
from cv2 import cv2

detected_gesture = None
player_1s_turn = True


class CameraFrame(Image):
    pass


class GameWindow(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.init)

    # Init images and labels
    def init(self, dt):
        # Camera feed
        self.ids.camera_frame.source = constants.GESTURE_IMAGES[constants.LOG_NO_HAND]
        # Detected images
        self.ids.gesture_image_p1.source = constants.GESTURE_IMAGES[constants.LOG_NO_HAND]
        self.ids.gesture_image_p2.source = constants.GESTURE_IMAGES[constants.LOG_NO_HAND]
        # Detected labels
        self.ids.gesture_text_p1.text = constants.LOG_NO_HAND
        self.ids.gesture_text_p2.text = constants.LOG_NO_HAND

    def on_pre_enter(self, *args):
        self.cap = cv2.VideoCapture(0)
        self.hd = HandDetection()
        Clock.schedule_interval(self.update, 0.03)

    def update(self, dt):
        if self.cap.isOpened():
            success, image = self.cap.read()
            (processed_image, landmarks) = self.hd.find_hand_positions(image)

            global detected_gesture

            if landmarks:
                data = get_coordinates_by_hand(landmarks, 0, processed_image.shape[1], processed_image.shape[0])
                detected_gesture = recognise_hand_gesture(data)
                print(constants.LOG_TEMPLATE, constants.LOG_PREDICTED_GESTURE, detected_gesture)
            else:
                detected_gesture = constants.LOG_NO_HAND

            buf1 = cv2.flip(processed_image, 0)
            buf = buf1.tostring()
            texture = Texture.create(size=(processed_image.shape[1], processed_image.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            self.ids.camera_frame.texture = texture

            if player_1s_turn:
                self.predicted_photo_p1()
                self.predicted_text_p1()
            else:
                self.predicted_photo_p2()
                self.predicted_text_p2()

    def countdown(self, dt):
        sec = 3
        while sec:
            mins, secs = divmod(sec, 60)
            print(secs)
            sleep(1)
            sec -= 1

    def predicted_photo_p1(self):
        global detected_gesture
        if detected_gesture:
            if detected_gesture in constants.GESTURE_IMAGES.keys():
                self.ids.gesture_image_p1.source = constants.GESTURE_IMAGES[detected_gesture]

    def predicted_text_p1(self):
        global detected_gesture
        if detected_gesture:
            self.ids.gesture_text_p1.text = detected_gesture

    def predicted_photo_p2(self):
        global detected_gesture
        if detected_gesture:
            if detected_gesture in constants.GESTURE_IMAGES.keys():
                self.ids.gesture_image_p2.source = constants.GESTURE_IMAGES[detected_gesture]

    def predicted_text_p2(self):
        global detected_gesture
        if detected_gesture:
            self.ids.gesture_text_p2.text = detected_gesture

    def on_pre_leave(self, *args):
        self.cap.release()
