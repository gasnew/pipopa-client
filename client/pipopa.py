from os import walk
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

    self.p_state.set_state_callback('Standby', self.standby)
    self.p_state.set_state_callback('Recording', self.record)
    self.p_state.set_state_callback('Uploading', self.upload)
    self.p_state.set_state_callback('Downloading', self.download)
    self.p_state.set_state_callback('AwaitingPlayback', self.await_playback)
    self.p_state.set_state_callback('Playing', self.playback)
    self.p_state.set_state_callback('Polling', self.poll)

  def do_thing(self, channel):
    action = 'up' if GPIO.input(channel) else 'down'
    self.p_state.follow_edge(action)

  def standby(self):
    if len(self.current_mids()) > 0:
      self.p_state.follow_edge('waitingMessage')

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
      print(' [UPLOAD] Upload completed!')
      self.p_state.follow_edge('done')
    except Exception as e:
      print(' [ERROR] Upload failed with error:')
      print(e)
      self.p_state.follow_edge('error')

  def download(self):
    print(' [DOWNLOAD] Downloading now...')
    download(self.url, self.credentials, self.new_mids)
    self.new_mids = []
    print(' [DOWNLOAD] Finished downloading!')
    self.p_state.follow_edge('done')

  def await_playback(self):
    mid = self.current_mids()[0]
    print(' [AWAIT_PLAYBACK] Awaiting playback for message {}...'.format(mid))
    pass

  def playback(self):
    mid = self.current_mids()[0]
    print(' [PLAYBACK] Playing back message {}...'.format(mid))
    playback(mid)
    mark_read(self.url, self.credentials, mid)
    delete(mid)
    print(' [PLAYBACK] Finished playing back!')

    if (len(self.current_mids()) > 0):
      self.p_state.follow_edge('more')
    else:
      self.p_state.follow_edge('done')

  def poll(self):
    print(' [POLL] Polling for new messages...')
    new_mids = poll(self.url, self.credentials)
    self.new_mids = [mid for mid in new_mids if mid not in self.current_mids()]

    if len(self.new_mids) > 0:
      print(' [POLL] New message(s) found!')
      print(self.new_mids)
      self.p_state.follow_edge('newMessage')
    else:
      print(' [POLL] No new messages found')
      self.p_state.follow_edge('done')

  def current_mids(self):
    mids = [int(n.split('.')[0]) for n in self.filenames()]
    mids.sort()
    return mids

  def filenames(self):
    (_, _, filenames) = walk('messages').next()
    return filenames
