import os

from github import Github
from todoist import TodoistAPI

todoist = TodoistAPI(os.environ["TODOIST_TOKEN"])
github = Github(os.environ["GITHUB_TOKEN"])
