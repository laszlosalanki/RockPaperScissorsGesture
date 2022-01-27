from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from data import constants


class ClickableBoxLayout(ButtonBehavior, BoxLayout):

    def __init__(self, **kwargs):
        self.gesture = None
        super().__init__(**kwargs)


class HelpWindow(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.create_gesture_items)

    def help_item_press(self, instance):
        popup = Popup(size=(600, 400), size_hint=(None, None), title=instance.gesture.capitalize())

        box_layout_main = BoxLayout(orientation='vertical')
        box_layout_main.add_widget(Label(text='Properties', font_size=24, size_hint_y=0.2))

        # Container to hold weaknesses and strengths
        box_layout_content = BoxLayout(orientation='horizontal')

        # Weaknesses
        box_layout_left = BoxLayout(orientation='vertical', spacing=10, padding=20)
        box_layout_left.add_widget(Label(text='Weaknesses', font_size=16))
        box_layout_left.add_widget(Label())
        for weakness in constants.WEAKNESSES[instance.gesture]:
            weakness_label = Label(text=weakness, color=(1, 0, 0, 1))
            box_layout_left.add_widget(weakness_label)

        # Strengths
        box_layout_right = BoxLayout(orientation='vertical', spacing=10, padding=20)
        box_layout_right.add_widget(Label(text='Strengths', font_size=16))
        box_layout_right.add_widget(Label())
        for strength in constants.STRENGTHS[instance.gesture]:
            strength_label = Label(text=strength, color=(0, 0.5, 0, 1))
            box_layout_right.add_widget(strength_label)

        box_layout_content.add_widget(box_layout_left)
        box_layout_content.add_widget(box_layout_right)

        box_layout_main.add_widget(box_layout_content)
        close_button = Button(text='Close', size_hint_y=0.2)
        close_button.bind(on_release=popup.dismiss)
        box_layout_main.add_widget(close_button)

        popup.content = box_layout_main
        popup.open()

    def create_gesture_items(self, dt):
        for gesture in constants.GAME_MODE_3_CHOICES:
            container = ClickableBoxLayout(orientation='horizontal', size_hint_y=None, spacing=10, padding=20)
            container.gesture = gesture
            container.bind(on_press=self.help_item_press)
            img = Image(source=constants.GESTURE_HAND_IMAGES[gesture])
            txt = Label(text=gesture)
            container.add_widget(img)
            container.add_widget(txt)
            self.ids.gesture_help_item_holder.add_widget(container)
