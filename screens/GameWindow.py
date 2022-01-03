from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from hand_detection import HandDetection
import cv2

cap = cv2.VideoCapture(0)
hd = HandDetection()


class CameraFrame(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 0.05)

    def update(self, dt):
        if cap.isOpened():
            success, image = cap.read()
            (processed_image, landmarks) = hd.find_hand_positions(image)
            buf1 = cv2.flip(processed_image, 0)
            buf = buf1.tostring()
            texture = Texture.create(size=(processed_image.shape[1], processed_image.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = texture


class GameWindow(Screen):
    pass
