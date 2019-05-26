#! /usr/bin/env python

from flask import Flask, request, abort
from os import environ as env
import json

import vendors
from docker import deploy

app = Flask('Docker Webhook Deploy')


# Main webhook route
@app.route('/hooks/<vendor>', methods=['POST'])
def hook(vendor):
    try:
        # Load payload from JSON data
        payload = json.loads(request.data)
        config = vendors[vendor](payload)
    except Exception:
        return abort(400)

    # Run deployments in project directory
    deploy(config, env['PROJECTS_PATH'])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
