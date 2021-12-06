FROM python:3.9-slim

WORKDIR /usr/src/app/userbot

COPY requirements.txt /usr/src/app/userbot
RUN pip install -r /usr/src/app/userbot/requirements.txt
COPY . /usr/src/app/userbot

CMD python3 -m main