import re
import requests
from urllib.parse import urlparse, urljoin

class RobotsChecker:
    
    def __init__(self, user_agent='*') -> None:
        self.user_agent = user_agent

    def is_allowed(self, url: str) -> bool:
        # Initialize variables
        is_allowed = True
        
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
                is_allowed = False
        except requests.RequestException:
            is_allowed = False

        content = response.text.splitlines()
        user_agent_section = self._find_user_agent_section(content)
        
        # Allow access if no user agent section is found.
        # Disallow or allow, and determine access permission.
        for line in user_agent_section:
            if line.startswith('Allow:'):
                allow_path = line[len('Allow:'):].strip()
                if self._path_matches(allow_path, url):
                    is_allowed = True
            elif line.startswith('Disallow:'):
                disallow_path = line[len('Disallow:'):].strip()
                if self._path_matches(disallow_path, url):
                    is_allowed = False

        # If access permission is not specified, allow access.
        # return is_allowed
        
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
        """
        Extracts the section of the input `lines` that corresponds to the user agent
        specified in the class instance.

        Args:
            lines (list): List of strings representing the contents of a robots.txt file.

        Returns:
            list: List of strings representing the section of the robots.txt file that
            corresponds to the user agent specified in the class instance.
        """
        # Create a user agent marker based on the class instance user agent
        marker = "User-agent: " + self.user_agent
        
        if marker not in content:
            marker = "User-agent: *"
        
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
        
    def _path_matches(self, rule: str, url: str) -> bool:
        """
        Check if a URL matches a given rule.
        Args:
            rule (str): A string representing the URL pattern to match.
            url (str): A string representing the URL to test against the rule.
        Returns:
            bool: True if the URL matches the rule, False otherwise.
        """
        # Replace '*' with '.*' to create a regular expression pattern.
        pattern = rule.replace("*", ".*")
        # Use the 're.match' function to check if the URL matches the pattern.
        return bool(re.match(pattern, url))
        

class StatusError(Exception):
    """
    This is a custom exception class that inherits from the built-in Exception class.
    It is used to raise exceptions in case of certain errors in the program.
    """
    def __init__(self, message: str, status_code: int) -> None:
        super().__init__(f"{message}: {status_code}")

if __name__ == '__main__':
    checker = RobotsChecker('')
    url = 'https://example.com'
    if checker.is_allowed(url):
        print(f'{url} is accessible.')
    else:
        print(f'{url} is not accessible.')