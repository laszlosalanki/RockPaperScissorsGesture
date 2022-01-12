# Window
TITLE = 'Rock Paper Scissor Gesture'

# Console
LOG_TEMPLATE = '[LOG]'

# Log
LOG_GAME_MODE_SELECTED = 'Selected game mode:'
LOG_OPPONENT_SELECTED = 'Selected opponent:'
LOG_DIFFICULTY_SELECTED = 'Selected difficulty:'
LOG_ACT_GAME_SETTINGS_FILE_UPDATED = 'Actual game settings file updated.'
LOG_ACT_GAME_SETTINGS_FILE_CREATED = 'Actual game settings file created.'
LOG_ACT_GAME_SETTINGS_FILE_DELETED = 'Actual game settings file deleted.'
LOG_PREDICTED_GESTURE = 'Predicted gesture:'
LOG_CANNOT_RECOGNISE_GESTURE = 'Gesture cannot be recognised.'
LOG_NO_HAND = 'No hand detected.'

# Supported gestures
# Game mode 1
ROCK = 'rock'
PAPER = 'paper'
SCISSOR = 'scissor'
# Game mode 2
LIZARD = 'lizard'
SPOCK = 'spock'
# Game mode 3
WIZARD = 'wizard'
BATMAN = 'batman'
SPIDERMAN = 'spiderman'
GLOCK = 'glock'

# File
ACT_GAME_SETTINGS_FILE_NAME = 'ACT_TMP_SETTINGS'
ACT_GAME_SETTINGS_RELATIVE_PATH = 'data/'
ACT_GAME_SETTINGS_HEADER = 'Actual game settings'

# Act settings keys
GAME_MODE = 'GAME_MODE: '
OPPONENT = 'OPPONENT: '
DIFFICULTY = 'DIFFICULTY: '

# Settings
SETTINGS_FILE_NAME = 'game.settings'
SETTINGS_FILE_RELATIVE_PATH = 'data/'
SETTINGS_HEADER = 'Settings'

SETTINGS_IS_LOGGING_ENABLED_KEY = 'LOGGING: '
SETTINGS_IS_LOGGING_ENABLED_DEFAULT_VALUE = True

SETTINGS_MIN_DETECTION_CONFIDENCE_KEY = 'MIN_DETECTION_CONFIDENCE: '
SETTINGS_MIN_DETECTION_CONFIDENCE_DEFAULT_VALUE = 0.5

SETTINGS_MIN_TRACKING_CONFIDENCE_KEY = 'MIN_TRACKING_CONFIDENCE: '
SETTINGS_MIN_TRACKING_CONFIDENCE_DEFAULT_VALUE = 0.5

# Gesture images
GESTURE_IMAGES_PATH = 'D:/Downloads/egyetem/hatodik/szakdolgozat/img/'
GESTURE_IMAGES = {
    'rock': GESTURE_IMAGES_PATH + 'rock.png',
    'paper': GESTURE_IMAGES_PATH + 'paper.png',
    'scissor': GESTURE_IMAGES_PATH + 'scissor.png',
    'glock': GESTURE_IMAGES_PATH + 'glock.png',
    'spock': GESTURE_IMAGES_PATH + 'spock.png',
    'wizard': GESTURE_IMAGES_PATH + 'wizard.png',
    'lizard': GESTURE_IMAGES_PATH + 'lizard.png',
    'spiderman': GESTURE_IMAGES_PATH + 'spiderman.png',
    'batman': GESTURE_IMAGES_PATH + 'batman.png',
    LOG_CANNOT_RECOGNISE_GESTURE: GESTURE_IMAGES_PATH + 'image-not-found.png',
    LOG_NO_HAND: GESTURE_IMAGES_PATH + 'image-not-found.png'
}
