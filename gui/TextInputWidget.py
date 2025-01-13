from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from gui.custom_layout import CustomHeightLayout
from gui.global_variables import default_font_size, title_font_size


class TextInputWidget(GridLayout):
    def __init__(self, text, label_text, hint_text, input_filter=None, **kwargs):
        super(TextInputWidget, self).__init__(**kwargs)
        self.text = label_text
        self.cols = 1
        self.rows = 2
        self.size_hint_y = None
        self.height = 60

        label_layout = CustomHeightLayout()
        label = Label(
            text=label_text,
            font_size=title_font_size,
        )
        label_layout.add_widget(label)

        text_input_layout = CustomHeightLayout(height=30)
        self.text_input = TextInput(
            text=text,
            hint_text=hint_text,
            multiline=False,
            font_size=default_font_size,
            input_filter=input_filter
        )
        text_input_layout.add_widget(self.text_input)

        self.add_widget(label_layout)
        self.add_widget(text_input_layout)

    def get_text(self):
        return self.text_input.text
