from utils import *
from pstate import PState

class PiPoPa:
  def __init__(self, name, password, recipient):
    self.name = name
    self.password = password
    self.recipient = recipient

    self.credentials = {
      'username': self.name,
      'password': self.password,
    }
    self.url = 'http://204.48.25.88:8080'
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
      upload(self.url, self.credentials, self.recipient)
      self.p_state.follow_edge('done')
    except Exception as e:
      print(' [ERROR] Upload failed with error:')
      print(e)
      self.p_state.follow_edge('error')

  def download(self):
    download(self.url, self.credentials, self.new_mids)
    self.p_state.follow_edge('done')

  def await_feedback(self):
    pass

  def playback(self):
    playback()
    self.p_state.follow_edge('done')

  def poll(self):
    print(' [POLL] Polling for new messages...')
    mids = poll(self.url, self.credentials)
    print(mids)
    print(' [POLL] No new messages found')
    self.new_mids = mids
    self.p_state.follow_edge('newMessage')
