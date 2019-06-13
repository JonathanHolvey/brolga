FROM python:3.7-alpine

RUN apk add libffi-dev openssl-dev gcc libc-dev make \
    && pip install pipenv docker-compose

ENV DOCKER_HOST=unix:///tmp/docker.sock \
    APP_PATH=/opt/deploy \
    CONFIG_PATH=/etc/deploy \
    PROJECTS_PATH=/var/docker \
    PYTHONPATH=$PYTHONPATH:$APP_PATH

WORKDIR $APP_PATH
COPY src/Pipfile* ./
RUN pipenv install

COPY src ../deploy
COPY bin/* /usr/bin/

VOLUME $CONFIG_PATH

EXPOSE 80
ENTRYPOINT ["pipenv", "run"]
CMD ["app"]
