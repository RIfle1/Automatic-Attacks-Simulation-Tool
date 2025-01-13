from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

from gui.global_variables import default_font_size, default_button_height
from gui.utils.custom_layout import CustomHeightLayout


class ConsoleView(GridLayout):
    def __init__(self, hint_text, button_text, **kwargs):
        super(ConsoleView, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 2

        self.text_area = TextInput(
            hint_text=hint_text,
            multiline=True,
            readonly=True,
            size_hint=(1, 1),
            font_size=default_font_size
        )

        clear_button_layout = CustomHeightLayout(height=default_button_height)
        self.clear_console_button = Button(text=button_text)
        self.clear_console_button.bind(on_press=self.clear_console)
        clear_button_layout.add_widget(self.clear_console_button)

        self.add_widget(self.text_area)
        self.add_widget(clear_button_layout)

    def add_text_schedule(self, text):
        Clock.schedule_once(lambda dt: self.add_text(text))

    def add_text(self, text):
        self.text_area.text += text + '\n'
        self.text_area.scroll_y = 0

    def clear_console(self, instance):
        self.text_area.text = ''
