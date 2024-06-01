import app
import requests

from app_components import clear_background
from system.eventbus import eventbus
from events.input import Buttons, BUTTON_TYPES
from tildagonos import tildagonos
from system.patterndisplay.events import PatternDisable

URL = "https://roygbivw.hecknswell.com/colour/"

class LeoSuit(app.App):
    def __init__(self):
        eventbus.emit(PatternDisable())
        self.button_states = Buttons(self)
        self.colour = { "r": 0, "g": 0, "b": 0}
        try:
            r = requests.get(URL)
            r.raise_for_status()
            self.colour = r.json()
        except Exception as e:
            print("failed to get colour", e)
        print("init", self.colour)

    def update(self, delta):
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
        data = self.colour
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
            try:
                r = requests.post(URL, json=self.colour)
                r.raise_for_status()
                self.colour = data
                print("successfully updated")
            except Exception as e:
                print("failed to put colour", e)

    def draw(self, ctx):
        clear_background(ctx)
        ctx.rgb(self.colour['r'], self.colour['g'], self.colour['b'])
        ctx.rectangle(-150, -150, 300, 300).fill()

__app_export__ = LeoSuit