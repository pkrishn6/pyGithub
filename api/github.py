from lib.client import HTTPClient
from .utils import logger
import requests
import json

Response = requests.models.Response

logger = logger.get_logger("livy-api")

class GitHub(object):
    def __init__(self):
        self.client = HTTPClient()
        self.url = "https://api.github.com"
        self.user = "pkrishn6"
        self.headers: Dict[str, str] = {"Content-Type": "application/json"}

    def list_contribs(self, username, repo):
        url = f"{self.url}/repos/{username}/{repo}/contributors"
        contributors = []

        r: Response = self.client.request(method=requests.get, url=url)
        for i in range(len(r.json())):
            contributors.append(r.json()[i]['login'])
        return contributors

    def create_repo(self, username, api_key, repo_name):
        url = f"{self.url}/user/repos"
        try:
            r: Response = self.client.request(method=requests.post, url=url,
                                              auth=(username, api_key),
                                              data=json.dumps({"name":repo_name}),
                                              headers=self.headers)
        except Exception as e:
            if isinstance(e, requests.exceptions.HTTPError):
                print(e.response.status_code)
                print(e.response.json())
                print(e.response.headers)
            logger.exception(e)
        return True

    def get_user_repositories(self, username):
        """
        List users' public repositories
        """
        url = f"{self.url}/users/{username}/repos"
        repos = []
        try:
            r: Response = self.client.request(method=requests.get, url=url)
            for i in range(len(r.json())):
                repos.append(r.json()[i]['name'])
        except Exception as e:
            if isinstance(e, requests.exceptions.HTTPError):
                print(e.response.status_code)
                print(e.response.json())
                print(e.response.headers)
            logger.exception(e)
        return repos

    def list_repos(self, username):
        return sorted(self.get_user_repositories(username))




