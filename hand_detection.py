import cv2
import mediapipe as mp

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

    def find_hand_positions(self, img, log=True, land_mark=True, lines=False):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = self.hands.process(img)
        if res.multi_hand_landmarks:
            if log:
                print(res.multi_hand_landmarks)
            if lines:
                for lm in res.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(img, lm, mp_hands.HAND_CONNECTIONS)
            elif land_mark:
                for lm in res.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(img, lm)
        return img


#############################################################


if __name__ == '__main__':
    hd = HandDetection()
    capture = cv2.VideoCapture(0)
    while capture.isOpened():
        success, image = capture.read()
        if not success:
            print("Ignoring empty camera frame")
            continue

        processed_image = hd.find_hand_positions(image, True, True, True)

        cv2.imshow('Hand detection test', cv2.flip(processed_image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break
    capture.release()
