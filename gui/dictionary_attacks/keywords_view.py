from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from dictionary_attacks.main import keywords
from gui.dictionary_attacks.custom_layout import CustomDynamicLayout, CustomHeightLayout
from gui.global_variables import default_font_size, title_font_size


def keywords_to_string(keywords_var):
    return ';'.join(keywords_var)


class KeywordsView(GridLayout):
    def __init__(self, **kwargs):
        super(KeywordsView, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.size_hint = (1, 0.3)

        label_layout = CustomHeightLayout()
        label = Label(
            text="Key Words",
            font_size=title_font_size,
        )
        label_layout.add_widget(label)

        keywords_area_layout = CustomDynamicLayout(size_x=1, size_y=0.9)
        self.keywords_area = TextInput(
            text=keywords_to_string(keywords),
            hint_text="Key Words (separated by semi-colon).. ex: jeff;henry;mark",
            multiline=True,
            font_size=default_font_size,
        )
        keywords_area_layout.add_widget(self.keywords_area)

        self.add_widget(label_layout)
        self.add_widget(keywords_area_layout)

    def get_keywords(self):
        return self.keywords_area.text.split(';')
