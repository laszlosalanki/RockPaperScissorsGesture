# from kivy.app import App
# from kivy.lang import Builder
# from kivy.uix.button import Button
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.label import Label
# from kivy.config import Config
# from kivy.uix.popup import Popup
# from kivy.uix.textinput import TextInput
# from kivy.uix.widget import Widget
# from kivy.core.window import Window
#
# kv_file = Builder.load_file('rockpaperscissor.kv')
#
#
# class Widgets(Widget):
#     pass
#
#
# class RockPaperScissorApp(App):
#
#     def build(self):
#         return Widgets()
#
#     def set_res(self, instance):
#         Window.size = (int(self.width_input.text), int(self.height_input.text))
#         self.popup.dismiss()
#
#     def on_start(self):
#         layout = GridLayout(cols=1, rows=3, row_force_default=True, row_default_height=40, spacing=10)
#
#         self.width_input = TextInput(hint_text='Width', multiline=False, input_filter='int')
#         self.height_input = TextInput(hint_text='Height', multiline=False, input_filter='int')
#
#         btn_set_res = Button(text='Set', on_press=self.set_res)
#
#         layout.add_widget(self.width_input)
#         layout.add_widget(self.height_input)
#         layout.add_widget(btn_set_res)
#
#         self.popup = Popup(title='Resolution',
#                            content=layout,
#                            size_hint=(None, None), size=(400, 200))
#         self.popup.open()
#
#
# if __name__ == '__main__':
#     RockPaperScissorApp().run()
