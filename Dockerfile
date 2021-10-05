FROM tiangolo/uwsgi-nginx:python3.7-2021-10-02

ENV LISTEN_PORT=5000
EXPOSE 5000

ENV UWSGI_INI uwsgi.ini

WORKDIR /score_sheet_api

COPY . /score_sheet_api

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 unixodbc-dev -y

COPY requirements.txt /
RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -r /requirements.txt
