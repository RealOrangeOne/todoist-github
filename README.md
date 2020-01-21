# Todoist GitHub

![](https://github.com/RealOrangeOne/todoist-github/workflows/Build/badge.svg)

Import assigned issues and PRs into Todoist.

A docker container is available for easy usage: https://hub.docker.com/r/theorangeone/todoist-github

## Requirements

- `requirements.txt` installed in your environment
- `$TODOIST_TOKEN`
- `$GITHUB_TOKEN` (Requires at least `public_repo`, `repo` required for access to private repositories)

## Usage

Run `python3 -m todoist_github` to run once. `--interval` can be used to provide the number of seconds between automated updates.

## Task Details

Task names are built using the task link and title, and are updated automatically on rename.

Tasks are added to projects based on the repository organisation / owner or repository name. If specially named projects exist as children of these, they're used instead. If no project is found, `$DEFAULT_TODOIST_PROJECT_NAME` can be used, else no project is assigned.

Task due dates are based off their milestone.

Once an issue is closed / PR merged, the task is completed. If you're unassigned, the issue is deleted.

## Example `docker-compose.yml`

```yml
version: '3'
services:
  todoist-github:
    image: theorangeone/todoist-github:latest
    container_name: todoist-github
    restart: unless-stopped
    command: python3 -m todoist_github --interval 900
    environment:
      - TODOIST_TOKEN=
      - GITHUB_TOKEN=
```
