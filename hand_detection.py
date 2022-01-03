import cv2
import mediapipe as mp

from data import constants

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


class HandDetection:
    def __init__(self, static_image_mode=False, max_num_hands=2,
                 min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.hands = mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence)

    def find_hand_positions(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = self.hands.process(img)
        if res.multi_hand_landmarks:
            for lm in res.multi_hand_landmarks:
                mp_drawing.draw_landmarks(img, lm, mp_hands.HAND_CONNECTIONS)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = cv2.flip(img, 1)
        return img, res.multi_hand_landmarks

    def find_hand_positions_plain(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = self.hands.process(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = cv2.flip(img, 1)
        return img, res.multi_hand_landmarks


#############################################################
# Gestures

def is_rock(positions):
    return (positions[8][2] > positions[6][2]) and \
           (positions[12][2] > positions[10][2]) and \
           (positions[16][2] > positions[14][2]) and \
           (positions[20][2] > positions[18][2])


def is_paper(positions):
    return (positions[8][2] < positions[6][2]) and \
           (positions[12][2] < positions[10][2]) and \
           (positions[16][2] < positions[14][2]) and \
           (positions[20][2] < positions[18][2])


def is_scissor(positions):
    return (positions[8][2] < positions[6][2]) and \
           (positions[8][2] < positions[6][2]) and \
           not is_paper(positions)


def is_spiderman(positions):
    return (positions[8][2] < positions[6][2]) and \
           (positions[20][2] < positions[18][2]) and \
           (positions[12][2] > positions[10][2]) and \
           (positions[16][2] > positions[14][2])


def is_batman(positions):
    return (positions[4][2] < positions[3][2]) and \
           (positions[20][2] < positions[18][2]) and \
           (positions[8][2] > positions[6][2]) and \
           (positions[12][2] > positions[10][2]) and \
           (positions[16][2] > positions[14][2])


def is_spock(positions):
    tip_distance = positions[16][1] - positions[12][1]
    return is_paper(positions) and tip_distance > 50.0


def is_glock(positions):
    return (positions[8][2] < positions[6][2]) and \
           (positions[4][2] < positions[3][2]) and \
           (positions[12][2] > positions[10][2]) and \
           (positions[16][2] > positions[14][2]) and \
           (positions[20][2] > positions[18][2])


def get_coordinates_by_hand(data, hand_no, img_w, img_h):
    hand_landmarks = data[hand_no]
    data = list()
    for id, lm in enumerate(hand_landmarks.landmark):
        data.append([id, int(lm.x * img_w), int(lm.y * img_h), lm.z])
    return data


def recognise_hand_gesture(positions):
    if is_spiderman(positions):
        return constants.SPIDERMAN
    elif is_batman(positions):
        return constants.BATMAN
    elif is_glock(positions):
        return constants.GLOCK
    elif is_scissor(positions):
        return constants.SCISSOR
    elif is_rock(positions):
        return constants.ROCK
    elif is_spock(positions):
        return constants.SPOCK
    elif is_paper(positions):
        return constants.PAPER
    else:
        return constants.LOG_CANNOT_RECOGNISE_GESTURE
#############################################################


if __name__ == '__main__':
    hd = HandDetection()
    capture = cv2.VideoCapture(0)
    while capture.isOpened():
        success, image = capture.read()
        if not success:
            print("Ignoring empty camera frame")
            continue

        (processed_image, landmarks) = hd.find_hand_positions(image)

        if landmarks:
            data = get_coordinates_by_hand(landmarks, 0, processed_image.shape[1], processed_image.shape[0])
            print(recognise_hand_gesture(data))

        cv2.imshow('Hand detection test', processed_image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
    capture.release()
