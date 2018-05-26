from utils import *
from pstate import PState

class PiPoPa:
  def __init__(self):
    self.p_state = PState('Standby')

    self.p_state.set_state_callback('Recording', self.record)
    self.p_state.set_state_callback('Uploading', self.upload)
    self.p_state.set_state_callback('Downloading', self.download)
    self.p_state.set_state_callback('AwaitingFeedback', self.await_feedback)
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
    print(' [UPLOAD] Uploading now...')
    try:
      url = 'http://204.48.25.88:8080'
      credentials = {
        'username': 'garrett',
        'password': 'garrett',
      }
      upload(url, credentials, 'jesse')
      self.p_state.follow_edge('done')
    except Exception as e:
      print(' [ERROR] Upload failed with error:')
      print(e)
      self.p_state.follow_edge('error')

  def download(self):
    download()
    self.p_state.follow_edge('done')

  def await_feedback(self):
    pass

  def playback(self):
    playback()
    self.p_state.follow_edge('done')
