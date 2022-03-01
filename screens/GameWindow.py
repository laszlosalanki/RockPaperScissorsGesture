import operator
import random
from datetime import datetime
from json import dumps

import asynckivy as ak
from cv2 import cv2
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from data import constants
from hand_detection import HandDetection, get_coordinates_by_hand, recognise_hand_gesture, which_players_hand
from settings_file_helper import read_into_dict

player_1s_turn = True

available_gestures = list()

can_show_live_image_p1 = True

should_save_history_file = True
should_draw_handmarks = True

can_show_live_image_other_player_mode = True
detected_gesture_p1 = None
detected_gesture_list_p1 = list()
detected_gesture_p2 = None
detected_gesture_list_p2 = list()

game_data = dict()

winner = None
p1_score = 0
p2_score = 0

game_time_in_secs = 0

act_settings = dict()
settings = dict()

act_settings_filename = constants.ACT_GAME_SETTINGS_RELATIVE_PATH + constants.ACT_GAME_SETTINGS_FILE_NAME
settings_filename = constants.SETTINGS_FILE_RELATIVE_PATH + constants.SETTINGS_FILE_NAME


def incr_game_time(dt):
    global game_time_in_secs
    game_time_in_secs += 1


async def handle_error():
    error = Popup(title='Error', text='Could not open camera feed')
    error.open()
    await ak.sleep(5)
    error.dismiss()
    App.get_running_app().root.current = 'main'


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
        self.ids.p1_score.text = str(p1_score)
        self.ids.p2_score.text = str(p2_score)
        # Counter for initial countdown
        self.init_countdown_cnt = 5
        # Bind the cancel button
        self.ids.game_main_button.bind(on_press=self.cancel_things)

    def on_pre_enter(self, *args):
        # Run init again (in case of the game was cancelled before)
        Clock.schedule_once(self.init)
        # Read ACT_SETTINGS file
        global act_settings, settings, game_data, available_gestures, should_draw_handmarks
        act_settings = read_into_dict(act_settings_filename)
        settings = read_into_dict(settings_filename)
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
        if int(act_settings[constants.GAME_MODE]) == 1:
            available_gestures = constants.GAME_MODE_1_CHOICES
        elif int(act_settings[constants.GAME_MODE]) == 2:
            available_gestures = constants.GAME_MODE_2_CHOICES
        else:
            available_gestures = constants.GAME_MODE_3_CHOICES
        game_data[constants.HISTORY_GAME_MODE] = int(act_settings[constants.GAME_MODE])
        # Initialize webcam and hand detection module
        self.cap = cv2.VideoCapture(int(settings[constants.SETTINGS_CAMERA_DEVICE_KEY]))
        if int(act_settings[constants.OPPONENT]) == 1:
            self.hd = HandDetection(
                min_detection_confidence=float(settings[constants.SETTINGS_MIN_DETECTION_CONFIDENCE_KEY]),
                min_tracking_confidence=float(settings[constants.SETTINGS_MIN_TRACKING_CONFIDENCE_KEY]))
        else:
            self.hd = HandDetection(
                min_detection_confidence=float(settings[constants.SETTINGS_MIN_DETECTION_CONFIDENCE_KEY]),
                min_tracking_confidence=float(settings[constants.SETTINGS_MIN_TRACKING_CONFIDENCE_KEY]),
                max_num_hands=2)

        # Schedule camera frame update
        if settings[constants.SETTINGS_SHOULD_DRAW_HANDMARKS_KEY] == 'True':
            should_draw_handmarks = True
        else:
            should_draw_handmarks = False
        self.update_schedule = Clock.schedule_interval(self.update, 0.03)

    def update(self, dt):
        if self.cap.isOpened():
            success, image = self.cap.read()
            processed_image, landmarks = self.hd.find_hand_positions(image, should_draw=should_draw_handmarks)

            global detected_gesture_p1, detected_gesture_p2, \
                detected_gesture_list_p1, detected_gesture_list_p2

            if int(act_settings[constants.OPPONENT]) == 1:
                if landmarks:
                    data = get_coordinates_by_hand(landmarks, 0, processed_image.shape[1], processed_image.shape[0])
                    gesture = recognise_hand_gesture(data)
                    # Check if the detected gesture is available in the selected game mode
                    if gesture in available_gestures:
                        detected_gesture_p1 = gesture
                    else:
                        detected_gesture_p1 = constants.LOG_CANNOT_RECOGNISE_GESTURE
                    detected_gesture_list_p1.append(detected_gesture_p1)

                else:
                    detected_gesture_p1 = constants.LOG_NO_HAND
                # Only show live image, when should
                if can_show_live_image_p1:
                    self.ids.gesture_image_p1.source = constants.GESTURE_IMAGES[detected_gesture_p1]
                    self.ids.gesture_text_p1.text = detected_gesture_p1
            else:
                if landmarks:
                    data_dict = which_players_hand(landmarks, processed_image.shape[1], processed_image.shape[0])
                    # If the two hands aren't on the same side
                    if data_dict:
                        # If both hands could be found
                        if constants.PLAYER1 in data_dict.keys() and constants.PLAYER2 in data_dict.keys():
                            player_1_gesture = recognise_hand_gesture(data_dict[constants.PLAYER1])
                            player_2_gesture = recognise_hand_gesture(data_dict[constants.PLAYER2])
                            if player_1_gesture in available_gestures:
                                detected_gesture_p1 = player_1_gesture
                            else:
                                detected_gesture_p1 = constants.LOG_CANNOT_RECOGNISE_GESTURE
                            if player_2_gesture in available_gestures:
                                detected_gesture_p2 = player_2_gesture
                            else:
                                detected_gesture_p2 = constants.LOG_CANNOT_RECOGNISE_GESTURE
                            detected_gesture_list_p1.append(detected_gesture_p1)
                            detected_gesture_list_p2.append(detected_gesture_p2)

                            if can_show_live_image_other_player_mode:
                                self.ids.gesture_image_p1.source = constants.GESTURE_IMAGES[detected_gesture_p1]
                                self.ids.gesture_image_p2.source = constants.GESTURE_IMAGES[detected_gesture_p2]
                                self.ids.gesture_text_p1.text = detected_gesture_p1
                                self.ids.gesture_text_p2.text = detected_gesture_p2
                        # If only Player 1's hand could be found
                        elif constants.PLAYER1 in data_dict.keys() and constants.PLAYER2 not in data_dict.keys():
                            player_1_gesture = recognise_hand_gesture(data_dict[constants.PLAYER1])
                            detected_gesture_p2 = constants.LOG_NO_HAND
                            if player_1_gesture in available_gestures:
                                detected_gesture_p1 = player_1_gesture
                            else:
                                detected_gesture_p1 = constants.LOG_CANNOT_RECOGNISE_GESTURE
                            detected_gesture_list_p1.append(detected_gesture_p1)
                            detected_gesture_list_p2.append(detected_gesture_p2)

                            if can_show_live_image_other_player_mode:
                                self.ids.gesture_image_p1.source = constants.GESTURE_IMAGES[detected_gesture_p1]
                                self.ids.gesture_image_p2.source = constants.GESTURE_IMAGES[constants.LOG_NO_HAND]
                                self.ids.gesture_text_p1.text = detected_gesture_p1
                                self.ids.gesture_text_p2.text = constants.LOG_NO_HAND
                        # If only Player 2's hand could be found
                        else:
                            player_2_gesture = recognise_hand_gesture(data_dict[constants.PLAYER2])
                            detected_gesture_p1 = constants.LOG_NO_HAND
                            if player_2_gesture in available_gestures:
                                detected_gesture_p2 = player_2_gesture
                            else:
                                detected_gesture_p2 = constants.LOG_CANNOT_RECOGNISE_GESTURE
                            detected_gesture_list_p1.append(detected_gesture_p1)
                            detected_gesture_list_p2.append(detected_gesture_p2)

                            if can_show_live_image_other_player_mode:
                                self.ids.gesture_image_p1.source = constants.GESTURE_IMAGES[constants.LOG_NO_HAND]
                                self.ids.gesture_image_p2.source = constants.GESTURE_IMAGES[detected_gesture_p2]
                                self.ids.gesture_text_p1.text = constants.LOG_NO_HAND
                                self.ids.gesture_text_p2.text = detected_gesture_p2
                    # If both hands are on the same side
                    else:
                        detected_gesture_p1 = constants.LOG_NO_HAND
                        detected_gesture_p2 = constants.LOG_NO_HAND
                        self.ids.gesture_image_p1.source = constants.GESTURE_IMAGES[detected_gesture_p1]
                        self.ids.gesture_image_p2.source = constants.GESTURE_IMAGES[detected_gesture_p2]
                        self.ids.gesture_text_p1.text = detected_gesture_p1
                        self.ids.gesture_text_p2.text = detected_gesture_p2
                # If no hands could be found at all
                else:
                    detected_gesture_p1 = constants.LOG_NO_HAND
                    detected_gesture_p2 = constants.LOG_NO_HAND
                    if can_show_live_image_other_player_mode:
                        self.ids.gesture_image_p1.source = constants.GESTURE_IMAGES[detected_gesture_p1]
                        self.ids.gesture_image_p2.source = constants.GESTURE_IMAGES[detected_gesture_p2]
                        self.ids.gesture_text_p1.text = detected_gesture_p1
                        self.ids.gesture_text_p2.text = detected_gesture_p2

            buf1 = cv2.flip(processed_image, 0)
            buf = buf1.tostring()
            texture = Texture.create(size=(processed_image.shape[1], processed_image.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            self.ids.camera_frame.texture = texture
        else:
            ak.start(handle_error())

    async def computer_game(self):
        global player_1s_turn, p1_score, p2_score, available_gestures, can_show_live_image_p1, \
            winner, should_save_history_file
        try:
            self.rounds = 1
            self.rounds_actually = 1
            self.p1_choice = None
            self.p2_choice = None
            while self.rounds != int(act_settings[constants.ROUNDS]) + 1:
                detected_gesture_list_p1.clear()
                self.ids.player1_round.text = str(self.rounds_actually) + ' / ' + str(act_settings[constants.ROUNDS])
                self.ids.player2_round.text = str(self.rounds_actually) + ' / ' + str(act_settings[constants.ROUNDS])
                # Player 1
                self.ids.player1_info.text = constants.YOUR_TURN
                await ak.sleep(3)
                self.ids.player1_info.text = constants.STAY_STILL
                await ak.sleep(2)
                detected_gesture_list_p1.clear()

                for i in reversed(range(5+1)):
                    self.ids.countdown_p1.text = str(i)
                    await ak.sleep(1)
                self.ids.countdown_p1.text = ''
                self.ids.player1_info.text = ''

                gesture_stats = dict()
                for gesture in detected_gesture_list_p1:
                    if gesture not in gesture_stats:
                        gesture_stats[gesture] = 1
                    else:
                        gesture_stats[gesture] = gesture_stats[gesture] + 1
                #
                detected_gesture_list_p1.clear()
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
                detected_gesture_list_p1.clear()
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
        global p1_score, p2_score, available_gestures, \
            winner, should_save_history_file, can_show_live_image_other_player_mode
        try:
            self.rounds = 1
            self.rounds_actually = 1
            self.p1_choice = None
            self.p2_choice = None
            while self.rounds != int(act_settings[constants.ROUNDS]) + 1:
                detected_gesture_list_p1.clear()
                detected_gesture_list_p2.clear()
                self.ids.player1_round.text = str(self.rounds_actually) + ' / ' + str(act_settings[constants.ROUNDS])
                self.ids.player2_round.text = str(self.rounds_actually) + ' / ' + str(act_settings[constants.ROUNDS])

                self.ids.player1_info.text = constants.PREPARE
                self.ids.player2_info.text = constants.PREPARE

                await ak.sleep(5)

                self.ids.player1_info.text = constants.STAY_STILL
                self.ids.player2_info.text = constants.STAY_STILL

                await ak.sleep(2)

                detected_gesture_list_p1.clear()
                detected_gesture_list_p2.clear()

                for i in reversed(range(5 + 1)):
                    self.ids.countdown_p1.text = str(i)
                    self.ids.countdown_p2.text = str(i)
                    await ak.sleep(1)
                self.ids.countdown_p1.text = ''
                self.ids.countdown_p2.text = ''
                self.ids.player1_info.text = ''
                self.ids.player2_info.text = ''

                # Player 1
                gesture_stats = dict()
                for gesture in detected_gesture_list_p1:
                    if gesture not in gesture_stats:
                        gesture_stats[gesture] = 1
                    else:
                        gesture_stats[gesture] = gesture_stats[gesture] + 1
                #
                detected_gesture_list_p1.clear()
                if len(gesture_stats.keys()) < 1:
                    self.p1_choice = constants.LOG_NO_HAND
                else:
                    self.p1_choice = max(gesture_stats.items(), key=operator.itemgetter(1))[0]

                # Player 2

                gesture_stats = dict()
                for gesture in detected_gesture_list_p2:
                    if gesture not in gesture_stats:
                        gesture_stats[gesture] = 1
                    else:
                        gesture_stats[gesture] = gesture_stats[gesture] + 1
                #
                detected_gesture_list_p2.clear()
                if len(gesture_stats.keys()) < 1:
                    self.p2_choice = constants.LOG_NO_HAND
                else:
                    self.p2_choice = max(gesture_stats.items(), key=operator.itemgetter(1))[0]

                can_show_live_image_other_player_mode = False

                self.ids.gesture_image_p1.source = constants.GESTURE_IMAGES[self.p1_choice]
                self.ids.gesture_image_p2.source = constants.GESTURE_IMAGES[self.p2_choice]
                self.ids.gesture_text_p1.text = self.p1_choice
                self.ids.gesture_text_p2.text = self.p2_choice

                await ak.sleep(5)

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
                else:
                    self.rounds_actually += 1
                self.ids.p1_score.text = str(p1_score)
                self.ids.p2_score.text = str(p2_score)

                detected_gesture_list_p1.clear()
                detected_gesture_list_p2.clear()

                await ak.sleep(5)

                self.ids.who_won_round.text = ''

                self.p1_choice = constants.LOG_NO_HAND
                self.p2_choice = constants.LOG_NO_HAND

                self.ids.gesture_image_p1.source = constants.GESTURE_IMAGES[self.p1_choice]
                self.ids.gesture_text_p1.text = self.p1_choice

                self.ids.gesture_image_p2.source = constants.GESTURE_IMAGES[self.p2_choice]
                self.ids.gesture_text_p2.text = self.p2_choice

                await ak.sleep(3)

                can_show_live_image_other_player_mode = True
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
        global player_1s_turn, available_gestures, act_settings, settings, detected_gesture_p1, detected_gesture_p2
        detected_gesture_p1 = None
        detected_gesture_p2 = None
        detected_gesture_list_p1.clear()
        detected_gesture_list_p2.clear()
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
