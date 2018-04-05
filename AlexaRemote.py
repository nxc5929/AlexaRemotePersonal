import os
import time

from flask import Flask, render_template
from flask_ask import Ask, statement

app = Flask(__name__)
ask = Ask(app, '/remote/')

@ask.launch
def launch():
    message = "Hello Kaylie. I am the Alexa Remote. " \
              "You can ask me to power on or off the tv, turn volume up or down, and change inputs. " \
              "What would you like to do?"
    return statement(message)

@ask.intent('TVPowerOn')
def power_on():
    message = "TV has been turned on"
    return statement(message)

@ask.intent('TVPowerOff')
def power_off():
    message = "TV has been turned off"
    return statement(message)

@ask.intent('TVVolumeUp')
def volume_up():
    message = "Volume has been turned up"
    return statement(message)

@ask.intent('TVVolumeDown')
def volume_down():
    message = "Volume has been turned down"
    return statement(message)

@ask.intent('TVVolumeSet', convert={'volume': int})
def volume_set(volume):
    message = render_template('volumeSet', volume=volume)
    return statement(message)

@ask.intent('TVVolumeSetup')
def volume_setup():
    message = "Volume has been setup"
    return statement(message)

@ask.intent('TVChangeInput')
def input_change():
    message = "The input has been changed"
    return statement(message)


@ask.intent('LEDLightsON')
def led_lights_on():
    message = "The lights have been turned on"
    os.system("irsend SEND_ONCE LED KEY_POWER")
    return statement(message)

@ask.intent('LEDLightsOff')
def led_lights_off():
    message = "The lights have been turned off"
    os.system("irsend SEND_ONCE LED KEY_POWER")
    return statement(message)

if __name__ == '__main__':
    app.run(debug=True)
