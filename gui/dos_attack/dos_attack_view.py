import time
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
from attacks.dos_attack.global_variables import url_global, fake_ip_global


class DoSAttackView(BoxLayout):
    def __init__(self, console_view, report_view, **kwargs):
        super(DoSAttackView, self).__init__(**kwargs)
        self.console_view = console_view
        self.report_view = report_view
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Initialize attack statistics
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0

        # Add URL Input
        self.target_input = TextInputWidget(
            url_global, "URL", "URL of the website you want to target"
        )
        self.add_widget(self.target_input)

        # Add Fake IP Input
        self.fake_ip_input = TextInputWidget(
            fake_ip_global, "Fake IP", "Fake IP to use in the attack"
        )
        self.add_widget(self.fake_ip_input)

        # Add Threads Input
        self.threads_input = TextInputWidget(
            "10", "Threads", "Number of threads for the attack"
        )
        self.add_widget(self.threads_input)

        # Add Delay Input
        self.delay_input = TextInputWidget(
            "0.5", "Delay (s)", "Delay between requests in seconds"
        )
        self.add_widget(self.delay_input)

        # Spacer
        self.add_widget(BoxLayout(size_hint_y=1))  # Spacer

        # Button Layout
        button_layout = BoxLayout(orientation='vertical', size_hint_y=None)

        # Start DDoS Button
        ddos_button_layout = CustomHeightLayout(height=default_button_height)
        self.ddos_button = Button(text="Start DDoS Attack")
        self.ddos_button.bind(on_press=self.start_ddos)
        ddos_button_layout.add_widget(self.ddos_button)
        button_layout.add_widget(ddos_button_layout)

        # Add Spacer Between Buttons
        padding_widget = Widget(size_hint_y=None, height=default_padding_1)
        button_layout.add_widget(padding_widget)

        # Stop Button
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
        try:
            num_threads = int(self.threads_input.get_text().strip())
            delay = float(self.delay_input.get_text().strip())
        except ValueError:
            self.console_view.add_text_schedule("[ERROR] Invalid thread count or delay value.")
            stop_process()
            return

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

        # Reset attack statistics
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0

        # Start the attack in a separate thread
        attack_thread = Thread(target=self.run_ddos, args=(target, fake_ip, num_threads, delay))
        attack_thread.daemon = True
        attack_thread.start()

    def run_ddos(self, target, fake_ip, num_threads, delay):
        self.console_view.add_text_schedule(
            f"Starting DDoS Attack on {target} with {num_threads} threads and {delay}s delay."
        )
        try:
            ddos_attack(
                target,
                fake_ip,
                self.console_view,
                self.update_attack_statistics,
                num_threads=num_threads,
                delay=delay
            )
        except Exception as e:
            self.console_view.add_text_schedule(f"[ERROR] An error occurred: {e}")

        # Generate report automatically after attack completion
        self.console_view.add_text_schedule("[INFO] Attack stopped by user.")
        self.console_view.add_text_schedule("[INFO] Attack complete. Generating report...")
        self.generate_report()

    def update_attack_statistics(self, success):
        self.total_requests += 1
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1

    def generate_report(self):
        report = f"--------------DDoS Attack Report START--------------\n"
        report += f"[INFO] Total Requests Sent: {self.total_requests}\n"
        report += f"[INFO] Successful Requests: {self.successful_requests}\n"
        report += f"[INFO] Failed Requests: {self.failed_requests}\n"
        report += f"--------------DDoS Attack Report END--------------\n"

        # Display the report in the report view
        self.report_view.add_text_schedule(report)

    def stop_attack(self, instance):
        stop_process()
        self.console_view.add_text_schedule("[INFO] Stopping attack...")


    @staticmethod
    def validate_url(url):
        try:
            parsed = urlparse(url)
            return all([parsed.scheme, parsed.netloc])
        except Exception:
            return False

    @staticmethod
    def validate_ip(ip):
        parts = ip.split(".")
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit() or not 0 <= int(part) <= 255:
                return False
        return True
