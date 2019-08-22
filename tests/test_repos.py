from unittest.mock import patch
from api.github import GitHub

def test_get_repos():
    g_handle = GitHub()

    def _mock(*args):
        return ["Ziddle", "Act"]

    with patch('api.github.GitHub.get_user_repositories',
               _mock), patch.object(g_handle, 'user', "dummy"):
        result = g_handle.list_repos("dummy")
        assert(result == ["Act", "Ziddle"])
        assert(g_handle.user == "dummy")
