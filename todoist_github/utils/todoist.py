from github.Issue import Issue


def get_issue_link(issue_or_pr) -> str:
    return "[#{id}]({url})".format(id=issue_or_pr.number, url=issue_or_pr.html_url)


def issue_to_task_name(issue: Issue) -> str:
    return get_issue_link(issue) + ": " + issue.title


def is_task_completed(task):
    return task.data.get("checked", 0)
