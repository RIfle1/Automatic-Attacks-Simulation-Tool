import requests
from bs4 import BeautifulSoup
from nbclient.exceptions import stream_output_msg


def scan_for_post_endpoints(html):
    response = requests.get(html)
    soup = BeautifulSoup(response.text, 'html.parser')
    forms = soup.find_all('form', method='post')
    forms += soup.find_all('form', method='POST')
    post_endpoints = [form['action'] for form in forms]
    return post_endpoints


def test_csrf_protection(html,console_view):
    with requests.Session() as session:
        post_endpoints = scan_for_post_endpoints(html)


        for endpoint in post_endpoints:
            console_view.add_text_schedule(f"Found POST endpoint: {endpoint}")

            # Get the CSRF token and form action URL from the form (only once)
            response = session.get(html)
            csrf_token, form_action = extract_csrf_token_and_action(response.text,console_view)

            if csrf_token is None or form_action is None:
                console_view.add_text_schedule("CSRF token or form action is missing.")
                break # CSRF token or form action missing

            # Attempt to submit the form without CSRF token
            response = session.post(f'{html}{endpoint}', data={'name': 'Test'})
            if 'The CSRF token is missing.' not in response.text:
                console_view.add_text_schedule(f"CSRF token missing protection failed at {endpoint}")
                break  # CSRF protection failed

            # Submit the form with the CSRF token
            console_view.add_text_schedule(f"Extracted CSRF token: {csrf_token}")
            response = session.post(f'{html}{form_action}', data={'name': 'Test', 'csrf_token': csrf_token})
            if 'Form submitted successfully' not in response.text:
                console_view.add_text_schedule(f"Form submission failed at {endpoint}")
                break  # Form submission failed

        # If all checks pass
        return True


def extract_csrf_token_and_action(html,console_view):
    soup = BeautifulSoup(html, 'html.parser')
    csrf_input = soup.find('input', {'name': 'csrf_token'})

    if csrf_input:
        csrf_token = csrf_input['value']
        form_action = soup.find('form')['action']
        return csrf_token, form_action
    else:
        console_view.add_text_schedule("No CSRF token found.")
        return None, None
