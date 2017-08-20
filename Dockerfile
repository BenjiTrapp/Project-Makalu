FROM python:3.4-alpine
LABEL maintainer="benji.trapp@gmail.com"

COPY . /code
COPY static /code/static
COPY templates /code/templates
WORKDIR /code
RUN pip install -r requirements.txt

RUN python ProjectMakaluApp.py