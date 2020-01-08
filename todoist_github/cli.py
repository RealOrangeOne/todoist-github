#!/usr/bin/env python3
import datetime

from dateutil.relativedelta import relativedelta

from .clients import github, todoist
from .utils import get_github_issue_details, get_github_task, get_issue


def get_issue_link(issue_or_pr) -> str:
    return "[#{id}]({url})".format(id=issue_or_pr.number, url=issue_or_pr.html_url)


def issue_to_task_name(issue) -> str:
    return get_issue_link(issue) + ": " + issue.title


def get_relevant_todoist_tasks():
    todoist.items.sync()
    tasks = {}
    for task in todoist.items.all():
        github_task = get_github_task(task["content"])
        if github_task:
            tasks[github_task] = task
    return tasks


def is_task_completed(task):
    return task.data.get("checked", 0)


def main():
    todoist_tasks = get_relevant_todoist_tasks()
    relevant_since = datetime.datetime.now() - relativedelta(
        weeks=30
    )  # TODO: Make this a sane number
    tasks_actioned = []
    me = github.get_user()
    for assigned_issue in me.get_issues(state="all", since=relevant_since):
        task = todoist_tasks.get(assigned_issue.html_url)
        if not task and assigned_issue.state == "open":
            task = todoist.items.add(issue_to_task_name(assigned_issue))
        if not task:
            continue
        tasks_actioned.append(task["id"])
        if assigned_issue == "closed" and not is_task_completed(task):
            print("completing", assigned_issue)
            task.complete()
        if is_task_completed(task):
            print("uncompleting task", assigned_issue)
            task.uncomplete()
        if task["content"] != issue_to_task_name(assigned_issue):
            print("updating issue name for", assigned_issue)
            task.update(content=issue_to_task_name(assigned_issue))
        if assigned_issue.milestone and assigned_issue.milestone.due_on:
            task.update(
                date_string=assigned_issue.milestone.due_on.strftime("%d/%m/%Y")
            )

    for task in todoist_tasks.values():
        if not is_task_completed(task) or task["id"] in tasks_actioned:
            continue
        org, repo, issue_number = get_github_issue_details(task["content"])
        issue = get_issue(me, org, repo, issue_number)
        me_assigned = me.login in {assignee.login for assignee in issue.assignees}
        if not me_assigned:
            print("Deleting", issue)
            task.delete()


if __name__ == "__main__":
    main()
