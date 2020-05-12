import os, sys, json, shutil
from github import Github

_stage_list = [
    "integration",
    "edge",
    "stable",
    "release"
]

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Not enough parameters\nUsage: python3 generate_snapshot_diff.py <old-snapshot> <new-snapshot>")

    columns, lines = shutil.get_terminal_size((80, 20)) # get the terminal sizing for some printouts later

    # default release version is 1.0.0... might be a bad idea to set a default but we're doing it
    release_version = os.getenv("OCM_RELEASE_VERSION") if os.getenv("OCM_RELEASE_VERSION") is not None else "1.0.0"

    snapshot1 = sys.argv[1] # first variable should be your "old" snapshot
    snapshot2 = sys.argv[2] # second variable should be your "new" snapshot

    g = Github(os.getenv("GITHUB_TOKEN"))
    org = g.get_organization("open-cluster-management")
    repo = org.get_repo("pipeline")

    if snapshot1 in _stage_list: # if someone passed in a stage name, grab the newest snapshot in that release_version-stage pipeline branch
        m1 = repo.get_contents("snapshots", ref=f"{release_version}-{snapshot1}")
        m1 = list(filter(lambda x: "manifest" in x.name and "v2" in x.name, m1))
        m1 = sorted(m1, key = lambda manifest: manifest.name)
        m1 = m1[len(m1) - 1]
    else: # otherwise get the stage:snapshot that was passed in from the release_version-stage pipeline branch
        m1_stage, m1_snapshot = snapshot1.split(":")
        m1 = repo.get_contents("snapshots", ref=f"{release_version}-{m1_stage}")
        m1 = list(filter(lambda x: x.name == f"manifest-{m1_snapshot}-v2.json", m1))
        if len(m1) != 1:
            print(f"Found {len(m1)} matches for manifest-{m1_snapshot}-v2.json in {release_version}-{m1_stage} when we should've found 1.  Exiting with an error.")
            exit(1)
        m1 = m1[0]

    if snapshot2 in _stage_list: # if someone passed in a stage name, grab the newest snapshot in that release_version-stage pipeline branch
        m2 = repo.get_contents("snapshots", ref=f"{release_version}-{snapshot2}")
        m2 = list(filter(lambda x: "manifest" in x.name and "v2" in x.name, m2))
        m2 = sorted(m2, key = lambda manifest: manifest.name)
        m2 = m2[len(m2) - 1]
    else: # otherwise get the stage:snapshot that was passed in from the release_version-stage pipeline branch
        m2_stage, m2_snapshot = snapshot2.split(":")
        m2_target = f"manifest-{m2_snapshot}-v2.json"
        m2 = repo.get_contents("snapshots", ref=f"{release_version}-{m2_stage}")
        m2 = list(filter(lambda x: x.name == m2_target, m2))
        if len(m2) != 1:
            print(f"Found {len(m2)} matches for {m2_target} in {release_version}-{m2_stage} when we should've found 1.  Exiting with an error.")
            exit(1)
        m2 = m2[0]

    # grab names and json load the decoded content (content in plain text of the manifest file)
    m1_name = m1.name
    m2_name = m2.name
    m1_json = json.loads(m1.decoded_content)
    m2_json = json.loads(m2.decoded_content)

    for m2_image in m2_json:
        # get a list of all images from manifest 1 that match the entry in manifest 1, so we can compare them.  
        m1_entries = list(filter(lambda repo: repo["git-repository"] == m2_image["git-repository"] and repo["image-name"] == m2_image["image-name"], m1_json))
        if len(m1_entries) < 1: # if there is no match (< 1 results that match), then either it was deleted or an error occurred
            print("".ljust(columns, '#'))
            print(f'Repo: {m2_image["git-repository"]}, Image: {m2_image["image-name"]}')
            print()
            print(f'Image from {m2_image["git-repository"]} was not present in {m1_name} but was present in {m2_name}.')
            print("".ljust(columns, "#"))
            print()
        elif len(m1_entries) > 1: # if there is more than one match, that's a problem, we check unique identifiers
            print("".ljust(columns, '#'))
            print(f'#Repo: {m2_image["git-repository"]}, Image: {m2_image["image-name"]}'.ljust(columns, '#'))
            print()
            print(f'Image from {m2_image["git-repository"]} had multiple entries in {m1_name}, something is wrong!')
            print("".ljust(columns, "#"))
            print()
        elif m1_entries[0]["git-sha256"] != m2_image["git-sha256"]: # if there is one matching image but the shas don't match, work begins
            m1_image = m1_entries[0]
            print("".ljust(columns, '#'))
            print(f'Repo: {m2_image["git-repository"]}, Image: {m2_image["image-name"]}')
            print()
            print(f'Repo named {m2_image["git-repository"]} changed between {m1_name} and {m2_name}.\n')

            # derive org/repo from the image name from the manifest entry
            image_details = m2_image["git-repository"].split("/")
            org = g.get_organization(image_details[0])
            repo = org.get_repo(image_details[1])

            # grab commits from the cooresponding shas
            m1_commit = repo.get_commit(m1_image["git-sha256"])
            m2_commit = repo.get_commit(m2_image["git-sha256"])

            # walk the tree from the newest commit back up to the oldest commit.  
            # we have to do this because the github api has no git log like behavior
            # if we can't walk back up the tree, some branching nonsense has occurred that
            # we don't care to accomodate, so skip this part.  
            # 
            # if we can get a path of commits, we can print each and try to link them to pull requests
            commit_path = [m2_commit]
            iter_commit = m2_commit.parents[0]
            while iter_commit.sha != m1_commit.sha and iter_commit is not None:
                commit_path.append(iter_commit)
                iter_commit = iter_commit.parents[0] if len(iter_commit.parents) > 0 else None
            commit_path.append(m1_commit)
            if iter_commit is None:
                print(f"Walked the entire commit tree up from {m2_commit.sha} without finding {m1_commit.sha}, we can't report on changes.")
            else:
                print("".rjust(columns, ">"))
                print(f"COMMITS between {m1_commit.sha} and {m2_commit.sha}")
                for commit in commit_path:
                    print("".ljust(columns, '-'))
                    print("Commit:")
                    print(f"\tSHA: {commit.commit.sha}")
                    print(f"\tURL: {commit.commit.html_url}")
                    for pull in commit.get_pulls():
                        print(f"\tAppears in Pull Request: {pull.html_url}")

                        # TODO: Currently, events don't show mentions/references to other issues, only
                        # References to _this_ pr from a commit.  These features should be coming to the
                        # api, but they're not here yet.  Here's a github community post about the linked
                        # issues to follow: https://github.community/t5/GitHub-API-Development-and/Get-all-issues-linked-to-a-pull-request/td-p/46955

                        # Here's some code I was poking around with, events and comments both omit
                        # any linkage information.  
                        # print("Events:")
                        # for event in pull.as_issue().get_events():
                        #     print(event.event)
                        #     if event.event == "referenced":
                        #         print(f"Reference: {event.commit_id}")
                        #     if event.event == "mentioned":
                        #         print(f"Mentioned by {event.commit_id}")
                        # print("Comments")
                        # for comment in pull.get_comments():
                        #     print(comment)

                    print(f"\tMessage:")
                    print(f"{commit.commit.message}")
                    print("".ljust(columns, '-'))
                    print()
                print("".ljust(columns, "<"))
                print()

            # finally, generate a compare link.  
            print(f'Compare all changes at: https://github.com/{image_details[0]}/{image_details[1]}/compare/{m1_image["git-sha256"]}..{m2_image["git-sha256"]}\n')

            print("".rjust(columns, '#'))
            print("\n")
