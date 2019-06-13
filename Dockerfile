FROM python:3.7-alpine

ENV DOCKER_HOST unix:///tmp/docker.sock
ENV APP_PATH /opt/deploy
ENV CONFIG_PATH /etc/deploy
ENV PROJECTS_PATH /var/docker

RUN apk add libffi-dev openssl-dev gcc libc-dev make
RUN pip install pipenv docker-compose

WORKDIR $APP_PATH
COPY src/Pipfile* ./
RUN pipenv install

COPY src ../deploy
COPY bin/* /usr/bin/

VOLUME $CONFIG_PATH

EXPOSE 80
ENTRYPOINT ["pipenv", "run"]
CMD ["app"]
