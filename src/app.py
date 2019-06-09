#! /usr/bin/env python

from flask import Flask, request
from flask.json import jsonify as response
from os import environ as env
from threading import Thread

import translators
from hook import Hook
from deploy import Deploy

app = Flask('Docker Webhook Deploy')


@app.route('/hooks/<vendor>', methods=['POST'])
def hook(vendor):
    """Main webhook route"""

    translator = getattr(translators, vendor)()
    app.logger.info('Calling webhook translator for {}'.format(translator.name))
    try:
        hookdata = Hook(*translator.readhook(request))
    except Exception as error:
        app.logger.error('Could not read hook data: {}'.format(error))
        return response(success=False), 400

    # Check for valid secret
    if not auth(hookdata.secret):
        return response(success=False), 401

    # Run deployments in project directory asynchronously
    deploy = Deploy(env['PROJECTS_PATH'], app.logger)
    thread = Thread(target=deploy.run, args=(hookdata.repo, hookdata.tag))
    thread.start()

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
