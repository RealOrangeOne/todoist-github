from todoist import TodoistAPI
import os

todoist = TodoistAPI(os.environ["TODOIST_TOKEN"])
