#FROM ubuntu:latest
FROM python:latest
LABEL authors="vorto"
WORKDIR /contacts
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt .
RUN pip install --upgrade pip && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
ENTRYPOINT ["top", "-b"]
COPY ./entrypoint.sh .
COPY . .