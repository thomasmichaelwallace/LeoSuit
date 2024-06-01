import math
import app
import requests

from app_components import clear_background
from system.eventbus import eventbus
from events.input import Buttons, BUTTON_TYPES
from tildagonos import tildagonos
from system.patterndisplay.events import PatternDisable

URL = "http://roygbivw.hecknswell.com/colour/"
TIMEOUT = 8

class LeoSuit(app.App):

    def set_colour(self, json):
        try:
            print("setting", json)
            requests.post(URL, json=json, timeout=TIMEOUT)
            self.colour['r'] = json['r']
            self.colour['g'] = json['g']
            self.colour['b'] = json['b']
            print("successfully updated")
            return True
        except Exception as e:
            print("failed to put colour", e)
            return False
        


    def refresh(self):
        self.t += 1
        if self.t > 25:
            self.t = 0
            try:
                self.error = None
                r = requests.get(URL, timeout=TIMEOUT)
                json = r.json()
                print("got", json)
                if json['r']:
                    self.colour["r"] = json['r']
                if json['g']:
                    self.colour["g"] = json['g']
                if json['b']:
                    self.colour["b"] = json['b']
            except Exception as e:
                print("failed to get colour", e)    
                # self.error = e
            print("refreshed", self.colour)

    def __init__(self):
        self.colour = { "r": 0, "g": 0, "b": 0}
        self.t = 0
        self.d = 0
        self.error = None
        self.button_states = Buttons(self)
        eventbus.emit(PatternDisable())

    def update(self, delta):
        self.refresh()
        # force leds to change every time
        tildagonos.leds[2] = (255, 0, 0)
        tildagonos.leds[3] = (255, 0, 0)
        tildagonos.leds[8] = (0, 255, 0)
        tildagonos.leds[9] = (0, 255, 0)
        tildagonos.leds[12] = (0, 0, 255)
        tildagonos.leds[1] = (0, 0, 255)
        tildagonos.leds[6] = (255, 255, 0)
        tildagonos.leds[7] = (255, 255, 0)
        tildagonos.leds[10] = (0, 255, 255)
        tildagonos.leds[11] = (0, 255, 255)
        tildagonos.leds[4] = (255, 0, 255)
        tildagonos.leds[5] = (255, 0, 255)
        # get colour matching button led
        data = {
            "r": self.colour["r"],
            "g": self.colour["g"],
            "b": self.colour["b"]
        }
        if self.button_states.get(BUTTON_TYPES["RIGHT"]):
            data = { "r": 255, "g": 0, "b": 0}
        elif self.button_states.get(BUTTON_TYPES["LEFT"]):
            data = { "r": 0, "g": 255, "b": 0}
        elif self.button_states.get(BUTTON_TYPES["UP"]):
            data = { "r": 0, "g": 0, "b": 255}
        elif self.button_states.get(BUTTON_TYPES["DOWN"]):
            data = { "r": 255, "g": 255, "b": 0}
        elif self.button_states.get(BUTTON_TYPES["CANCEL"]):
            data = { "r": 0, "g": 255, "b": 255}
        elif self.button_states.get(BUTTON_TYPES["CONFIRM"]):
            data = { "r": 255, "g": 0, "b": 255}

        if data["r"] != self.colour["r"] or data["g"] != self.colour["g"] or data["b"] != self.colour["b"]:
            print("putting", self.colour, "to", data)
            while not self.set_colour(data):
                pass

    def draw(self, ctx):
        self.d += 1
        print("drawing", self.colour, self.d, self.error)
        ctx.rgb(self.colour['r'], self.colour['g'], self.colour['b']).move_to(-0,0).rectangle(-120, -120, 120*2, 120*2).fill()
        dots = ""
        for _ in range(0, math.floor(self.d / 12) % 3 + 1):
            dots += "."
        ctx.rgb(255, 255, 255).move_to(-110,-15).text("roygbiVW " + dots)
        # if self.error is not None:
        #     ctx.rgb(255, 255, 255).move_to(-120,0).text(repr(self.error))
        ctx.rgb(255, 255, 255).move_to(-110,15).text("" + str(self.colour['r']) + "/" + str(self.colour['g']) + "/" + str(self.colour['b']))

__app_export__ = LeoSuit