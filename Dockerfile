FROM python:3.7-alpine

RUN apk add libffi-dev openssl-dev gcc libc-dev make
RUN pip install pipenv docker-compose

WORKDIR /opt/deploy
COPY src/Pipfile* ./
RUN pipenv install

COPY src ../deploy

ENV DOCKER_HOST unix:///tmp/docker.sock
ENV PROJECTS_PATH /var/docker
ENV CONFIG_PATH /etc/deploy

VOLUME $CONFIG_PATH

EXPOSE 80
ENTRYPOINT ["pipenv", "run"]
CMD ["app"]
