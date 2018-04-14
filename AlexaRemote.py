import json
from Lights import Lights, LightStates

from flask import Flask, render_template, current_app, request
from flask_ask import Ask, statement

app = Flask(__name__)
ask = Ask(app, '/remote/')

light_thread = Lights(1, "Lights-1", 1)
light_thread.start()

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

##################################################
# LED STRIP
##################################################

@ask.default_intent
def default():
    message = "This feature hasn't been added yet"
    return statement(message)

@ask.intent('LightsOn')
def led_lights_on():
    if light_thread.power_lights(True):
        message = "Lights have been turned on"
    else:
        message = "Lights are already on"
    return statement(message)

@ask.intent('LightsOff')
def led_lights_off():
    if light_thread.power_lights(False):
        message = "The lights have been turned off"
    else:
        message = "Lights are already off"
    return statement(message)

@ask.intent('LightsBlue')
def led_lights_blue():
    message = "The lights have been turned blue"
    light_thread.changeState(LightStates.BLUE)
    return statement(message)

@ask.intent('LightsRed')
def led_lights_red():
    message = "The lights have been turned red"
    light_thread.changeState(LightStates.RED)
    return statement(message)

@ask.intent('LightsGreen')
def led_lights_green():
    message = "The lights have been turned green"
    light_thread.changeState(LightStates.GREEN)
    return statement(message)

@ask.intent('LightsNiceBlue')
def led_lights_nice_blue():
    message = "The lights have been turned a nice shade of blue"
    light_thread.changeState(LightStates.NICE_BLUE)
    return statement(message)

@ask.intent('LightsWhite')
def led_lights_white():
    message = "The lights have been turned white"
    light_thread.changeState(LightStates.WHITE)
    return statement(message)

@ask.intent('LightsFade')
def led_lights_fade():
    message = "The lights have been set to fade"
    light_thread.changeState(LightStates.FADE)
    return statement(message)

@ask.intent('LightsBrightness', convert={'brightness': int})
def led_lights_brightness(brightness):
    if light_thread.set_brightness(brightness):
        message = render_template('brightnessSet', brightness=brightness)
    else:
        message = "Brightness must be in range 1 to 8. Please try again."
    return statement(message)

@app.route('/updateLightData', methods=['POST'])
def update_lights_data():
    new_data = request.get_json()
    print(new_data)
    old_data = json.loads(get_lights_data())
    print(old_data)
    if new_data.get('power') != old_data.get('power'):
        light_thread.power_lights(new_data.get('power'))
    if new_data.get('color') != old_data.get('color'):
        color = new_data.get('color')
        if color == "blue":
            light_thread.changeState(LightStates.BLUE)
        elif  color == "nice-blue":
            light_thread.changeState(LightStates.NICE_BLUE)
        elif  color == "green":
            light_thread.changeState(LightStates.GREEN)
        elif color == "red":
            light_thread.changeState(LightStates.RED)
        elif color == "white":
            light_thread.changeState(LightStates.WHITE)
        elif color == "flow":
            light_thread.changeState(LightStates.FADE)
    if new_data.get('brightness') != old_data.get('brightness'):
        light_thread.set_brightness(new_data.get('brightness'))
    return "Success"

@app.route('/getLightData', methods=['GET'])
def get_lights_data():
    return json.dumps(light_thread.getData())

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return current_app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)