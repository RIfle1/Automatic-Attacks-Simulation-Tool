from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput


class ConsoleView(GridLayout):
    def __init__(self, **kwargs):
        super(ConsoleView, self).__init__(**kwargs)
        self.cols = 1

        self.text_area = TextInput(
            hint_text="Console",
            multiline=True,
            readonly=True,
            size_hint=(1, 1)
        )
        self.add_widget(self.text_area)

    def add_text_schedule(self, text):
        Clock.schedule_once(lambda dt: self.add_text(text))

    def add_text(self, text):
        self.text_area.text += text + '\n'
        self.text_area.scroll_y = 0
