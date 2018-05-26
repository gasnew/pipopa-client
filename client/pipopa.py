from utils import *
from pstate import PState

class PiPoPa:
  def __init__(self):
    self.p_state = PState('Standby')

    self.p_state.set_state_callback('Recording', self.record)

  def do_thing(self, channel):
    action = 'up' if GPIO.input(channel) else 'down'
    self.p_state.follow_edge(action)

  def record(self):
    print(' [STATE] Recording now...')
