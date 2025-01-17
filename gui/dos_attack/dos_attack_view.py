from threading import Thread
from urllib.parse import urlparse
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from attacks.dos_attack.main import ddos_attack
from gui.dos_attack.stopped_manager import start_process, stop_process
from gui.global_variables import default_button_height, default_padding_1
from gui.utils.custom_layout import CustomHeightLayout
from gui.utils.text_input_widget import TextInputWidget
from attacks.dos_attack.global_variables import url_global, fake_ip_global  # Import the default URL


class DoSAttackView(BoxLayout):
    def __init__(self, console_view, **kwargs):
        super(DoSAttackView, self).__init__(**kwargs)
        self.console_view = console_view
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Add URL view at the top
        self.target_input = TextInputWidget(
            url_global, "URL", "URL of the website you want to target"
        )
        self.add_widget(self.target_input)


        self.fake_ip_input = TextInputWidget(
            fake_ip_global, "Fake IP", "Fake IP to use in the attack"
        )
        self.add_widget(self.fake_ip_input)

        # Add a spacer to push buttons to the bottom
        self.add_widget(BoxLayout(size_hint_y=1))  # Spacer

        # Button layout at the bottom using CustomHeightLayout
        button_layout = BoxLayout(orientation='vertical', size_hint_y=None)

        # Start DDoS Button
        ddos_button_layout = CustomHeightLayout(height=default_button_height)
        self.ddos_button = Button(text="Start DDoS Attack")
        self.ddos_button.bind(on_press=self.start_ddos)
        ddos_button_layout.add_widget(self.ddos_button)
        button_layout.add_widget(ddos_button_layout)

        # Add a spacer (Widget) between the two buttons for padding
        padding_widget = Widget(size_hint_y=None, height=default_padding_1)
        button_layout.add_widget(padding_widget)

        stop_button_layout = CustomHeightLayout(height=default_button_height)
        self.stop_button = Button(text="Stop Attack")
        self.stop_button.bind(on_press=self.stop_attack)
        stop_button_layout.add_widget(self.stop_button)
        button_layout.add_widget(stop_button_layout)

        self.add_widget(button_layout)




    def start_ddos(self, instance):
        """
        Validate inputs and start the attack in a new thread.
        """
        start_process()

        # Retrieve inputs
        target = self.target_input.get_text().strip()
        fake_ip = self.fake_ip_input.get_text().strip()

        # Validate the URL
        if not self.validate_url(target):
            self.console_view.add_text_schedule("[ERROR] Invalid URL provided.")
            stop_process()
            return

        # Validate the Fake IP
        if not self.validate_ip(fake_ip):
            self.console_view.add_text_schedule("[ERROR] Invalid Fake IP provided.")
            stop_process()
            return

        # Start the attack in a separate thread
        attack_thread = Thread(target=self.run_ddos, args=(target, fake_ip))
        attack_thread.daemon = True  # The thread will exit when the main program exits
        attack_thread.start()

    def run_ddos(self, target, fake_ip):
        """
        Run the DDoS attack function.
        """
        self.console_view.add_text_schedule(f"Starting DDoS Attack on {target}.")
        ddos_attack(target, fake_ip, self.console_view)

    def stop_attack(self, instance):
        """
        Stop the DDoS attack.
        """
        stop_process()
        self.console_view.add_text_schedule("[INFO] Attack stopped by user.")

    @staticmethod
    def validate_url(url):
        """
        Validate the provided URL.
        """
        try:
            parsed = urlparse(url)
            return all([parsed.scheme, parsed.netloc])
        except Exception:
            return False

    @staticmethod
    def validate_ip(ip):
        """
        Validate the provided Fake IP.
        """
        parts = ip.split(".")
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit() or not 0 <= int(part) <= 255:
                return False
        return True
