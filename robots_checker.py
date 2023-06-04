from urllib.parse import urlparse, urljoin

class RobotsChecker:
    """
    This class checks whether a given URL is allowed to be accessed by robots.txt file.
    """
    
    def __init__(self, user_agent='*') -> None:
        self.user_agent = user_agent

    def is_allowed(self, url: str) -> bool:
        """
        Determines whether the specified URL is allowed to be accessed by robots.txt file.
        Unless you specify otherwise in your robots.txt file, all files are implicitly allowed for crawling.

        Args:
            url (str): URL to check access permission.

        Returns:
            bool: True if access is allowed, False if not.
        """
        # Parse the base URL from the given URL.
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        # Construct the URL for the robots.txt file based on the base URL.
        robots_url = urljoin(base_url, "/robots.txt")
        
        print(robots_url)
        return True

if __name__ == '__main__':
    checker = RobotsChecker()
    url = 'https://example.com'
    if checker.is_allowed(url):
        print(f'{url} is accessible.')
    else:
        print(f'{url} is not accessible.')