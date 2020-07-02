from flask import Flask, send_file, jsonify
from .expenses import expenses
from .logger import log
from os import path
import json

# Start application
app = Flask(__name__)


@app.route('/log')
def log_route():
    """ Sends the log file for debug """
    return send_file(path.join('..', 'app.log'), as_attachment=True)


@app.route('/')
def root_route():
    log.info('Test Request Received')
    return 'Success!'


@app.route('/expenses')
def expenses_route():
    log.info('Expenses Request Received')
    return jsonify(expenses())
