import requests


def list_github_repos(organization):
    url = f"https://api.github.com/orgs/{organization}/repos"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to get data.")
        return

    repos = response.json()
    for repo in repos:
        print(repo["name"])


if __name__ == "__main__":
    list_github_repos("kestra-io")
