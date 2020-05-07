import os, sys
from github import Github
import json

if __name__ == "__main__":
    s1 = sys.argv[1]
    s2 = sys.argv[2]
    s1_json = None
    s2_json = None

    g = Github(os.getenv("GITHUB_TOKEN"))

    with open(s1, "r") as js1:
        s1_json = json.load(js1)
    with open(s2, "r") as js2:
        s2_json = json.load(js2)

    for s2_image in s2_json:
        s1_entries = list(filter(lambda repo: repo["git-repository"] == s2_image["git-repository"] and repo["image-name"] == s2_image["image-name"], s1_json))
        if len(s1_entries) < 1:
            print(f'#-----Repo: {s2_image["git-repository"]}, Image: {s2_image["image-name"]}-----#')
            print(f'Image from {s2_image["git-repository"]} was not present in {s1} but was present in {s2}.')
            print("#---------------#\n")
        elif len(s1_entries) > 1:
            print(f'#-----Repo: {s2_image["git-repository"]}, Image: {s2_image["image-name"]}-----#')
            print(f'Image from {s2_image["git-repository"]} had multiple entries in {s1}, something is wrong!')
            print("#---------------#\n")
        elif s1_entries[0]["git-sha256"] != s2_image["git-sha256"]:
            s1_image = s1_entries[0]
            print(f'#-----Repo: {s2_image["git-repository"]}, Image: {s2_image["image-name"]}-----#')
            print(f'Snapshot 1: {s1_image["git-sha256"]}\nSnapshot 2: {s2_image["git-sha256"]}\n')

            image_details = s2_image["git-repository"].split("/")
            org = g.get_organization(image_details[0])
            repo = org.get_repo(image_details[1])

            s1_commit = repo.get_commit(s1_image["git-sha256"])
            s2_commit = repo.get_commit(s2_image["git-sha256"])

            print(f'Snapshot 1: {s1_commit.html_url}\nSnapshot 2: {s2_commit.html_url}\n')

            print(f'Compare: https://github.com/{image_details[0]}/{image_details[1]}/compare/{s1_image["git-sha256"]}..{s2_image["git-sha256"]}')

            print("#---------------#\n")