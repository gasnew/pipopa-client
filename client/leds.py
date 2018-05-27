import RPi.GPIO as GPIO
import time
from threading import Thread

RED_PIN = 18
GREEN_PIN = 15
YELLOW_PIN = 14

class LEDs(Thread):
  STATE_MAPS = {
    'Standby': {
    },
    'Recording': {
      'red': 'on',
    },
    'Uploading': {
      'period': 1,
      'yellow': 'blink',
    },
    'Downloading': {
      'yellow': 'blink',
    },
    'AwaitingPlayback': {
      'period': 20,
      'green': 'blink',
    },
    'Playing': {
      'green': 'on',
    },
    'Polling': {
      'yellow': 'blink',
    },
  }
  BLINK_PERIOD = 0.05

  def __init__(self, get_state):
    Thread.__init__(self)
    self.get_state = get_state

  def run(self):
    while True:
      self.update_leds(
        state = self.get_state(),
        red = RED_PIN,
        green = GREEN_PIN,
        yellow = YELLOW_PIN,
      )

      time.sleep(self.BLINK_PERIOD)

  def update_leds(self, state, red, green, yellow):
    channels = {
      'red': red,
      'green': green,
      'yellow': yellow,
    }
    state_map = self.STATE_MAPS[state['state']]
    for channel_name in channels:
      channel_map = state_map.get(channel_name, 'off')
      channel = channels[channel_name]

      if channel_map == 'on':
        state[channel_name] = True
      elif channel_map == 'blink':
        if state['period_counter'] >= state_map.get('period', 1):
          state[channel_name] = False if state[channel_name] else True
          state['period_counter'] = 0
        state['period_counter'] += 1
      else:
        state[channel_name] = False

      GPIO.output(channel, state[channel_name])
