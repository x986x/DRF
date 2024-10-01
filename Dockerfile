FROM python:3.11-slim
WORKDIR /code
RUN apt update
RUN apt install -y gcc libpq-dev
COPY . .
RUN pip install -r requirements.txt