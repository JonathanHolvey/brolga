#! /usr/bin/env python

from flask import Flask, request
from flask.json import jsonify as response
from os import environ as env
from os import path
from threading import Thread

import hooks
from deploy import Deploy
from keys import Keystore

app = Flask('Docker Webhook Deploy')
auth = Keystore(path.join(env['CONFIG_PATH'], 'keys'))


@app.route('/hooks/<vendor>', methods=['GET', 'POST'])
def hook_controller(vendor):
    """Main webhook route"""

    hook = getattr(hooks, vendor)()
    app.logger.info('Loading {} webhook data'.format(hook.name))
    try:
        hook.read(request)
    except Exception as error:
        app.logger.error('Could not read hook data: {}'.format(error))
        return response(success=False, message='Client error'), 400

    # Check for valid secret
    if not auth.verify(hook.key):
        return response(success=False, message='Access denied'), 401

    # Run deployments in project directory asynchronously
    deploy = Deploy(env['PROJECTS_PATH'], app.logger)
    thread = Thread(target=deploy.run, args=(hook,))
    thread.start()

    return response(success=True, message='Deployment scheduled'), 202


if __name__ == '__main__':
    debug = env.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port='80')
