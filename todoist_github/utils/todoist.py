from github.Issue import Issue

from . import get_github_task


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
