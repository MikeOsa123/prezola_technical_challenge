# Base Image
FROM python:3.7.2-stretch

RUN adduser prezola
# create and set working directory
RUN mkdir /app
WORKDIR /app

ADD . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN chmod +x boot.sh

ENV FLASK_APP prezola.py

RUN chown -R prezola:prezola ./
USER prezola

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]