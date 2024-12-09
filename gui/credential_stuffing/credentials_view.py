from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from credential_stuffing.main import Credentials
from gui.credential_stuffing.custom_layout import CustomDynamicLayout, CustomHeightLayout
from gui.global_variables import default_font_size, default_button_height, title_font_size


class CredentialsView(GridLayout):
    def __init__(self, **kwargs):
        super(CredentialsView, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 3
        self.size_hint = (1, 0.3)

        label_layout = CustomHeightLayout()
        label = Label(
            text="Credentials",
            font_size=title_font_size,
        )
        label_layout.add_widget(label)

        self.credentials_scroll_view = CredentialsScrollView()

        add_credential_button_layout = CustomHeightLayout(height=default_button_height)
        self.add_credential_button = Button(text="Add Credentials")
        self.add_credential_button.bind(on_press=self.on_add_credential_click)

        add_credential_button_layout.add_widget(self.add_credential_button)

        self.add_widget(label_layout)
        self.add_widget(self.credentials_scroll_view)
        self.add_widget(add_credential_button_layout)

    def on_add_credential_click(self, instance):
        self.credentials_scroll_view.add_credential(CredentialsWidget(self.credentials_scroll_view))

    def get_credentials_list(self):
        return [credentials.get_credentials() for credentials in self.credentials_scroll_view.credentials_layout.children]


class CredentialsScrollView(ScrollView):
    def __init__(self, **kwargs):
        super(CredentialsScrollView, self).__init__(**kwargs)
        self.size_hint = (1, 1)
        self.credentials_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.credentials_layout.bind(minimum_height=self.credentials_layout.setter('height'))

        self.add_widget(self.credentials_layout)

    def add_credential(self, credential):
        self.credentials_layout.add_widget(credential)

    def remove_credential(self, credential):
        self.credentials_layout.remove_widget(credential)


class CredentialsWidget(GridLayout):
    def __init__(self, credentials_scroll_view: CredentialsScrollView, **kwargs):
        super(CredentialsWidget, self).__init__(**kwargs)
        self.credentials_scroll_view = credentials_scroll_view

        self.cols = 3
        self.rows = 1
        self.size_hint_max_y = 35
        self.size_hint_min_y = 35

        username_input_layout = CustomDynamicLayout(size_x=0.4, size_y=1, padding=1)
        self.username_input = TextInput(
            hint_text="Username",
            multiline=False,
            font_size=default_font_size,
        )
        username_input_layout.add_widget(self.username_input)

        password_input_layout = CustomDynamicLayout(size_x=0.4, size_y=1, padding=1)
        self.password_input = TextInput(
            hint_text="Password",
            multiline=False,
            font_size=default_font_size,
        )
        password_input_layout.add_widget(self.password_input)

        delete_button_layout = CustomDynamicLayout(size_x=0.15, size_y=1, padding=1)
        self.delete_button = Button(text="Delete")
        self.delete_button.bind(on_press=self.on_delete_click)

        delete_button_layout.add_widget(self.delete_button)

        self.add_widget(username_input_layout)
        self.add_widget(password_input_layout)
        self.add_widget(delete_button_layout)

    def on_delete_click(self, instance):
        self.credentials_scroll_view.remove_credential(self)

    def get_credentials(self):
        return Credentials(self.username_input.text, self.password_input.text)
