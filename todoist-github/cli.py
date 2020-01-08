#!/usr/bin/env python3
from .clients import todoist
from .utils import get_github_task


def get_relevant_todoist_tasks():
    todoist.items.sync()
    tasks = {}
    for task in todoist.items.all():
        if get_github_task(task["content"]):
            tasks[task['content']] = task
    return tasks


def main():
    todoist_tasks = get_relevant_todoist_tasks()




if __name__ == "__main__":
    main()
