import yaml
import requests
import time
from urllib.parse import urlsplit

def read_yaml_file(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def test_endpoint(endpoint):
    try:
        start_time = time.time()
        response = requests.request(
            method=endpoint.get('method', 'GET'),
            url=endpoint['url'],
            headers=endpoint.get('headers', {}),
            data=endpoint.get('body', ''),
            timeout=5
        )
        latency = (time.time() - start_time) * 1000
        if 200 <= response.status_code < 300 and latency < 500:
            return True
    except requests.exceptions.RequestException:
        return False

def calculate_availability(total_urls, passed_urls):
    for url in total_urls:
        total_count = total_urls.get(url)
        passed_count = passed_urls.get(url, 0)

        availability = (passed_count / total_count) * 100 if total_count > 0 else 0

        print(f"{url} has {availability}% availability percentage")

def monitor_endpoints(file_path):
    endpoints = read_yaml_file(file_path)
    total_urls = {}
    passed_urls = {}
    while True:
        for endpoint in endpoints:
            url = endpoint['url']
            domain = urlsplit(url).hostname
            if domain in total_urls:
                total_urls[domain] += 1
            if domain not in passed_urls:
                passed_urls[domain] = 0
            if domain not in total_urls:
                total_urls[domain] = 1

            result = test_endpoint(endpoint)
            if result:
                passed_urls[domain] += 1

        calculate_availability(total_urls, passed_urls)

        time.sleep(15)

if __name__ == "__main__":
    file_path = input("Enter the YAML file path: ")
    monitor_endpoints(file_path)
