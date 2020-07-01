from flask import Flask, jsonify, send_file
from .logger import log
from os import path


# Start application
app = Flask(__name__)


@app.route('/log')
def get_log():
    """ Sends the log file for debug """
    return send_file(path.join('..', 'app.log'), as_attachment=True)


@app.route('/')
def test():
    log.info('Request received')
    return 'Success!'
