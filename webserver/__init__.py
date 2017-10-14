import logging
import json
from uuid import uuid4

from flask import Flask, request

app = Flask(__name__)


def _generate_token():
    token = str(uuid4())
    # Possible token generation here
    return token

@app.route('/token')
def token():
    return json.loads({'token': _generate_token})

# Handles' the initial questions
@app.route('/questions', methods=['POST'])
def questions():
    if request.method == 'POST':
        return json.dumps({'response': 'I got %s' % request.form.get('response')})
    else:
        logging.debug('I received a non-post packet.')

@app.route('/response', methods=["POST"])
def response():
    if request.method == 'POST':
        return json.dumps({'response': 'I got %s' % request.form.get('response')})
    else:
        logging.debug('I received a non-post packet.')

app.run()
