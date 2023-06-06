import requests
from urllib.parse import urlparse, urljoin

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
        # https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt#http-status-codes
        try:
            response = requests.get(robots_url)
            self._raise_status(response)
        except StatusError:
            status_code = response.status_code
            
            if status_code == 429 and status_code // 100 == 5:
                return False
            else:
                return True 
        except requests.RequestException:
            return False

        content = response.text.splitlines()
        user_agent_section = self._find_user_agent_section(content)
        
        return True
        
    def _raise_status(self, response: requests.Response) -> None:
        """
        Raises an exception if the HTTP status code is not in the 200 range.

        Args:
            response (requests.Response): The HTTP response object.

        Raises:
            StatusError: If the HTTP status code is not in the 200 range.
        """
        status_code = response.status_code
        if status_code // 100 != 2:
            raise StatusError("Unexpected HTTP status code", status_code)
        
    def _find_user_agent_section(self, content: list) -> list:
        # Create a user agent marker based on the class instance user agent
        marker = "User-agent: " + self.user_agent
        
        # Initialize variables
        section_lines = []
        user_agent_found = False
        
        # Iterate over all the lines in the file
        for line in content:
            # Check if the current line is a user agent specification
            if line.startswith("User-agent: "):
                user_agent_found = (line == marker)
            # If a user agent has been found, add the current line to the section
            elif user_agent_found:
                section_lines.append(line.strip())

        # Return the section lines
        return section_lines
        
    def _path_matches(self, url: str) -> bool:
        pass

class StatusError(Exception):
    """
    This is a custom exception class that inherits from the built-in Exception class.
    It is used to raise exceptions in case of certain errors in the program.
    """
    def __init__(self, message: str, status_code: int) -> None:
        super().__init__(f"{message}: {status_code}")

if __name__ == '__main__':
    checker = RobotsChecker()
    url = 'https://example.com'
    if checker.is_allowed(url):
        print(f'{url} is accessible.')
    else:
        print(f'{url} is not accessible.')