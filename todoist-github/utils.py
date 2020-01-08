from typing import Optional
from urlextract import URLExtract
from urllib.parse import urlparse


extractor = URLExtract()


def get_github_task(content) -> Optional[str]:
    if "github" not in content.lower():
        return None
    for url in extractor.gen_urls(content):
        if urlparse(url).netloc == "github.com":
            return url
