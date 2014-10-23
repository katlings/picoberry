#!/usr/bin/env python3

import RPi.GPIO as gpio
from RPIO import PWM

from flask import Flask, make_response, render_template

LED_PIN = 24
gpio.setmode(gpio.BCM)
gpio.setup(LED_PIN, gpio.OUT)

servo = PWM.Servo()

app = Flask(__name__)
app.debug = True

# On/off state is kept as a global variable due to PWM.
state = gpio.input(LED_PIN)

def get_led_state():
  return state

def set_led_state(new_state):
  global state
  state = new_state
  return state

def state_to_string(state):
  return "on" if state else "off"

@app.route("/")
def control_center():
  current_state = get_led_state()
  return render_template("control_center.html", ledState=state_to_string(current_state))

@app.route("/on")
def turn_on():
  set_led_state(True)
  gpio.output(LED_PIN, 1)
  return make_response("Light is on!", 200)

@app.route("/off")
def turn_off():
  set_led_state(False)
  gpio.output(LED_PIN, 0)
  return make_response("Light is off!", 200)

@app.route("/toggle")
def toggle():
  current_state = get_led_state()
  new_state = not current_state
  set_led_state(new_state)
  #gpio.output(LED_PIN, new_state)
  if current_state:
    servo.stop_servo(LED_PIN)
  else:
    servo.set_servo(LED_PIN, 1000)
  return make_response("Light is %s!" % state_to_string(new_state), 200)

if __name__ == "__main__":
  app.run(host='0.0.0.0')
