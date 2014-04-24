#!/usr/bin/env python3

import RPi.GPIO as gpio

from flask import Flask, make_response, render_template

LED_PIN = 24
gpio.setmode(gpio.BCM)
gpio.setup(LED_PIN, gpio.OUT)

app = Flask(__name__)
app.debug = True

def get_led_state():
  return gpio.input(LED_PIN)

def state_to_string(state):
  return "on" if state else "off"

@app.route("/")
def control_center():
  current_state = get_led_state()
  return render_template("control_center.html", ledState=state_to_string(current_state))

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
  current_state = get_led_state()
  new_state = not current_state
  gpio.output(LED_PIN, new_state)
  return make_response("Light is %s!" % state_to_string(new_state), 200)

if __name__ == "__main__":
  app.run(host='0.0.0.0')
