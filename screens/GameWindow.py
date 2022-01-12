from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.graphics.texture import Texture

from data import constants
from hand_detection import HandDetection, get_coordinates_by_hand, recognise_hand_gesture
import cv2


class CameraFrame(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cap = cv2.VideoCapture(1)
        self.hd = HandDetection()
        Clock.schedule_interval(self.update, 0.03)

    def update(self, dt):
        if self.cap.isOpened():
            success, image = self.cap.read()
            (processed_image, landmarks) = self.hd.find_hand_positions(image)

            if landmarks:
                data = get_coordinates_by_hand(landmarks, 0, processed_image.shape[1], processed_image.shape[0])
                print(constants.LOG_TEMPLATE, constants.LOG_PREDICTED_GESTURE, recognise_hand_gesture(data))

            buf1 = cv2.flip(processed_image, 0)
            buf = buf1.tostring()
            texture = Texture.create(size=(processed_image.shape[1], processed_image.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = texture


class GameWindow(Screen):
    pass
