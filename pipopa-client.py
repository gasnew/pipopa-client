# Important imports
import RPi.GPIO as GPIO
import time

# Cheery channels
RED_PIN = 18
BUTTON_PIN = 23

# Interesting inits
GPIO.setmode(GPIO.BCM) # make diagram life happy

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Classy classes
class PiPoPa:
  def __init__(self):
    self.p_state = PState()

  def do_thing(self, channel):
    action = 'up' if GPIO.input(channel) else 'down'
    print(action)
    self.p_state.follow_edge(action)

class PState:
  STATE_GRAPH = { 
    'Standby': {
      'down': 'Recording',
      'messageReady': 'Pending',
    },
    'Recording': {
      'up': 'Uploading',
    },
    'Uploading': {
      'done': 'Standby',
    },
    'Pending': {
      'down': 'Playing',
    },
    'Playing': {
      'done': 'Standby',
    },
  }

  def __init__(self):
    self.state_callbacks = {}

  def set_state_callback(self, state, callback):
    self.state_callbacks[state] = callback

  def follow_edge(self, action):
    self.state = self.STATE_GRAPH[self.state][action]
    self.state_callbacks[self.state]()

# Impeccable initializations
pipopa = PiPoPa()

# Eventful events
GPIO.add_event_detect(BUTTON_PIN,
  GPIO.BOTH,
  callback=pipopa.do_thing)

while True:
  time.sleep(5)
