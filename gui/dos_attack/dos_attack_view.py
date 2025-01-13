import threading

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget

from attacks.dos_attack.global_variables import target_url
from attacks.dos_attack.main import perform_dos
from gui.dos_attack.stopped_manager import start_process, stop_process
from gui.global_variables import default_button_height, default_padding_1
from gui.utils.console_view import ConsoleView
from gui.utils.custom_layout import CustomHeightLayout
from gui.utils.text_input_widget import TextInputWidget


class DoSAttackView(BoxLayout):
    def __init__(self, console_view: ConsoleView, **kwargs):
        self.console_view = console_view
        super(DoSAttackView, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Add URL view at the top
        self.url_view = TextInputWidget(target_url, "Target URL", "URL of the website")
        self.add_widget(self.url_view)

        # Add a spacer to push buttons to the bottom
        self.add_widget(BoxLayout(size_hint_y=1))

        button_layout = BoxLayout(orientation='vertical', size_hint_y=None)

        # Start Attack Button
        start_button_layout = CustomHeightLayout(height=default_button_height)
        self.start_button = Button(text="Start DoS Attack")
        self.start_button.bind(on_press=self.start_attack_thread)
        start_button_layout.add_widget(self.start_button)
        button_layout.add_widget(start_button_layout)

        padding_widget = Widget(size_hint_y=None, height=default_padding_1)
        button_layout.add_widget(padding_widget)

        # Stop Attack Button
        stop_button_layout = CustomHeightLayout(height=default_button_height)
        self.stop_button = Button(text="Stop Attack")
        self.stop_button.bind(on_press=self.stop_attack)
        stop_button_layout.add_widget(self.stop_button)
        button_layout.add_widget(stop_button_layout)

        # Add the button layout to the main view
        self.add_widget(button_layout)

    def start_attack_thread(self, instance):
        start_process()
        threading.Thread(target=self.start_attack).start()

    def start_attack(self):
        url = self.url_view.get_text()
        self.console_view.add_text_schedule(f"Starting DoS Attack on {url}. Press 'Stop Attack' to terminate.")
        perform_dos(url, self.console_view)

    def stop_attack(self, instance):
        stop_process()
        self.console_view.add_text_schedule("DoS Attack stopped by user.")
