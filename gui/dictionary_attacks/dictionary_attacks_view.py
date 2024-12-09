import threading

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from dictionary_attacks.global_variables import headers_global, USERNAME_KEY, PASSWORD_KEY, LOGIN_SUCCESS_KEY
from dictionary_attacks.main import set_credentials, dictionary_attack
from gui.dictionary_attacks.UrlView import UrlView
from gui.dictionary_attacks.console_view import ConsoleView
from gui.dictionary_attacks.credentials_view import CredentialsView
from gui.dictionary_attacks.custom_layout import CustomHeightLayout
from gui.dictionary_attacks.keywords_view import KeywordsView
from gui.dictionary_attacks.stopped_manager import start_process, stop_process, is_stopped
from gui.dictionary_attacks.variables_view import VariablesView
from gui.global_variables import default_button_height


class DictionaryAttackView(GridLayout):
    def __init__(self, console_view: ConsoleView, **kwargs):
        super(DictionaryAttackView, self).__init__(**kwargs)
        self.console_view = console_view

        self.cols = 1
        self.rows = 6
        self.padding = 10
        self.spacing = 10

        self.url_view = UrlView()
        self.credentials_view = CredentialsView()
        self.keywords_view = KeywordsView()
        self.variables_view = VariablesView()

        self.add_widget(self.url_view)
        self.add_widget(self.keywords_view)
        self.add_widget(self.credentials_view)
        self.add_widget(self.variables_view)

        start_attack_button_layout = CustomHeightLayout(height=default_button_height)
        self.start_button = Button(text="Start Dictionary Attack")
        self.start_button.bind(on_press=self.start_dictionary_attack_thread)
        start_attack_button_layout.add_widget(self.start_button)

        stop_attack_button_layout = CustomHeightLayout(height=default_button_height)
        self.stop_button = Button(text="Stop Dictionary Attack")
        self.stop_button.bind(on_press=self.stop_dictionary_attack_thread)
        stop_attack_button_layout.add_widget(self.stop_button)

        self.add_widget(start_attack_button_layout)
        self.add_widget(stop_attack_button_layout)

    def start_dictionary_attack_thread(self, instance):
        start_process()
        threading.Thread(target=start_dictionary_attack, args=(self,)).start()


    def stop_dictionary_attack_thread(self, instance):
        stop_process()


def start_dictionary_attack(self: DictionaryAttackView):
    url = self.url_view.get_url()
    keywords = self.keywords_view.get_keywords()

    username_variable = self.variables_view.get_variable_values(USERNAME_KEY)
    password_variable = self.variables_view.get_variable_values(PASSWORD_KEY)
    login_success_variable = self.variables_view.get_variable_values(LOGIN_SUCCESS_KEY)

    print(self.credentials_view.get_credentials_list())

    if len(self.credentials_view.get_credentials_list()) > 0:
        dictionary_attack(username_variable, password_variable, login_success_variable, url,
                          headers_global, self.credentials_view.get_credentials_list(), self.console_view)

    if len(keywords) > 0:
        for keyword in keywords:
            success = dictionary_attack(username_variable, password_variable, login_success_variable, url,
                                        headers_global, set_credentials(keyword, self.console_view), self.console_view)

            if success or is_stopped():
                break

    if not is_stopped():
        self.console_view.add_text_schedule("Dictionary Attack Complete")
    else:
        self.console_view.add_text_schedule("Dictionary Attack Stopped")

