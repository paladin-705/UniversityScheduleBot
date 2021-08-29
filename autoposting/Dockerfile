FROM python:3.6-alpine

LABEL maintainer="Sergey Kornev <paladin705@yandex.ru>"

ENV TZ="Europe/Moscow"

ENV DB_NAME=
ENV DB_USER=
ENV DB_PASSWORD=
ENV DB_HOST=

ENV TELEGRAM_API_TOKEN=

ENV STATISTIC_TOKEN=

ENV WEEK_TYPE=

WORKDIR /app

RUN apk update \
    && apk upgrade \
    && apk add tzdata \
    && apk add git build-base postgresql-dev \
    && mkdir log

COPY * ./

RUN pip3 install -r requirements.txt \
    && chmod +x deploy

CMD ./deploy ${DB_NAME} ${DB_USER} ${DB_PASSWORD} ${DB_HOST} \
             ${TELEGRAM_API_TOKEN} \
             ${WEEK_TYPE} ${STATISTIC_TOKEN} ${TZ}
