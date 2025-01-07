import threading

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget

from attacks.least_privilege.leastPriviliege import test_least_privilege
from gui.least_privilege.SitemapUrlView import SiteMapUrlView
from gui.least_privilege.UrlView import UrlView

from gui.least_privilege.console_view import ConsoleView
from gui.least_privilege.custom_layout import CustomHeightLayout
from gui.least_privilege.stopped_manager import start_process, is_stopped, stop_process
from gui.global_variables import default_button_height, default_padding_1


class LeastPrivilegeTokenView(BoxLayout):
    def __init__(self,console_view: ConsoleView, **kwargs):
        self.console_view = console_view
        super(LeastPrivilegeTokenView, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Add URL view at the top
        self.url_view = UrlView()
        self.add_widget(self.url_view)

        self.site_map_url_view = SiteMapUrlView()
        self.add_widget(self.site_map_url_view)

        # Add a spacer to push buttons to the bottom
        self.add_widget(BoxLayout(size_hint_y=1))  # Spacer

        # Button layout at the bottom using CustomHeightLayout
        button_layout = BoxLayout(orientation='vertical', size_hint_y=None)

        # First button in CustomHeightLayout
        start_button_layout = CustomHeightLayout(height=default_button_height)
        self.start_button = Button(text="Least Privilege Attack")
        self.start_button.bind(on_press=self.start_credential_stuffing_attack_thread)
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
        return self.url_view.get_url()

    def start_credential_stuffing_attack_thread(self, instance):
        start_process()
        threading.Thread(target=start_csrf_grab, args=(self,)).start()

    def stop_attack(self, instance):
        stop_process()

def start_csrf_grab(self: LeastPrivilegeTokenView):
    url = self.url_view.get_url()
    sitemap_url = self.site_map_url_view.get_url()
    self.console_view.add_text_schedule(f"Starting Least Privilege Attack on {url}")

    success=False
    while not is_stopped():
        success=test_least_privilege(url,sitemap_url, self.console_view)
        if success or is_stopped():
            break

    if not is_stopped():
        self.console_view.add_text_schedule("Least Privilege attack complete")
        self.console_view.add_text_schedule("")
    else:
        self.console_view.add_text_schedule("Least Privilege attack stopped")
        self.console_view.add_text_schedule("")
