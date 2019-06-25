FROM python:3.7-alpine

RUN apk add libffi-dev openssl-dev gcc libc-dev make \
    && pip install pipenv docker-compose

ENV DOCKER_HOST=unix:///tmp/docker.sock \
    APP_PATH=/opt/brolga \
    CONFIG_PATH=/etc/opt/brolga \
    PROJECTS_PATH=/var/docker

WORKDIR $APP_PATH
COPY src/Pipfile* ./
RUN pipenv install

COPY src ../brolga
COPY bin/* /usr/local/bin/

VOLUME $CONFIG_PATH

EXPOSE 80
ENTRYPOINT ["pipenv", "run"]
CMD ["app"]
