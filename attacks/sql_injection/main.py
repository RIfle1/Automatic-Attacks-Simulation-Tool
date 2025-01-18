import requests


def sql_injection_test(target_url, parameters, payloads, console_view):
    for payload in payloads:
        # Inject the payload into the parameters
        injection_parameters = parameters.copy()
        injection_parameters["username"] = payload

        try:
            # Send the POST request
            response = requests.post(target_url, data=injection_parameters)

            # Log the response and status
            console_view.add_text_schedule(f"[INFO] Payload: {payload}")
            console_view.add_text_schedule(f"[INFO] Response Status Code: {response.status_code}")
            console_view.add_text_schedule(f"[INFO] Response Text: {response.text[:200]}")  # Limit response text
        except Exception as e:
            console_view.add_text_schedule(f"[ERROR] Failed to test payload '{payload}': {e}")
