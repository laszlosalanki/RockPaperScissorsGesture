import operator
import random
from datetime import datetime
from json import dumps

import asynckivy as ak
from cv2 import cv2
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

from data import constants
from hand_detection import HandDetection, get_coordinates_by_hand, recognise_hand_gesture
from settings_file_helper import read_into_dict

detected_gesture = None
detected_gesture_list = list()
player_1s_turn = True
available_gestures = list()
can_show_live_image_p1 = True
can_show_live_image_p2 = False
should_save_history_file = True

game_data = dict()

winner = None
p1_score = 0
p2_score = 0

game_time_in_secs = 0

act_settings = dict()
settings = dict()

act_settings_filename = constants.ACT_GAME_SETTINGS_RELATIVE_PATH + constants.ACT_GAME_SETTINGS_FILE_NAME
settings_filename = constants.SETTINGS_FILE_RELATIVE_PATH + constants.SETTINGS_FILE_NAME


class CameraFrame(Image):
    pass


def incr_game_time(dt):
    global game_time_in_secs
    game_time_in_secs += 1


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
        # Init texts
        self.ids.who_won_round.text = ''
        self.ids.countdown_p1.text = ''
        self.ids.countdown_p2.text = ''
        self.ids.player1_info.text = ''
        self.ids.player2_info.text = ''
        # Init score
        self.ids.p1_score.text = '0'
        self.ids.p2_score.text = '0'
        # Counter for initial countdown
        self.init_countdown_cnt = 5
        # Bind the cancel button
        self.ids.game_main_button.bind(on_press=self.cancel_things)

    def on_pre_enter(self, *args):
        # Run init again (in case of the game was cancelled before)
        Clock.schedule_once(self.init)
        # Read ACT_SETTINGS file
        global act_settings
        act_settings = read_into_dict(act_settings_filename)
        global settings
        settings = read_into_dict(settings_filename)
        global game_data
        # Set player names according to the selected opponent
        self.ids.player1_name.text = act_settings[constants.USERNAME]
        game_data[constants.HISTORY_PLAYER_1] = act_settings[constants.USERNAME]
        if int(act_settings[constants.OPPONENT]) == 1:
            self.ids.player2_name.text = random.choice(constants.COMPUTER_NAMES)
            game_data[constants.HISTORY_PLAYER_2] = self.ids.player2_name.text
        else:
            self.ids.player2_name.text = act_settings[constants.USERNAME_2]
            game_data[constants.HISTORY_PLAYER_2] = act_settings[constants.USERNAME_2]
        game_data[constants.HISTORY_OPPONENT] = int(act_settings[constants.OPPONENT])
        # Init round
        self.ids.player1_round.text = '0 / ' + str(act_settings[constants.ROUNDS])
        self.ids.player2_round.text = '0 / ' + str(act_settings[constants.ROUNDS])
        game_data[constants.HISTORY_SELECTED_ROUNDS] = int(act_settings[constants.ROUNDS])
        # Set the available gestures according to the selected game mode
        global available_gestures
        if int(act_settings[constants.GAME_MODE]) == 1:
            available_gestures = constants.GAME_MODE_1_CHOICES
        elif int(act_settings[constants.GAME_MODE]) == 2:
            available_gestures = constants.GAME_MODE_2_CHOICES
        else:
            available_gestures = constants.GAME_MODE_3_CHOICES
        game_data[constants.HISTORY_GAME_MODE] = int(act_settings[constants.GAME_MODE])
        # Initialize webcam and hand detection module
        self.cap = cv2.VideoCapture(int(settings[constants.SETTINGS_CAMERA_DEVICE_KEY]))
        self.hd = HandDetection(
            min_detection_confidence=float(settings[constants.SETTINGS_MIN_DETECTION_CONFIDENCE_KEY]),
            min_tracking_confidence=float(settings[constants.SETTINGS_MIN_TRACKING_CONFIDENCE_KEY]))

        # Schedule camera frame update
        self.update_schedule = Clock.schedule_interval(self.update, 0.03)

    def update(self, dt):
        if self.cap.isOpened():
            success, image = self.cap.read()
            (processed_image, landmarks) = self.hd.find_hand_positions(image)

            global detected_gesture, detected_gesture_list

            if landmarks:
                data = get_coordinates_by_hand(landmarks, 0, processed_image.shape[1], processed_image.shape[0])
                gesture = recognise_hand_gesture(data)
                # Check if the detected gesture is available in the selected game mode
                if gesture in available_gestures:
                    detected_gesture = gesture
                else:
                    detected_gesture = constants.LOG_CANNOT_RECOGNISE_GESTURE
                detected_gesture_list.append(detected_gesture)
                # print(constants.LOG_TEMPLATE, constants.LOG_PREDICTED_GESTURE, detected_gesture)
            else:
                detected_gesture = constants.LOG_NO_HAND

            buf1 = cv2.flip(processed_image, 0)
            buf = buf1.tostring()
            texture = Texture.create(size=(processed_image.shape[1], processed_image.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            self.ids.camera_frame.texture = texture

            if player_1s_turn and can_show_live_image_p1:
                self.predicted_photo_p1()
                self.predicted_text_p1()
            elif (not player_1s_turn) and (not can_show_live_image_p1) and can_show_live_image_p2 and \
                    int(act_settings[constants.OPPONENT]) != 1:
                self.predicted_photo_p2()
                self.predicted_text_p2()

    async def computer_game(self):
        global player_1s_turn, p1_score, p2_score, available_gestures, can_show_live_image_p1, \
            winner, should_save_history_file
        try:
            self.rounds = 1
            self.rounds_actually = 1
            self.p1_choice = None
            self.p2_choice = None
            while self.rounds != int(act_settings[constants.ROUNDS]) + 1:
                detected_gesture_list.clear()
                self.ids.player1_round.text = str(self.rounds_actually) + ' / ' + str(act_settings[constants.ROUNDS])
                self.ids.player2_round.text = str(self.rounds_actually) + ' / ' + str(act_settings[constants.ROUNDS])
                # Player 1
                self.ids.player1_info.text = constants.YOUR_TURN
                await ak.sleep(3)
                self.ids.player1_info.text = constants.STAY_STILL
                await ak.sleep(2)
                detected_gesture_list.clear()

                for i in reversed(range(5+1)):
                    self.ids.countdown_p1.text = str(i)
                    await ak.sleep(1)
                self.ids.countdown_p1.text = ''
                self.ids.player1_info.text = ''

                gesture_stats = dict()
                for gesture in detected_gesture_list:
                    if gesture not in gesture_stats:
                        gesture_stats[gesture] = 1
                    else:
                        gesture_stats[gesture] = gesture_stats[gesture] + 1
                #
                detected_gesture_list.clear()
                if len(gesture_stats.keys()) < 1:
                    self.p1_choice = constants.LOG_NO_HAND
                else:
                    self.p1_choice = max(gesture_stats.items(), key=operator.itemgetter(1))[0]

                player_1s_turn = False
                can_show_live_image_p1 = False
                self.ids.gesture_image_p1.source = constants.GESTURE_IMAGES[self.p1_choice]
                self.ids.gesture_text_p1.text = self.p1_choice

                # Player 2
                self.ids.player2_info.text = constants.YOUR_TURN
                await ak.sleep(3)
                player_1s_turn = True
                computer_choice = random.choice(available_gestures)
                self.ids.gesture_image_p2.source = constants.GESTURE_IMAGES[computer_choice]
                self.ids.gesture_text_p2.text = computer_choice
                self.p2_choice = computer_choice
                await ak.sleep(3)
                self.ids.player2_info.text = ''
                if self.p1_choice != constants.LOG_CANNOT_RECOGNISE_GESTURE and self.p1_choice != constants.LOG_NO_HAND:
                    if self.p1_choice == self.p2_choice:
                        self.ids.who_won_round.text = constants.DRAW
                        self.rounds_actually += 1
                    elif self.p1_choice in constants.WEAKNESSES[self.p2_choice]:
                        p1_score += 1
                        self.rounds += 1
                        self.rounds_actually += 1
                        self.ids.who_won_round.text = constants.P1_WON
                    elif self.p2_choice in constants.WEAKNESSES[self.p1_choice]:
                        p2_score += 1
                        self.rounds += 1
                        self.rounds_actually += 1
                        self.ids.who_won_round.text = constants.P2_WON
                self.ids.p1_score.text = str(p1_score)
                self.ids.p2_score.text = str(p2_score)
                detected_gesture_list.clear()
                await ak.sleep(5)
                self.ids.who_won_round.text = ''
                can_show_live_image_p1 = True
            if p1_score > p2_score:
                winner = act_settings[constants.USERNAME]
            else:
                winner = 'Computer (' + self.ids.player2_name.text + ')'
            Clock.unschedule(self.game_time_schedule)
        except GeneratorExit:
            should_save_history_file = False
            raise
        finally:
            game_data[constants.HISTORY_PLAYED_ROUNDS] = self.rounds_actually-1
            game_data[constants.HISTORY_PLAYER_1_SCORE] = p1_score
            game_data[constants.HISTORY_PLAYER_2_SCORE] = p2_score
            game_data[constants.HISTORY_WINNER] = winner

    async def other_player_game(self):
        global player_1s_turn, p1_score, p2_score, available_gestures, can_show_live_image_p1, \
            winner, should_save_history_file, can_show_live_image_p2
        try:
            self.rounds = 1
            self.rounds_actually = 1
            self.p1_choice = None
            self.p2_choice = None
            while self.rounds != int(act_settings[constants.ROUNDS]) + 1:
                detected_gesture_list.clear()
                self.ids.player1_round.text = str(self.rounds_actually) + ' / ' + str(act_settings[constants.ROUNDS])
                self.ids.player2_round.text = str(self.rounds_actually) + ' / ' + str(act_settings[constants.ROUNDS])
                # Player 1
                self.ids.player1_info.text = constants.YOUR_TURN
                self.ids.player2_info.text = constants.LOOK_AWAY
                await ak.sleep(5)
                self.ids.player1_info.text = constants.STAY_STILL
                await ak.sleep(2)
                detected_gesture_list.clear()

                for i in reversed(range(5 + 1)):
                    self.ids.countdown_p1.text = str(i)
                    await ak.sleep(1)
                self.ids.countdown_p1.text = ''
                self.ids.player1_info.text = ''

                gesture_stats = dict()
                for gesture in detected_gesture_list:
                    if gesture not in gesture_stats:
                        gesture_stats[gesture] = 1
                    else:
                        gesture_stats[gesture] = gesture_stats[gesture] + 1
                #
                detected_gesture_list.clear()
                if len(gesture_stats.keys()) < 1:
                    self.p1_choice = constants.LOG_NO_HAND
                else:
                    self.p1_choice = max(gesture_stats.items(), key=operator.itemgetter(1))[0]

                ak.sleep(3)

                can_show_live_image_p1 = False

                self.ids.gesture_image_p1.source = constants.GESTURE_IMAGES[self.p1_choice]
                self.ids.gesture_text_p1.text = self.p1_choice

                player_1s_turn = False

                ak.sleep(8)

                can_show_live_image_p2 = True

                # Player 2
                self.ids.player1_info.text = constants.LOOK_AWAY
                self.ids.player2_info.text = constants.YOUR_TURN
                await ak.sleep(5)
                self.ids.player2_info.text = constants.STAY_STILL
                await ak.sleep(2)
                detected_gesture_list.clear()

                for i in reversed(range(5 + 1)):
                    self.ids.countdown_p2.text = str(i)
                    await ak.sleep(1)
                self.ids.countdown_p2.text = ''
                self.ids.player2_info.text = ''

                gesture_stats = dict()
                for gesture in detected_gesture_list:
                    if gesture not in gesture_stats:
                        gesture_stats[gesture] = 1
                    else:
                        gesture_stats[gesture] = gesture_stats[gesture] + 1
                #
                detected_gesture_list.clear()
                if len(gesture_stats.keys()) < 1:
                    self.p2_choice = constants.LOG_NO_HAND
                else:
                    self.p2_choice = max(gesture_stats.items(), key=operator.itemgetter(1))[0]

                can_show_live_image_p2 = False

                self.ids.gesture_image_p2.source = constants.GESTURE_IMAGES[self.p2_choice]
                self.ids.gesture_text_p2.text = self.p2_choice
                ak.sleep(5)

                if self.p1_choice != constants.LOG_CANNOT_RECOGNISE_GESTURE and \
                        self.p1_choice != constants.LOG_NO_HAND and \
                        self.p2_choice != constants.LOG_CANNOT_RECOGNISE_GESTURE and \
                        self.p2_choice != constants.LOG_NO_HAND:
                    if self.p1_choice == self.p2_choice:
                        self.ids.who_won_round.text = constants.DRAW
                        self.rounds_actually += 1
                    elif self.p1_choice in constants.WEAKNESSES[self.p2_choice]:
                        p1_score += 1
                        self.rounds += 1
                        self.rounds_actually += 1
                        self.ids.who_won_round.text = constants.P1_WON
                    elif self.p2_choice in constants.WEAKNESSES[self.p1_choice]:
                        p2_score += 1
                        self.rounds += 1
                        self.rounds_actually += 1
                        self.ids.who_won_round.text = constants.P2_WON
                self.ids.p1_score.text = str(p1_score)
                self.ids.p2_score.text = str(p2_score)
                detected_gesture_list.clear()
                await ak.sleep(5)
                self.ids.who_won_round.text = ''

                self.p1_choice = constants.LOG_NO_HAND
                self.p2_choice = constants.LOG_NO_HAND

                self.ids.gesture_image_p1.source = constants.GESTURE_IMAGES[self.p1_choice]
                self.ids.gesture_text_p1.text = self.p1_choice

                self.ids.gesture_image_p2.source = constants.GESTURE_IMAGES[self.p2_choice]
                self.ids.gesture_text_p2.text = self.p2_choice

                ak.sleep(3)

                player_1s_turn = True
                can_show_live_image_p1 = True
            if p1_score > p2_score:
                winner = act_settings[constants.USERNAME]
            else:
                winner = act_settings[constants.USERNAME_2]
            Clock.unschedule(self.game_time_schedule)
        except GeneratorExit:
            should_save_history_file = False
            raise
        finally:
            game_data[constants.HISTORY_PLAYED_ROUNDS] = self.rounds_actually - 1
            game_data[constants.HISTORY_PLAYER_1_SCORE] = p1_score
            game_data[constants.HISTORY_PLAYER_2_SCORE] = p2_score
            game_data[constants.HISTORY_WINNER] = winner

    def init_countdown(self, dt):
        if self.init_countdown_cnt > 0:
            self.ids.countdown_p1.text = str(self.init_countdown_cnt)
            self.ids.countdown_p2.text = str(self.init_countdown_cnt)
            self.init_countdown_cnt -= 1
        elif self.init_countdown_cnt == 0:
            self.ids.countdown_p1.text = ''
            self.ids.countdown_p2.text = ''
            self.ids.player1_info.text = constants.GET_READY
            self.ids.player2_info.text = constants.GET_READY

    def computer_task_helper(self, dt):
        self.computer_game_task = ak.start(self.computer_game())

    def other_player_task_helper(self, dt):
        self.other_game_task = ak.start(self.other_player_game())

    def on_enter(self, *args):
        # Increase game time
        self.game_time_schedule = Clock.schedule_interval(incr_game_time, 1)
        # Initial countdown
        self.init_cntdwn = Clock.schedule_interval(self.init_countdown, 1)
        Clock.schedule_once(lambda l: Clock.unschedule(self.init_cntdwn), 7)
        # Game should start according to the selected opponent
        if int(act_settings[constants.OPPONENT]) == 1:
            self.computer_game_schedule = Clock.schedule_once(self.computer_task_helper, 7)
        else:
            self.other_player_schedule = Clock.schedule_once(self.other_player_task_helper, 7)
            pass
        self.finished_schedule = Clock.schedule_interval(self.is_finished, 2)

    def is_finished(self, dt):
        if winner:
            App.get_running_app().root.current = 'scoreboard'

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

    def cancel_things(self, instance):
        global should_save_history_file, game_data, game_time_in_secs
        Clock.unschedule(self.game_time_schedule)
        game_data[constants.HISTORY_PLAY_TIME] = game_time_in_secs
        Clock.unschedule(self.update_schedule)
        Clock.unschedule(self.finished_schedule)
        if game_time_in_secs < 7:
            Clock.unschedule(self.init_cntdwn)
            if int(act_settings[constants.OPPONENT]) == 1:
                Clock.unschedule(self.computer_game_schedule)
            else:
                Clock.unschedule(self.other_player_schedule)
            should_save_history_file = False
        else:
            if int(act_settings[constants.OPPONENT]) == 1:
                self.computer_game_task.cancel()
            else:
                self.other_game_task.cancel()

    def on_pre_leave(self, *args):
        self.cancel_things(None)
        global p1_score, p2_score, can_show_live_image_p1, winner, game_time_in_secs
        self.cap.release()
        Clock.schedule_once(self.init)
        global detected_gesture, player_1s_turn, available_gestures, act_settings, settings
        detected_gesture = None
        detected_gesture_list.clear()
        p1_score = 0
        p2_score = 0
        game_time_in_secs = 0
        winner = None
        can_show_live_image_p1 = True
        player_1s_turn = True
        if should_save_history_file:
            now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            game_data[constants.HISTORY_TIME] = now
            history_filename_with_path = constants.HISTORY_RELATIVE_PATH + now + constants.HISTORY_FILENAME_ENDING
            json_str = dumps(game_data)
            with open(history_filename_with_path, 'w') as history_file:
                history_file.write(json_str)
            #
