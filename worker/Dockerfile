# Dockerfile
FROM python:3.10-slim

WORKDIR /worker

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY tasks.py .
COPY config.py .
COPY ./params /worker/params
COPY ./algebra /worker/algebra
COPY ./image_process /worker/image_process

EXPOSE 5000

CMD ["celery", "-A", "tasks", "worker", "--loglevel=info", "--pool=solo"]