FROM python:3.8.1-alpine3.11

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./todoist_github /app/todoist_github

WORKDIR /app

CMD ["python3", "-m", "todoist_github"]
