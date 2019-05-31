FROM python:3.7-alpine

ENV DOCKER_HOST unix:///tmp/docker.sock
ENV PROJECTS_PATH /var/docker

RUN apk add libffi-dev openssl-dev gcc libc-dev make
RUN pip install flask docker-compose

WORKDIR /opt/deploy
COPY src ../deploy

ENTRYPOINT ["python"]
CMD ["/opt/deploy/app.py"]
