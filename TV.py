from enum import Enum
import os
from time import sleep
import threading

class TVStates(Enum):
    STANDBY = 0
    POWER = 1
    VOLUME = 2
    INPUT = 3
    MUTE = 4

class TV(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.delay = 0.5
        self.currentState = TVStates.STANDBY
        self.tvOn = False
        self.currentVolume = 0
        self.wantedVolume = 0
        self.options = {
            TVStates.STANDBY: self.standby,
            TVStates.POWER:  self.power,
            TVStates.VOLUME: self.volume,
            TVStates.INPUT: self.input,
            TVStates.MUTE: self.mute
        }

    def reset(self):
        global currentState
        self.currentState = TVStates.STANDBY

    def standby(self):
        return

    def power(self):
        os.system("irsend SEND_ONCE Sony-TV KEY_POWER")
        self.reset()

    def mute(self):
        os.system("irsend SEND_ONCE Sony-TV KEY_MUTE")
        self.reset()

    def input(self):
        os.system("irsend SEND_ONCE Sony-TV KEY_INPUT")
        self.reset()

    def power_tv(self, on):
        if on != self.tvOn:
            self.tvOn = on
            self.changeState(TVStates.POWER)
            return True
        return False

    #0-100
    def volume(self):
        if(self.currentVolume > self.wantedVolume):
            while(self.currentVolume > self.wantedVolume):
                os.system("irsend SEND_ONCE Sony-TV KEY_VOLUMEDOWN")
                self.currentVolume = self.currentVolume - 1
                sleep(0.5)
        else:
            while(self.currentVolume < self.wantedVolume):
                os.system("irsend SEND_ONCE LED KEY_VOLUMEUP")
                self.currentVolume = self.currentVolume + 1
                sleep(0.5)
        self.reset()

    def set_volume(self, volume):
        if volume in range(0,101):
            self.wantedVolume = volume
            self.changeState(TVStates.VOLUME)
            return True
        else:
            return False

    def set_volume_up(self):
        self.set_volume(self.wantedVolume + 2)

    def set_volume_down(self):
        self.set_volume(self.wantedVolume - 2)

    def getData(self):
        return {"power": self.tvOn, "volume": self.volume}

    def changeState(self, state):
        self.currentState = state
        print("State changed to " + str(state))

    def execute(self):
        self.options[self.currentState]()

    def run(self):
        while(True):
            self.execute()
            sleep(self.delay)