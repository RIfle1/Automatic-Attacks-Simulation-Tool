from kivy.uix.boxlayout import BoxLayout

from gui.global_variables import default_padding_1, default_button_height


class CustomDynamicLayout(BoxLayout):
    def __init__(self, orientation='vertical',
                 size_x=1, size_y=0.1, padding=0,
                 **kwargs):
        super(CustomDynamicLayout, self).__init__(**kwargs)
        self.orientation = orientation
        self.padding = padding
        self.size_hint = (size_x, size_y)


class CustomHeightLayout(CustomDynamicLayout):
    def __init__(self, height=30, **kwargs):
        super(CustomHeightLayout, self).__init__(orientation='vertical', **kwargs)
        self.height = height
        self.size_hint_y = None



