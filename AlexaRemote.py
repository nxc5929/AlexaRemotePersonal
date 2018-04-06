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

# LED STRIP

lightsOn = False

@ask.intent('LightsOn')
def led_lights_on():
    global lightsOn
    if not lightsOn:
        lightsOn = True
        message = "The lights have been turned on"
        os.system("irsend SEND_ONCE LED KEY_POWER")
    else:
        message = "Lights are already on"
    return statement(message)

@ask.intent('LightsOff')
def led_lights_off():
    global lightsOn
    if lightsOn:
        lightsOn = False
        message = "The lights have been turned off"
        os.system("irsend SEND_ONCE LED KEY_POWER")
    else:
        message = "Lights are already off"
    return statement(message)

@ask.intent('LightsBlue')
def led_lights_blue():
    message = "The lights have been turned blue"
    os.system("irsend SEND_ONCE LED KEY_BLUE")
    return statement(message)

@ask.intent('LightsRed')
def led_lights_red():
    message = "The lights have been turned red"
    os.system("irsend SEND_ONCE LED KEY_RED")
    return statement(message)

@ask.intent('LightsGreen')
def led_lights_green():
    message = "The lights have been turned green"
    os.system("irsend SEND_ONCE LED KEY_GREEN")
    return statement(message)

@ask.intent('LightsNiceBlue')
def led_lights_nice_blue():
    message = "The lights have been turned a nice shade of blue"
    os.system("irsend SEND_ONCE LED KEY_NICEBLUE")
    return statement(message)

@ask.intent('LightsFade')
def led_lights_fade():
    message = "The lights have been set to fade"
    os.system("irsend SEND_ONCE LED KEY_FADE")
    return statement(message)

currentBrightness = 0
@ask.intent('LightsBrightness', convert={'brightness': int})
def led_lights_brightness(brightness):
    global currentBrightness
    message = render_template('brightnessSet', brightness=brightness)
    if(currentBrightness < brightness):
        for x in range(1, brightness-currentBrightness):
            os.system("irsend SEND_ONCE LED KEY_BRIGHTUP")
    else:
        for x in range(1, currentBrightness-brightness):
            os.system("irsend SEND_ONCE LED KEY_BRIGHTDOWN")
    currentBrightness = brightness
    return statement(message)

if __name__ == '__main__':
    app.run(debug=True)
