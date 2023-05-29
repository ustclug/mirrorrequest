import os
from github import Github

def count_reactions(token, repo_name):
    g = Github(token)
    repo = g.get_repo(repo_name)

    issues = repo.get_issues(state="open", labels=["needvote"])

    reactions_count = {}

    for issue in issues:
        reactions = issue.get_reactions()
        count = 0
        for reaction in reactions:
            if reaction.content == "+1":
                count += 1
        reactions_count[issue.number] = count

    sorted_reactions_count = dict(sorted(reactions_count.items(), key=lambda item: item[1], reverse=True))

    table = "* Votes:\n  | Title| Count |\n  | --- | --- |\n"
    for issue_number, count in sorted_reactions_count.items():
        table += f"  | #{issue_number} | {count} |\n"

    repo.get_issue(366).edit(body=table)


if __name__ == "__main__":
    token = os.environ["GITHUB_TOKEN"]
    repo_name = os.environ["GITHUB_REPOSITORY"]
    count_reactions(token, repo_name)
