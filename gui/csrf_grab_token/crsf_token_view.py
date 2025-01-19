import threading

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget

from attacks.credential_stuffing.global_variables import url_global
from attacks.csrf_grab.csrfTest import test_csrf_protection
from gui.csrf_grab_token.stopped_manager import start_process, is_stopped, stop_process
from gui.global_variables import default_button_height, default_padding_1
from gui.utils.console_view import ConsoleView
from gui.utils.custom_layout import CustomHeightLayout
from gui.utils.text_input_widget import TextInputWidget


class CSRFTokenView(BoxLayout):
    def __init__(self, console_view: ConsoleView,report_view: ConsoleView, **kwargs):
        self.console_view = console_view
        self.report_view = report_view
        super(CSRFTokenView, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Add URL view at the top
        self.url_view = TextInputWidget('https://csrf.ldelatullaye.fr/', "URL", "URL of the website you want")
        self.add_widget(self.url_view)

        # Add a spacer to push buttons to the bottom
        self.add_widget(BoxLayout(size_hint_y=1))  # Spacer

        # Button layout at the bottom using CustomHeightLayout
        button_layout = BoxLayout(orientation='vertical', size_hint_y=None)

        # First button in CustomHeightLayout
        start_button_layout = CustomHeightLayout(height=default_button_height)
        self.start_button = Button(text="Grab csrf token")
        self.start_button.bind(on_press=self.start_csrf_attack_thread)
        start_button_layout.add_widget(self.start_button)
        button_layout.add_widget(start_button_layout)

        # Add a spacer (Widget) between the two buttons for padding
        padding_widget = Widget(size_hint_y=None, height=default_padding_1)
        button_layout.add_widget(padding_widget)

        # Second button in CustomHeightLayout
        stop_button_layout = CustomHeightLayout(height=default_button_height)
        self.stop_button = Button(text="Stop Attack")
        self.stop_button.bind(on_press=self.stop_attack)
        stop_button_layout.add_widget(self.stop_button)
        button_layout.add_widget(stop_button_layout)

        # Add the button layout to the main view
        self.add_widget(button_layout)

    def get_url(self):
        """Fetch the URL from UrlView."""
        return self.url_view.get_text()

    def start_csrf_attack_thread(self, instance):
        start_process()
        threading.Thread(target=start_csrf_grab, args=(self,)).start()

    def stop_attack(self, instance):
        stop_process()


def start_csrf_grab(self: CSRFTokenView):
    url = self.url_view.get_text()

    self.console_view.add_text_schedule(f"Starting CSRF Token Grabbing Attack on {url}")
    self.console_view.add_text_schedule("")

    success = False
    while not is_stopped():

        success,endpoints,result = test_csrf_protection(url, console_view=self.console_view,report_view=self.report_view)
        report_results(self.report_view,endpoints,result)

        if success or is_stopped():
            break

    if not is_stopped():
        self.console_view.add_text_schedule("Csrf token grab attack complete")
        self.console_view.add_text_schedule("")
    else:
        self.console_view.add_text_schedule("Csrf token grab attack stopped")
        self.console_view.add_text_schedule("")


def report_results(report_view: ConsoleView, endpoints, result):
    report_results = f"--------------CSRF Token grab Report START--------------\n"
    report_results += "endpoints tested: \n"
    for endpoint in endpoints:
        report_results+= endpoint +"\n"
    report_results+=result+" \n"
    report_results = report_results + f"--------------CSRF Token grab Report END--------------\n"

    report_view.add_text_schedule(report_results)