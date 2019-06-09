#! /usr/bin/env python

from flask import Flask, request
from flask.json import jsonify as response
from os import environ as env

import translators
from deploy import Deploy

app = Flask('Docker Webhook Deploy')


@app.route('/hooks/<vendor>', methods=['POST'])
def hook(vendor):
    """Main webhook route"""

    app.logger.info('Calling webhook translator for {}'.format(vendor))
    try:
        repo, tag, secret = getattr(translators, vendor)(request)
    except Exception as error:
        app.logger.error(error)
        return response(success=False), 400

    # Check for valid secret
    if not auth(secret):
        return response(success=False), 401

    # Run deployments in project directory
    deploy = Deploy(env['PROJECTS_PATH'], app.logger)
    deploy.run(repo, tag)

    return response(success=True), 202


def auth(secret):
    """Validate a secret against the secrets file"""
    try:
        with open(env['SECRETS_FILE'], 'r') as f:
            secrets = f.read().splitlines()
        return secret in secrets
    except FileNotFoundError:
        return False


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
