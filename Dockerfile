FROM python:3.7.8

RUN pip install -r requirements.txt

COPY src/ app/
WORKDIR /app

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threade 8 app:app
