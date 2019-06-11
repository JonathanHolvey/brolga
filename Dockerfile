FROM python:3.7-alpine

RUN apk add libffi-dev openssl-dev gcc libc-dev make
RUN pip install pipenv docker-compose

ENV DOCKER_HOST unix:///tmp/docker.sock
ENV PROJECTS_PATH /var/docker
ENV SECRETS_FILE /etc/secrets

WORKDIR /opt/deploy
COPY src/Pipfile* ./
RUN pipenv install

COPY src ../deploy

EXPOSE 80

ENTRYPOINT ["pipenv", "run"]
CMD ["app"]
