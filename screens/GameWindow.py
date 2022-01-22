import random

from kivy.animation import Animation
from kivy.properties import NumericProperty
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from data import constants
from hand_detection import HandDetection, get_coordinates_by_hand, recognise_hand_gesture
from cv2 import cv2

from settings_file_helper import read_into_dict

detected_gesture = None
player_1s_turn = True
available_gestures = None

act_settings = dict()
settings = dict()

act_settings_filename = constants.ACT_GAME_SETTINGS_RELATIVE_PATH + constants.ACT_GAME_SETTINGS_FILE_NAME
settings_filename = constants.SETTINGS_FILE_RELATIVE_PATH + constants.SETTINGS_FILE_NAME


class Player1Name(Label):
    pass


class Player2Name(Label):
    pass


class Player1Turn(Label):
    pass


class Player2Turn(Label):
    pass


class CameraFrame(Image):
    pass


class CountdownClockP1(Label):
    a = NumericProperty(5)

    def start_initial_countdown(self):
        Animation.cancel_all(self)
        self.anim = Animation(a=0, duration=self.a)

        def finish_callback(animation, incr_crude_clock):
            incr_crude_clock.text = ""

        self.anim.bind(on_complete=finish_callback)
        self.anim.start(self)


class CountdownClockP2(Label):
    a = NumericProperty(5)

    def start_initial_countdown(self):
        Animation.cancel_all(self)
        self.anim = Animation(a=0, duration=self.a)

        def finish_callback(animation, incr_crude_clock):
            incr_crude_clock.text = ""

        self.anim.bind(on_complete=finish_callback)
        self.anim.start(self)


class GameWindow(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.init)

    # Init images and labels
    def init(self, dt):
        # Init camera feed
        self.ids.camera_frame.source = constants.GESTURE_IMAGES[constants.LOG_NO_HAND]
        # Init detected images
        self.ids.gesture_image_p1.source = constants.GESTURE_IMAGES[constants.LOG_NO_HAND]
        self.ids.gesture_image_p2.source = constants.GESTURE_IMAGES[constants.LOG_NO_HAND]
        # Init detected labels
        self.ids.gesture_text_p1.text = constants.LOG_NO_HAND
        self.ids.gesture_text_p2.text = constants.LOG_NO_HAND

    def on_pre_enter(self, *args):
        # Read ACT_SETTINGS file
        global act_settings
        act_settings = read_into_dict(act_settings_filename)
        global settings
        settings = read_into_dict(settings_filename)
        # Set player names according to the selected opponent
        self.ids.player1_name.text = act_settings[constants.USERNAME]
        if int(act_settings[constants.OPPONENT]) == 1:
            self.ids.player2_name.text = random.choice(constants.COMPUTER_NAMES)
        else:
            self.ids.player2_name.text = act_settings[constants.USERNAME_2]

        # Set the available gestures according to the selected game mode
        global available_gestures
        if int(act_settings[constants.GAME_MODE]) == 1:
            available_gestures = constants.GAME_MODE_1_CHOICES
        elif int(act_settings[constants.GAME_MODE]) == 2:
            available_gestures = constants.GAME_MODE_2_CHOICES
        else:
            available_gestures = constants.GAME_MODE_3_CHOICES

        # Initialize webcam and hand detection module (TODO: user should be able to select webcam number)
        self.cap = cv2.VideoCapture(0)
        self.hd = HandDetection(min_detection_confidence=float(settings[constants.SETTINGS_MIN_DETECTION_CONFIDENCE_KEY]),
                                min_tracking_confidence=float(settings[constants.SETTINGS_MIN_TRACKING_CONFIDENCE_KEY]))
        # Schedule camera frame update
        Clock.schedule_interval(self.update, 0.03)

    def update(self, dt):
        if self.cap.isOpened():
            success, image = self.cap.read()
            (processed_image, landmarks) = self.hd.find_hand_positions(image)

            global detected_gesture

            if landmarks:
                data = get_coordinates_by_hand(landmarks, 0, processed_image.shape[1], processed_image.shape[0])
                gesture = recognise_hand_gesture(data)
                # Check if the detected gesture is available in the selected game mode
                if gesture in available_gestures:
                    detected_gesture = gesture
                else:
                    detected_gesture = constants.LOG_CANNOT_RECOGNISE_GESTURE
                print(constants.LOG_TEMPLATE, constants.LOG_PREDICTED_GESTURE, detected_gesture)
            else:
                detected_gesture = constants.LOG_NO_HAND

            buf1 = cv2.flip(processed_image, 0)
            buf = buf1.tostring()
            texture = Texture.create(size=(processed_image.shape[1], processed_image.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            self.ids.camera_frame.texture = texture

            # TODO: should set elsewhere
            if player_1s_turn:
                self.predicted_photo_p1()
                self.predicted_text_p1()
            else:
                self.predicted_photo_p2()
                self.predicted_text_p2()

    def on_enter(self, *args):
        # Start the main countdown until the game actually starts
        self.ids.countdown_p1.start_initial_countdown()
        self.ids.countdown_p2.start_initial_countdown()
        # Game should continue according to the selected opponent
        if int(act_settings[constants.OPPONENT]) == 1:
            # Rounds
            rounds = 1
            while rounds != int(act_settings[constants.ROUNDS]) + 1:
                # TODO
                # Player 1 comes first. Let's set his/her round counter properly.
                self.ids.player1_round.text = str(rounds)
                # Set 'Your turn' text.
                self.ids.player1_turn.text = constants.YOUR_TURN
                # Countdown, take average of detected gestures
                # TODO
                # Player 2 comes next.
                # Set Player 1's 'Your turn' text to '', and Player 2's to 'Your turn'.
                self.ids.player1_turn.text = ''
                self.ids.player2_turn_text = constants.YOUR_TURN
                # Countdown
                # TODO
                # Choose random gesture and display it
                computer_choice = random.choice(available_gestures)
                self.ids.gesture_image_p2.source = constants.GESTURE_IMAGES[computer_choice]
                self.ids.gesture_text_p2.text = computer_choice
                # Compare choices and set arrow
                p1_won_round = None
                is_draw = None
                if detected_gesture == computer_choice:
                    is_draw = True
                    self.ids.who_won_round.text = '='
                elif detected_gesture in constants.WEAKNESSES[computer_choice]:
                    p1_won_round = True
                    self.ids.who_won_round.text = '>'
                else:
                    p1_won_round = False
                    self.ids.who_won_round.text = '<'
                # Set score properly
                if not is_draw:
                    if p1_won_round:
                        self.p1_score = None
                        if self.ids.p1_score.text == '':
                            self.p1_score = 1
                        else:
                            self.p1_score = int(self.ids.p1_score.text)
                            self.p1_score += 1
                        self.ids.p1_score.text = str(self.p1_score)
                    else:
                        self.p2_score = None
                        if self.ids.p2_score.text == '':
                            self.p2_score = 1
                        else:
                            self.p2_score = int(self.ids.p2_score.text)
                            self.p2_score += 1
                        self.ids.p2_score.text = str(self.p2_score)

                # Wait
                # TODO
                # Next round
                rounds += 1
        else:
            # TODO: Against other player
            rounds = 1
            while rounds != int(act_settings[constants.ROUNDS]) + 1:
                pass

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
        # TODO: save results, so it can be displayed later in Scoreboard window
