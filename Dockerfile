# FROM python:3.8.12-bullseye
FROM python:3.11.0-bullseye

# Fix timezone container
ENV TZ=America/New_York
ENV TERM=xterm
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


WORKDIR /app

COPY . .

RUN pip install -r requirements.txt