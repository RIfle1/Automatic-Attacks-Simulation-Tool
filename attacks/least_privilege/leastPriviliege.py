import time
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_urls_from_sitemap(sitemap_url,console_view):
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
                urls.extend(get_urls_from_sitemap(nested_sitemap_url,console_view))

            # Extract URLs from the current sitemap
            for url in root.findall('ns:url', namespaces):
                loc = url.find('ns:loc', namespaces).text
                urls.append(loc)

            return urls
        else:
            console_view.add_text_schedule(f"Sitemap not available or error fetching the sitemap (status code: {response.status_code})")
            return []
    except requests.exceptions.RequestException as e:
        console_view.add_text_schedule(f"Error fetching sitemap: {e}")
        return []

def get_post_endpoints(url,console_view):
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
            console_view.add_text_schedule(f"Rate limit hit while fetching {url}. Retrying after delay.")
            retry_with_backoff(console_view)
            return get_post_endpoints(url,console_view)
        else:
            console_view.add_text_schedule(f"Error fetching the URL: {response.status_code}")
            return set()
    except requests.exceptions.RequestException as e:
        console_view.add_text_schedule(f"Error fetching the URL {url}: {e}")
        return set()

def retry_with_backoff(console_view,retry_attempts=3,):
    for i in range(retry_attempts):
        wait_time = 2 ** i  # Exponential backoff
        console_view.add_text_schedule(f"Retrying in {wait_time} seconds...")
        time.sleep(wait_time)

def test_post_endpoint(base_url, endpoint, seen_endpoints, successful_endpoints,console_view):
    """
    Test a POST endpoint to check if it is protected or responds successfully.
    Skip testing if the endpoint has been marked as seen with a 400 or 429 response.
    """
    full_url = urljoin(base_url, endpoint,)

    # Skip previously seen 400/429 endpoints
    if full_url in seen_endpoints:
        console_view.add_text_schedule(f"Skipping endpoint {full_url} due to previous known response.")
        return

    test_data = {"test": "value"}  # Placeholder data
    try:
        response = requests.post(full_url, data=test_data, timeout=10)
        if response.status_code == 429:
            console_view.add_text_schedule(f"Rate limit hit for {full_url}. Retrying after delay.")
            retry_with_backoff(console_view)
            response = requests.post(full_url, data=test_data, timeout=10)

        elif response.status_code in [401, 403]:
            console_view.add_text_schedule(f"POST endpoint {full_url} is protected (status code: {response.status_code})")
        elif response.status_code < 400:  # Consider success for codes like 200 or 3xx
            console_view.add_text_schedule(f"POST endpoint {full_url} is functional (status code: {response.status_code})")
            successful_endpoints.add(full_url)  # Add successful endpoint (set will avoid duplicates)
        elif response.status_code == 400:
            console_view.add_text_schedule(f"POST endpoint {full_url} returned status code: 400")
            seen_endpoints.add(full_url)  # Add to seen endpoints
        else:
            console_view.add_text_schedule(f"POST endpoint {full_url} returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        console_view.add_text_schedule(f"Error testing endpoint {full_url}: {e}")

def print_post_endpoints(urls, base_url,console_view,endpoints,seen_endpoints,successful_endpoints):
    """
    Print and test POST endpoints for a list of URLs.
    """

    for url in urls[:3]:  # Limit to the first 10 URLs
        post_endpoints = get_post_endpoints(url,console_view)
        console_view.add_text_schedule(f"POST endpoints for {url}:")
        for endpoint in post_endpoints:
            endpoints.add(endpoint)
            console_view.add_text_schedule(f"  {endpoint}")
            test_post_endpoint(base_url, endpoint, seen_endpoints, successful_endpoints,console_view)
        console_view.add_text_schedule("")

    # Print all successful POST endpoints after processing
    if successful_endpoints:
        console_view.add_text_schedule("\nSuccessful POST endpoints:")
        for successful_url in successful_endpoints:
            console_view.add_text_schedule(f"  {successful_url}")
    else:
        console_view.add_text_schedule("\nNo successful POST endpoints found for least privilege attack.")

    return True


#    url = 'https://lab401.com'
#    sitemap_url = 'https://lab401.com/sitemap.xml'
def test_least_privilege(url,sitemap_url,console_view):

    endpoints=set()
    seen_endpoints = set()  # Keep track of endpoints returning 400 or 429 errors
    successful_endpoints = set()  # Use a set to collect successful POST endpoints (avoids duplicates)

    # Try to get URLs from the sitemap
    urls = get_urls_from_sitemap(sitemap_url,console_view)
    if not urls:
        # If no sitemap is available or no URLs found, test the original URL directly
        console_view.add_text_schedule(f"No sitemap found or no URLs extracted. Testing the base URL: {url}")
        urls = [url]

    return print_post_endpoints(urls, url,console_view,endpoints,seen_endpoints,successful_endpoints),endpoints,successful_endpoints

