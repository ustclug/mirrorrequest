#!/usr/bin/python3

import os
from github import Github


def count_reactions(token, repo_name):
    g = Github(token)
    repo = g.get_repo(repo_name)
    issues = repo.get_issues(state="open", labels=["needvote"])

    reactions_count = {}

    for issue in issues:
        reactions = issue.get_reactions()
        up_dates, down_dates = set(), set()
        for reaction in reactions:
            date = reaction.created_at.date()
            if reaction.content == "+1":
                up_dates.add(date)
            elif reaction.content == "-1":
                down_dates.add(date)
        reactions_count[issue.number] = (len(up_dates), len(down_dates))

    sorted_reactions_count = sorted(reactions_count.items(), key=lambda item: (item[1][0] - item[1][1], item[0]), reverse=True)

    table = "## Votes\n\n| Title| Priority | Score |\n| --- | --- | --- |\n"
    for issue_number, (up_count, down_count) in sorted_reactions_count:
        score = up_count - down_count
        table += f"| #{issue_number} | {score} | +{up_count}, -{down_count} |\n"

    repo.get_issue(366).edit(body=table)


if __name__ == "__main__":
    token = os.environ["GITHUB_TOKEN"]
    repo_name = os.environ["GITHUB_REPOSITORY"]
    count_reactions(token, repo_name)
