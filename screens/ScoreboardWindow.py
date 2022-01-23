from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from os import listdir, remove
from os.path import isfile, join, abspath
from json import load

from data import constants


files = list()


def read_dir_content():
    global files
    path = abspath(constants.HISTORY_RELATIVE_PATH)
    files = [join(path, f) for f in listdir(path) if isfile(join(path, f)) and f.endswith('json')]
    files.sort(reverse=True)


def read_file(file):
    with open(file, 'r') as history_file:
        file_content = load(history_file)
    #
    if file_content is None:
        file_content = dict()
    return file_content


class ScoreboardWindow(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.bind_clear_button)

    def bind_clear_button(self, dt):
        self.ids.clear_history_button.bind(on_release=self.on_clear_click)

    def on_clear_click(self, instance):
        for file in files:
            remove(file)
        App.get_running_app().root.current = 'main'

    def on_pre_enter(self, *args):
        self.__init__()
        Clock.schedule_once(self.fill_screen)

    def fill_screen(self, dt):
        read_dir_content()
        for file in files:
            file_content = read_file(file)
            line = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
            time = Label(text=file_content[constants.HISTORY_TIME], font_size=14)
            play_time = Label(text=str(file_content[constants.HISTORY_PLAY_TIME]), font_size=14)
            p1_name = Label(text=file_content[constants.HISTORY_PLAYER_1], font_size=14)
            p1_score = Label(text=str(file_content[constants.HISTORY_PLAYER_1_SCORE]), font_size=14)
            p2_name = Label(text=file_content[constants.HISTORY_PLAYER_2], font_size=14)
            p2_score = Label(text=str(file_content[constants.HISTORY_PLAYER_2_SCORE]), font_size=14)
            winner = Label(text=file_content[constants.HISTORY_WINNER], font_size=14)
            rounds_played = Label(text=str(file_content[constants.HISTORY_PLAYED_ROUNDS]), font_size=14)
            line.add_widget(time)
            line.add_widget(play_time)
            line.add_widget(p1_name)
            line.add_widget(p1_score)
            line.add_widget(p2_name)
            line.add_widget(p2_score)
            line.add_widget(winner)
            line.add_widget(rounds_played)
            self.ids.history_container.add_widget(line)

    def on_leave(self, *args):
        self.ids.history_scroll.remove_widget(self.ids.history_container)
