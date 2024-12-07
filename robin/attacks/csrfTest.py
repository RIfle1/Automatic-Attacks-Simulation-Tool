import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://127.0.0.1:5000'

def scan_for_post_endpoints():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    forms = soup.find_all('form', method='post')
    forms += soup.find_all('form', method='POST')
    post_endpoints = [form['action'] for form in forms]
    return post_endpoints

def test_csrf_protection():
    with requests.Session() as session:
        post_endpoints = scan_for_post_endpoints()
        for endpoint in post_endpoints:
            print(f"Found POST endpoint: {endpoint}")
            # Attempt to submit the form without CSRF token
            response = session.post(f'{BASE_URL}{endpoint}', data={'name': 'Test'})
            assert 'The CSRF token is missing.' in response.text

            # Get the CSRF token and form action URL from the form
            response = session.get(BASE_URL)
            csrf_token, form_action = extract_csrf_token_and_action(response.text)
            print(f"Extracted CSRF token: {csrf_token}")
            assert csrf_token is not None, "CSRF token should not be None"
            assert form_action is not None, "Form action URL should not be None"

            # Submit the form with the CSRF token
            response = session.post(f'{BASE_URL}{form_action}', data={'name': 'Test', 'csrf_token': csrf_token})
            assert 'Form submitted successfully' in response.text

def extract_csrf_token_and_action(html):
    soup = BeautifulSoup(html, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
    form_action = soup.find('form')['action']
    return csrf_token, form_action

if __name__ == '__main__':
    test_csrf_protection()
    print("CSRF protection test passed.")