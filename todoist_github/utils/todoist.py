import os
from itertools import chain

from github.Issue import Issue

from . import get_github_task

SUB_PROJECT_NAMES = ["Tasks", "GitHub"]


def get_issue_link(issue_or_pr) -> str:
    return "[#{id}]({url})".format(id=issue_or_pr.number, url=issue_or_pr.html_url)


def issue_to_task_name(issue: Issue) -> str:
    return get_issue_link(issue) + ": " + issue.title


def pr_to_task_name(pr) -> str:
    return f"Review {get_issue_link(pr)} : {pr.title}"


def is_task_completed(task):
    return task.data.get("checked", 0)


def get_relevant_todoist_tasks(todoist):
    todoist.items.sync()
    tasks = {}
    for task in todoist.items.all():
        github_task = get_github_task(task["content"])
        if github_task:
            tasks[github_task] = task
    return tasks


def get_project_for_issue(issue: Issue, todoist_projects: dict):
    repo_name = issue.repository.full_name.split("/")[1]
    search_terms = [
        issue.repository.full_name.split("/")[0],
    ]
    if issue.repository.organization:
        search_terms.insert(0, issue.repository.organization.name)
    elif issue.repository.owner:
        search_terms.insert(0, issue.repository.owner.login)
        search_terms.insert(0, issue.repository.owner.name)
    search_terms.append(repo_name)  # Always be at the end, as it's the least specific

    for search_term in search_terms:
        if search_term.lower() in todoist_projects:
            found_project = todoist_projects[search_term.lower()]
            for project in todoist_projects.values():
                if project["parent_id"] != found_project["id"]:
                    continue
                for sub_project_name in chain(SUB_PROJECT_NAMES, [repo_name]):
                    if project["name"].lower() == sub_project_name.lower():
                        return project
            return found_project
    return todoist_projects.get(
        os.environ.get("DEFAULT_TODOIST_PROJECT_NAME", "").lower()
    )
