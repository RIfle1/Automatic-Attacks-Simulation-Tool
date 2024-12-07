import time
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_urls_from_sitemap(sitemap_url):
    """
    Extract all URLs from the XML sitemaps.
    """
    try:
        response = requests.get(sitemap_url, timeout=10)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            urls = []

            # Check for nested sitemaps
            for sitemap in root.findall('ns:sitemap', namespaces):
                nested_sitemap_url = sitemap.find('ns:loc', namespaces).text
                urls.extend(get_urls_from_sitemap(nested_sitemap_url))

            # Extract URLs from the current sitemap
            for url in root.findall('ns:url', namespaces):
                loc = url.find('ns:loc', namespaces).text
                urls.append(loc)

            return urls
        else:
            print(f"Sitemap not available or error fetching the sitemap (status code: {response.status_code})")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching sitemap: {e}")
        return []

def get_post_endpoints(url):
    """
    Extract POST endpoints from the URL by parsing forms.
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form', method=lambda m: m and m.lower() == 'post')
            post_endpoints = set()

            for form in forms:
                action = form.get('action', '').strip()
                if action:
                    post_endpoints.add(action)

            return post_endpoints
        elif response.status_code == 429:
            print(f"Rate limit hit while fetching {url}. Retrying after delay.")
            retry_with_backoff()
            return get_post_endpoints(url)
        else:
            print(f"Error fetching the URL: {response.status_code}")
            return set()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL {url}: {e}")
        return set()

def retry_with_backoff(retry_attempts=3):
    """
    Implements exponential backoff with a maximum number of retry attempts.
    """
    for i in range(retry_attempts):
        wait_time = 2 ** i  # Exponential backoff
        print(f"Retrying in {wait_time} seconds...")
        time.sleep(wait_time)
        return

def test_post_endpoint(base_url, endpoint, seen_endpoints):
    """
    Test a POST endpoint to check if it is protected or responds successfully.
    Skip testing if the endpoint has been marked as seen with a 400 or 429 response.
    """
    full_url = urljoin(base_url, endpoint)

    # Skip previously seen 400/429 endpoints
    if full_url in seen_endpoints:
        print(f"Skipping endpoint {full_url} due to previous known response.")
        return

    test_data = {"test": "value"}  # Placeholder data
    try:
        response = requests.post(full_url, data=test_data, timeout=10)
        if response.status_code == 429:
            print(f"Rate limit hit for {full_url}. Retrying after delay.")
            retry_with_backoff()
            test_post_endpoint(base_url, endpoint, seen_endpoints)  # Retry after delay
        elif response.status_code in [401, 403]:
            print(f"POST endpoint {full_url} is protected (status code: {response.status_code})")
        elif response.status_code < 400:  # Consider success for codes like 200 or 3xx
            print(f"POST endpoint {full_url} is functional (status code: {response.status_code})")
        elif response.status_code == 400:
            print(f"POST endpoint {full_url} returned status code: 400")
            seen_endpoints.add(full_url)  # Add to seen endpoints
        else:
            print(f"POST endpoint {full_url} returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error testing endpoint {full_url}: {e}")

def print_post_endpoints(urls, base_url):
    """
    Print and test POST endpoints for a list of URLs.
    """
    seen_endpoints = set()  # Keep track of endpoints returning 400 or 429 errors
    for url in urls[:20]:  # Limit to the first 10 URLs
        post_endpoints = get_post_endpoints(url)
        print(f"POST endpoints for {url}:")
        for endpoint in post_endpoints:
            print(f"  {endpoint}")
            test_post_endpoint(base_url, endpoint, seen_endpoints)
        print()

if __name__ == '__main__':
    url = 'https://lab401.com'
    sitemap_url = 'https://lab401.com/sitemap.xml'

    # Try to get URLs from the sitemap
    urls = get_urls_from_sitemap(sitemap_url)
    if not urls:
        # If no sitemap is available or no URLs found, test the original URL directly
        print(f"No sitemap found or no URLs extracted. Testing the base URL: {url}")
        urls = [url]

    print_post_endpoints(urls, url)
