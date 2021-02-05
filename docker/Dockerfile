FROM python:3.9.1-slim-buster
WORKDIR /code
RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
COPY ./docker/settings.py ./snowbombers/
