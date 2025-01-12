from kivy.uix.boxlayout import BoxLayout

class CustomHeightLayout(BoxLayout):
    def __init__(self, height=30, **kwargs):
        super(CustomHeightLayout, self).__init__(orientation='vertical', **kwargs)
        self.height = height
        self.size_hint_y = None
