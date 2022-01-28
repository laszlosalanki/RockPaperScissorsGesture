# Rock Paper Scissors Gesture

## Description

This is a simple Python and Kivy based Rock Paper Scissors game. It's main feature's that
it can recognise hand gestures using a webcam.
The idea, gestures and the rules came from the well-known **The Big Bang Theory** series.
Source: http://bigbangtheory.lapunk.hu/?modul=oldal&tartalom=1195704

### There are three featured gamemodes:
- Rock Paper Scissors (Gamemode 1)
- Rock Paper Scissors Lizard Spock (Gamemode 2)
- Rock Paper Scissors Lizard Spock Wizard Batman Spiderman Glock (Gamemode 3)

![Gameplay](docs/images/screen_1.png)

### Rules:
- Gamemode 1:
    - Scissors > Paper
    - Paper > Rock
    - Rock > Scissors
- Gamemode 2:
    - Scissors > Paper
    - Paper > Rock
    - Rock > Scissors
    - Rock > Lizard
    - Lizard > Spock
    - Spock > Scissors
    - Scissors > Lizard
    - Lizard > Paper
    - Paper > Spock
    - Spock > Rock 
- Gamemode 3:
    - Scissors > Paper
    - Paper > Rock
    - Rock > Scissors
    - Rock > Lizard
    - Lizard > Spock
    - Spock > Scissors
    - Scissors > Lizard
    - Lizard > Paper
    - Paper > Spock
    - Spock > Rock
    - Spock > Wizard
    - Wizard > Batman
    - Batman > Spiderman
    - Spiderman > Glock
    - Glock > Rock
    - Rock > Wizard
    - Wizard > Paper
    - Spock > Spiderman
    - Spiderman > Lizard
    - Lizard > Batman
    - Scissors > Wizard
    - Wizard > Lizard
    - Paper > Glock
    - Glock > Batman
    - Batman > Rock
    - Lizard > Glock
    - Glock > Spock
    - Rock > Spiderman
    - Spiderman > Paper
    - Paper > Batman
    - Batman > Spock
    - Scissors > Spiderman
    - Spiderman > Wizard
    - Wizard > Glock
    - Glock > Scissors

## Install prerequisites

- Kivy:
    ````````````````````````````````
    python -m pip install kivy[base]
    ````````````````````````````````

- OpenCV 2:
    ```````````````````````````````````
    python -m pip install opencv-python
    ```````````````````````````````````

- MediaPipe:
    ````````````````````````````````
    python -m pip install mediapipe
    ````````````````````````````````

- AsyncKivy:
    ```````````````````````````````
    python -m pip install asynckivy
    ```````````````````````````````

## Run

``````````````
python main.py
``````````````

## Used for development: 
- **PyCharm Community Edition 2021.2.3**
- **Python 3.7**

## Used Python packages:
- [Kivy 2.0.0](https://kivy.org/#home)
- [OpenCV 2](https://opencv.org)
- [MediaPipe](https://mediapipe.dev/)
- [AsyncKivy](https://github.com/gottadiveintopython/asynckivy)

## Image sources:
- Gestures: [Imgur](https://imgur.com/gallery/vKzEw12)
- Images: [KindPNG](https://www.kindpng.com/)
