from flask import Flask, send_file
from .expenses import expenses
from .logger import log
from os import path


# Start application
app = Flask(__name__)


@app.route('/log')
def get_log():
    """ Sends the log file for debug """
    return send_file(path.join('..', 'app.log'), as_attachment=True)


@app.route('/')
def root():
    log.info('Test Request Received')
    return 'Success!'


@app.route('/expenses')
def test():
    log.info('Expenses Request Received')
    return expenses()
