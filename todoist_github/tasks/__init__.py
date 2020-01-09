from .assigned_issues import assigned_issues
from .prs_to_review import prs_to_review

ALL_TASKS = [prs_to_review, assigned_issues]

__all__ = ["ALL_TASKS"]
