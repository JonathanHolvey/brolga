FROM python:3.7-alpine

ENV PROJECTS_PATH /var/docker

RUN pip install flask

WORKDIR /opt/deploy
COPY src ../deploy

ENTRYPOINT ["python"]
CMD ["/opt/deploy/app.py"]
