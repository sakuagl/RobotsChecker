import requests
from urllib.parse import urlparse, urljoin
from requests.exceptions import RequestException

class RobotsChecker:
    
    def __init__(self, user_agent='*') -> None:
        self.user_agent = user_agent

    def is_allowed(self, url: str) -> bool:
        # Parse the base URL from the given URL.
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        # Construct the URL for the robots.txt file based on the base URL.
        robots_url = urljoin(base_url, "/robots.txt")

        # Attempt to retrieve the content of the robots.txt file.
        try:
            response = requests.get(robots_url)
            content = response.text
        except RequestException as e:
            # If an error occurs, assume that access is not allowed.
            print("A exception occurred:\n", str(e))
            return False

        return True

if __name__ == '__main__':
    checker = RobotsChecker()
    url = 'https://example.com'
    if checker.is_allowed(url):
        print(f'{url} is accessible.')
    else:
        print(f'{url} is not accessible.')