from api.github import GitHub

if __name__ == "__main__":
    gitHubClient = GitHub()
    i = 0
    while (i < 60):
        print(gitHubClient.list_repos("pkrishn6"))
        i += 1
    print(gitHubClient.list_contribs("pkrishn6", "kubernetes"))
    gitHubClient.create_repo("pkrishn6", "abcdefghi", "test3")
