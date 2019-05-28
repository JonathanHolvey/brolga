#! /usr/bin/env python

from flask import Flask, request
from flask.json import jsonify as response
from os import environ as env

import translators
from deploy import Deploy

app = Flask('Docker Webhook Deploy')


# Main webhook route
@app.route('/hooks/<vendor>', methods=['POST'])
def hook(vendor):
    app.logger.info('Calling webhook translator for {}'.format(vendor))
    try:
        repo, tag, secret = getattr(translators, vendor)(request.data, request.args)
    except Exception as error:
        app.logger.error(error)
        return response(success=False), 400

    # Run deployments in project directory
    deploy = Deploy(env['PROJECTS_PATH'], app.logger)
    deploy.run(repo, tag)

    return response(success=True), 202


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
