FROM python:3.6.15

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python app.py"]