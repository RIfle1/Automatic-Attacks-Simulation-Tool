from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from attacks.credential_stuffing.global_variables import url_global
from gui.global_variables import default_font_size, title_font_size
from gui.utils.custom_layout import CustomHeightLayout


class SiteMapUrlView(GridLayout):
    def __init__(self,url, **kwargs):
        super(SiteMapUrlView, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.size_hint_y = None
        self.height = 60

        label_layout = CustomHeightLayout()
        label = Label(
            text="SiteMap URL",
            font_size=title_font_size,
        )
        label_layout.add_widget(label)

        url_area_layout = CustomHeightLayout(height=30)
        self.url_area = TextInput(
            text=url,
            hint_text="SiteMap URL",
            multiline=False,
            font_size=default_font_size,
        )
        url_area_layout.add_widget(self.url_area)

        self.add_widget(label_layout)
        self.add_widget(url_area_layout)

    def get_url(self):
        return self.url_area.text
