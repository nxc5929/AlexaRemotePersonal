from enum import Enum
import os
from time import sleep
import threading

class LightStates(Enum):
    STANDBY = 0
    POWER = 1
    BLUE = 2
    RED = 3
    GREEN = 4
    NICE_BLUE = 5
    FADE = 6
    WHITE = 7
    BRIGHTNESS = 8

class Lights(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.delay = 0.5
        self.currentState = LightStates.STANDBY
        self.lightsOn = False
        self.currentBrightness = 0
        self.wantedBrightness = 0
        self.options = {
            LightStates.STANDBY : standby,
            LightStates.POWER : power,
            LightStates.BLUE : blue,
            LightStates.RED : red,
            LightStates.GREEN : green,
            LightStates.NICE_BLUE : nice_blue,
            LightStates.FADE : fade,
            LightStates.WHITE : white,
            LightStates.BRIGHTNESS : brightness
        }

    def reset(self):
        global currentState
        currentState = LightStates.STANDBY

    def standby(self):
        return

    def power(self):
        os.system("irsend SEND_ONCE LED KEY_POWER")
        self.reset()

    def power_lights(self, on):
        if on != self.lightsOn:
            self.lightsOn = on
            self.changeState(LightStates.POWER)
            return True
        return False

    def blue(self):
        os.system("irsend SEND_ONCE LED KEY_BLUE")
        self.reset()

    def red(self):
        os.system("irsend SEND_ONCE LED KEY_RED")
        self.reset()

    def green(self):
        os.system("irsend SEND_ONCE LED KEY_GREEN")
        self.reset()

    def nice_blue(self):
        os.system("irsend SEND_ONCE LED KEY_NICEBLUE")
        self.reset()

    def fade(self):
        os.system("irsend SEND_ONCE LED KEY_FADE")
        self.reset()

    def white(self):
        os.system("irsend SEND_ONCE LED KEY_WHITE")
        self.reset()

    #1-8
    def brightness(self):
        if(self.currentBrightness > self.wantedBrightness):
            while(self.currentBrightness > self.wantedBrightness):
                os.system("irsend SEND_ONCE LED KEY_BRIGHTDOWN")
                self.currentBrightness = self.currentBrightness - 1
                sleep(0.5)
        else:
            while(self.currentBrightness < self.wantedBrightness):
                os.system("irsend SEND_ONCE LED KEY_BRIGHTUP")
                self.currentBrightness = self.currentBrightness + 1
                sleep(0.5)
        self.reset()

    def set_brightness(self, bright):
        if bright in range(1,9):
            self.wantedBrightness = bright
            self.changeState(LightStates.BRIGHTNESS)
            return True
        else:
            return False

    def changeState(self, state):
        if state is LightStates:
            self.currentState = state
            print("State changed to " + str(state))

    def execute(self):
        self.options[self.currentState](self)

    def run(self):
        while(True):
            print("execute")
            self.execute()
            sleep(self.delay)