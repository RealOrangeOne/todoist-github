import datetime
import logging

from dateutil.relativedelta import relativedelta

from todoist_github.clients import github, todoist
from todoist_github.utils import get_github_issue_details, get_issue
from todoist_github.utils.todoist import (
    get_relevant_todoist_tasks,
    is_task_completed,
    issue_to_task_name,
)


def assigned_issues():
    todoist_tasks = get_relevant_todoist_tasks(todoist)
    relevant_since = datetime.datetime.now() - relativedelta(
        weeks=30
    )  # TODO: Make this a sane number
    tasks_actioned = []
    me = github.get_user()
    for assigned_issue in me.get_issues(state="all", since=relevant_since):
        task = todoist_tasks.get(assigned_issue.html_url)
        if not task and assigned_issue.state == "open":
            logging.info("Creating '%s'", assigned_issue.title)
            task = todoist.items.add(issue_to_task_name(assigned_issue))
        if not task:
            continue
        tasks_actioned.append(task["id"])
        if assigned_issue.state == "closed" and not is_task_completed(task):
            logging.info("Completing '%s'", assigned_issue.title)
            task.complete()
        elif assigned_issue.state == "open" and is_task_completed(task):
            logging.info("Uncompleting task '%s'", assigned_issue.title)
            task.uncomplete()
        if task["content"] != issue_to_task_name(assigned_issue):
            logging.info("Updating issue name for '%s'", assigned_issue.title)
            task.update(content=issue_to_task_name(assigned_issue))
        if assigned_issue.milestone and assigned_issue.milestone.due_on:
            task.update(
                date_string=assigned_issue.milestone.due_on.strftime("%d/%m/%Y")
            )

    for task in todoist_tasks.values():
        if not is_task_completed(task) or task["id"] in tasks_actioned:
            continue
        issue_details = get_github_issue_details(task["content"])
        if not issue_details:
            continue
        org, repo, issue_number = issue_details
        issue = get_issue(me, org, repo, issue_number)
        me_assigned = me.login in {assignee.login for assignee in issue.assignees}
        if not me_assigned:
            logging.warn("Deleting '%s'", issue.title)
            task.delete()
