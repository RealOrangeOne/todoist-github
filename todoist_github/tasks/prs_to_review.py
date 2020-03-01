import logging

from todoist_github.clients import github, todoist
from todoist_github.utils import get_my_review
from todoist_github.utils.todoist import (
    get_project_for_issue,
    get_relevant_todoist_tasks,
    is_task_completed,
    pr_to_task_name,
)

SEARCH_STRING = "is:pr review-requested:{username} archived:false"


def prs_to_review():
    relevant_tasks = get_relevant_todoist_tasks(todoist)
    me = github.get_user()
    search_string = SEARCH_STRING.format(username=me.login)
    todoist.projects.sync()
    todoist_projects = {
        project["name"].lower(): project for project in todoist.state["projects"]
    }
    tasks_actioned = []
    for issue in github.search_issues(search_string):
        task = relevant_tasks.get(issue.html_url)
        if not task and issue.state == "open":
            logging.info("Creating '%s'", issue.title)
            task = todoist.items.add(pr_to_task_name(issue))
        if not task:
            continue
        tasks_actioned.append(task["id"])
        pr = issue.as_pull_request()
        if task["content"] != pr_to_task_name(issue):
            logging.info("Updating issue name for '%s'", issue.title)
            task.update(content=pr_to_task_name(issue))

        todoist_project = get_project_for_issue(issue, todoist_projects)
        if todoist_project and task["project_id"] != todoist_project["id"]:
            logging.info("Updating project for '%s'", issue.title)
            task.move(project_id=todoist_project["id"])

        my_review = get_my_review(me, pr)
        if my_review:
            if my_review.commit_id == pr.head.sha and not is_task_completed(task):
                logging.info("Completing '%s'", issue.title)
                task.complete()
            elif is_task_completed(task):
                logging.info("Un-completing '%s'", issue.title)
                task.uncomplete()
        if pr.merged and not is_task_completed(task):
            logging.info("Deleting '%s'", issue.title)
            task.delete()
