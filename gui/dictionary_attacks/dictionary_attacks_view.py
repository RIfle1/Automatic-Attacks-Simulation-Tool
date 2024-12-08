import threading
import time

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from kivy.clock import Clock

from dictionary_attacks.global_variables import headers_global, USERNAME_KEY, PASSWORD_KEY, LOGIN_SUCCESS_KEY
from dictionary_attacks.main import set_credentials, global_credentials_list, dictionary_attack
from gui.dictionary_attacks.UrlView import UrlView
from gui.dictionary_attacks.console_view import ConsoleView
from gui.dictionary_attacks.credentials_view import CredentialsView
from gui.dictionary_attacks.custom_layout import CustomHeightLayout
from gui.dictionary_attacks.keywords_view import KeywordsView
from gui.dictionary_attacks.variables_view import VariablesView
from gui.global_variables import default_button_height


class DictionaryAttackView(GridLayout):
    def __init__(self, console_view: ConsoleView, **kwargs):
        super(DictionaryAttackView, self).__init__(**kwargs)
        self.console_view = console_view

        self.cols = 1
        self.rows = 5
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

        button_layout = CustomHeightLayout(height=default_button_height)
        self.button = Button(text="Start Dictionary Attack")
        self.button.bind(on_press=self.start_dictionary_attack_thread)
        button_layout.add_widget(self.button)

        self.add_widget(button_layout)

    def start_dictionary_attack_thread(self, instance):
        threading.Thread(target=start_dictionary_attack, args=(self,)).start()


def start_dictionary_attack(self: DictionaryAttackView):
    url = self.url_view.get_url()
    keywords = self.keywords_view.get_keywords()
    global_credentials_list.append(self.credentials_view.get_credentials_list())

    username_variable = self.variables_view.get_variable_values(USERNAME_KEY)
    password_variable = self.variables_view.get_variable_values(PASSWORD_KEY)
    login_success_variable = self.variables_view.get_variable_values(LOGIN_SUCCESS_KEY)

    for keyword in keywords:
        set_credentials(keyword)
        output = dictionary_attack(username_variable, password_variable, login_success_variable, url,
                                   headers_global, self.console_view)
        if output.success:
            break

    print("Dictionary Attack Complete")

    # for i in range(5):
    #     time.sleep(1)  # Simulate some work
    #     print(f"Background task running: {i + 1} seconds")
