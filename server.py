#!/usr/bin/env python3

import RPi.GPIO as gpio

from flask import Flask, make_response

LED_PIN = 24
gpio.setmode(gpio.BCM)
gpio.setup(LED_PIN, gpio.OUT)

app = Flask(__name__)
app.debug = True

@app.route("/")
def hello():
  return "Hello world"

@app.route("/on")
def turn_on():
  gpio.output(LED_PIN, 1)
  return make_response("Light is on!", 200)

@app.route("/off")
def turn_off():
  gpio.output(LED_PIN, 0)
  return make_response("Light is off!", 200)

@app.route("/toggle")
def toggle():
  current_state = gpio.input(LED_PIN)
  gpio.output(LED_PIN, not current_state)
  new_state = "off" if current_state else "on"
  return make_response("Light is %s!" % new_state, 200)

if __name__ == "__main__":
  app.run(host='0.0.0.0')
