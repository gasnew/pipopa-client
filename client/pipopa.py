from utils import *
from pstate import PState

class PiPoPa:
  def __init__(self):
    self.p_state = PState('Standby')

    self.p_state.set_state_callback('Recording', self.record)
    self.p_state.set_state_callback('Uploading', self.upload)
    self.p_state.set_state_callback('Playing', self.playback)

  def do_thing(self, channel):
    action = 'up' if GPIO.input(channel) else 'down'
    self.p_state.follow_edge(action)

  def record(self):
    try:
      print(' [RECORD] Recording now...')
      record()
      print(' [RECORD] Finished recording!')
      self.p_state.follow_edge('done')
    except Exception:
      print(' [ERROR] Record failed with error {}'.format(e))
      self.p_state.follow_edge('error')

  def upload(self):
    upload()
    self.p_state.follow_edge('done')
