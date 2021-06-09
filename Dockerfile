FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python","main.py"]
ENTRYPOINT ["gunicorn","--bind=0.0.0.0:8080","main:app"]