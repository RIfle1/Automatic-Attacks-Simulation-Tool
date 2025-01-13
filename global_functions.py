import requests

from gui.console_view import ConsoleView


def send_request(username_var, username_value, password_var, password_value,
                 login_success_var, url, headers, console_view: ConsoleView):
    try:
        trying = "[INFO] Trying password: {} and {}: {}".format(password_value, username_var,
                                                                username_value)
        console_view.add_text_schedule(trying)
        print(trying)

        payload = {
            username_var: username_value,
            password_var: password_value
        }

        response = requests.post(url, json=payload, headers=headers)

        if login_success_var in response.text or response.status_code == 200:
            success_msg = f"[SUCCESS] Password {password_value} and {username_var} {username_value} are correct"
            console_view.add_text_schedule(success_msg)
            print(success_msg)
            return True

        else:
            failed_msg = f"[FAILED] Password {password_value} and {username_var} {username_value} incorrect"
            console_view.add_text_schedule(failed_msg)
            print(failed_msg)

    except Exception as e:
        error_msg = f"[ERROR] Error: {e}"
        console_view.add_text_schedule(error_msg)
        print(error_msg)

    return False