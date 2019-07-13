# Brolga

A simple webhook listener for reloading updated Docker containers.

## How it works

Brolga runs in a container that shares the Docker socket from the host system, allowing it to control other containers running on the host. Container configuration is managed using Docker Compose so that a container that is stopped by Brolga can be started again with exactly the same configuration.

During setup, you provide a folder containing `docker-compose.yml` files for your services. On receipt of a valid webhook, Brolga will scan this folder, looking for services using the image specified in the hook. Any matching services will be restarted after the new image has been pulled from the image repository.

## Setup

A basic Docker Compose config can be used to quickly get a Brolga service running on port 8080:

```yaml
version: '3.7',

services:
  web:
    image: jonathanholvey/brolga:latest
    container_name: brolga
    restart: always
    volumes:
      - /var/run/docker.sock:/tmp/docker.sock:ro
      - /var/docker:/var/docker # Projects volume (see below)
      - ./config:/etc/opt/brolga
    ports:
      - '8080:80'
```

Start the server and check it is running:

```bash
docker-compose up -d
curl "http://localhost:8080/hooks/generic"
```

### Projects volume

The `docker-compose.yml` files for the services being deployed need to be included in a volume so that Brolga can restart the containers with the correct configuration.

The projects volume is searched recursively for the filenames `docker-compose.yml` and `docker-compose.yaml`, allowing project files to be organised into sub-folders.

If a project uses volumes with relative paths, the services volume should mount to the same path in the Brolga container and in the host, as in the example above. The path in the Brolga container can be changed using the environment variable `PROJECTS_PATH`.

### Webhook keys

Simple authentication is provided using secret keys. In order to call a webhook endpoint, you must provide a key in the hook request. If the key can't be verified, the request will be refused with code 401. Keys prevent public access to the webhook API, and hence should be kept safe.

A command line tool Keystore is provided for managing secret keys. Generate a key by running the following command, where `<name>` is a descriptive name to assign to the key:

```bash
docker exec brolga keystore add <name>
```

Once the key has been generated, it can be added to the webhook. Usually, the key can be specified with a `key` parameter in the request URL. Note that the Brolga container must be restarted before a new key can be used.

Note that after generating a key, it is impossible to retrieve it again. If a key is forgotten or lost, a replacement will have to be generated.

For more information on using the Keystore tool, run `docker exec brolga keystore --help`.

### SSL

This project doesn't provide SSL integration for HTTPS transport. It is recommended that an external service is used for this, such as [jwilder/nginx-proxy](https://github.com/jwilder/nginx-proxy).

## Webhook handlers

Support is included for webhooks from Dockerhub, as well as a generic GET request hook. Additional webhook handlers can be created by extending the class `BaseHook` (pull requests are welcome).

### Dockerhub

This handler accepts the standard request body supplied by Docker Hub webhooks. It requires a secret key to be included as a URL parameter in the webhook URL field when configuring the webhook on the Docker Hub website. The handler will send the result of the deployment (`success` or `failure`) to Docker Hub as JSON on completion. An example webhook payload can be found in `examples/payload.json`.

#### Example URL

```
https://deploy.example.com/hooks/dockerhub?key=kgkki-qyGE6cSHTGqnKQTr00SWbax8vOmKlelo
```

### Generic hook

This handler accepts generic hook data as a GET request. A secret key must be sent as a URL parameter, as well as the options `repo` and `tag` which spcify the image to be deployed. This hook can be used with any service that sends HTTP GET requests, including web browsers, making it useful for testing and debugging.

#### Example URL

```
https://deploy.example.com/hooks/generic?key=kgkki-qyGE6cSHTGqnKQTr00SWbax8vOmKlelo&repo=example-repository&tag=latest
```

## Todo

This project is a work in progress. Here are a few features that aren't yet implemented, but probably should be:

1. A proper web server, rather than Flask's dev server
2. Support for pulling from private Docker Hub repositories
