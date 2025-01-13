import requests

def sql_injection_test(url, parameters, payloads, console_view=None):

    if console_view:
        console_view.add_text_schedule(f"[INFO] Starting SQL Injection test on {url}.")
    else:
        print(f"[INFO] Starting SQL Injection test on {url}.")

    for payload in payloads:
        # Inject the payload into the parameters
        injected_params = {key: f"{value}{payload}" for key, value in parameters.items()}
        try:
            response = requests.get(url, params=injected_params)

            # Log the results
            log_message = f"[TEST] Payload: {payload} | Status Code: {response.status_code}"
            if console_view:
                console_view.add_text_schedule(log_message)
            else:
                print(log_message)

            # Check for vulnerability indicators
            if "error" in response.text.lower() or response.status_code == 500:
                vulnerability_msg = f"[VULNERABLE] Detected SQL Injection with payload: {payload}"
                if console_view:
                    console_view.add_text_schedule(vulnerability_msg)
                else:
                    print(vulnerability_msg)
            else:
                safe_msg = f"[SAFE] No vulnerability detected for payload: {payload}"
                if console_view:
                    console_view.add_text_schedule(safe_msg)
                else:
                    print(safe_msg)

        except Exception as e:
            error_msg = f"[ERROR] Failed to send payload: {payload} | Error: {e}"
            if console_view:
                console_view.add_text_schedule(error_msg)
            else:
                print(error_msg)

    if console_view:
        console_view.add_text_schedule("[INFO] SQL Injection test completed.")
    else:
        print("[INFO] SQL Injection test completed.")
