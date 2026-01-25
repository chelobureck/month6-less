FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /shop_api_app

COPY requirements.txt /shop_api_app/requirements.txt

RUN pip install -r requirements.txt

COPY . .