import os
import time

from flask import Flask, render_template
from flask_ask import Ask, statement

app = Flask(__name__)
ask = Ask(app, '/remote/')

# Power represents weather the TV wants to be switched on or off
@ask.intent('TVPowerOn')
def change_tv_power(power):
    message = "I have been reached"
    return statement(message)