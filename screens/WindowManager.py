from kivy.uix.screenmanager import ScreenManager, WipeTransition


class WindowManager(ScreenManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = WipeTransition()
