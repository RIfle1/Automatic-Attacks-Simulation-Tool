from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from dictionary_attacks.global_variables import url_global
from gui.dictionary_attacks.custom_layout import CustomHeightLayout
from gui.global_variables import default_font_size, title_font_size


class UrlView(GridLayout):
    def __init__(self, **kwargs):
        super(UrlView, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.size_hint_y = None
        self.height = 60

        label_layout = CustomHeightLayout()
        label = Label(
            text="URL",
            font_size=title_font_size,
        )
        label_layout.add_widget(label)

        url_area_layout = CustomHeightLayout(height=30)
        self.url_area = TextInput(
            text=url_global,
            hint_text="URL",
            multiline=False,
            font_size=default_font_size,
        )
        url_area_layout.add_widget(self.url_area)

        self.add_widget(label_layout)
        self.add_widget(url_area_layout)

    def get_url(self):
        return self.url_area.text
