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
        self.currentBrightness = 1
        self.color = "blue"
        self.wantedBrightness = 1
        self.options = {
            LightStates.STANDBY : self.standby,
            LightStates.POWER :self.power,
            LightStates.BLUE : self.blue,
            LightStates.RED : self.red,
            LightStates.GREEN : self.green,
            LightStates.NICE_BLUE : self.nice_blue,
            LightStates.FADE : self.fade,
            LightStates.WHITE : self.white,
            LightStates.BRIGHTNESS : self.brightness
        }

    def reset(self):
        global currentState
        self.currentState = LightStates.STANDBY

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
        self.color = "blue"
        os.system("irsend SEND_ONCE LED KEY_BLUE")
        self.reset()

    def red(self):
        self.color = "red"
        os.system("irsend SEND_ONCE LED KEY_RED")
        self.reset()

    def green(self):
        self.color = "green"
        os.system("irsend SEND_ONCE LED KEY_GREEN")
        self.reset()

    def nice_blue(self):
        self.color = "nice-blue"
        os.system("irsend SEND_ONCE LED KEY_NICEBLUE")
        self.reset()

    def fade(self):
        self.color = "fade"
        os.system("irsend SEND_ONCE LED KEY_FADE")
        self.reset()

    def white(self):
        self.color = "white"
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

    def getData(self):
        return {"power": self.lightsOn, "color": self.color, "brightness": self.wantedBrightness}

    def changeState(self, state):
        self.currentState = state
        print("State changed to " + str(state))

    def execute(self):
        self.options[self.currentState]()

    def run(self):
        while(True):
            self.execute()
            sleep(self.delay)