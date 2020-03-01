import re
from typing import Optional
from urllib.parse import urlparse

from github.Issue import Issue
from github.PullRequest import PullRequest
from urlextract import URLExtract

GITHUB_ISSUE_PR_RE = re.compile(r"\/(.+?)\/(.+?)\/(pull|issues)\/(\d+?)$")

extractor = URLExtract()


def get_github_task(content) -> Optional[str]:
    if "github" not in content.lower():
        return None
    for url in extractor.gen_urls(content):
        parsed_url = urlparse(url)
        if parsed_url.netloc == "github.com" and GITHUB_ISSUE_PR_RE.search(
            parsed_url.path
        ):
            return url
    return None


def get_github_issue_details(content):
    url = get_github_task(content)
    if not url:
        return
    parsed_url = urlparse(url)
    match = GITHUB_ISSUE_PR_RE.search(parsed_url.path)
    if not match:
        return
    return match.group(1), match.group(2), match.group(4)


def get_issue(me, org, repo, issue_num):
    headers, data = me._requester.requestJsonAndCheck(
        "GET", f"/repos/{org}/{repo}/issues/{issue_num}"
    )
    return Issue(me._requester, headers, data, completed=True)


def get_my_review(me, pr: PullRequest):
    for review in pr.get_reviews().reversed:
        if review.user.login == me.login:
            return review
