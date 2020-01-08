FROM python:3.8.1-alpine3.11

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./todoist-github /app

CMD ["/app/cli.py"]
