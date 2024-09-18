FROM python:3.11

WORKDIR /

COPY ./requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./app /app
COPY ./tests/dms-responses /tests/dms-responses
