from utils import *
from pstate import PState
from record_thread import RecordThread
from poll_thread import PollThread
from on_hold import OnHold
import threading

class PiPoPa:
  POLL_PERIOD = 4

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
    self.p_state.set_state_callback('Polling', self.start_poll_thread)

    self.led_state = {
      'state': self.p_state.state,
      'period_counter': 0,
      'red': False,
      'green': False,
      'yellow': False,
    }

    self.poll_thread = None

    self.on_hold = OnHold()

    if not os.path.exists('messages'):
      os.makedirs('messages')

  def start(self):
    while True:
      print(' [THREADING] Count: {}'.format(threading.active_count()))
      print(threading.enumerate())
      if self.poll_thread and self.poll_thread.is_alive():
        print(' [POLL] Poll thread already alive...')
      else:
        print(threading.current_thread())
        self.p_state.follow_edge('poll')

      print(' [THREADING] Count: {}'.format(threading.active_count()))
      time.sleep(self.POLL_PERIOD)

  def do_thing(self, channel):
    if self.poll_thread.is_alive():
      print(' [POLL] Joining poll thread...')
      self.poll_thread.join()
    self.on_hold.pause()

    action = 'up' if GPIO.input(channel) else 'down'
    self.p_state.follow_edge(action)

  def standby(self):
    self.on_hold.play()
    if len(self.current_mids()) > 0:
      self.p_state.follow_edge('waitingMessage')

  def record(self):
    try:
      print(' [RECORD] Recording now...')
      self.recordThread = RecordThread(lambda: self.p_state.state == 'Uploading')
      self.recordThread.start()
    except Exception:
      print(' [ERROR] Record failed with error {}'.format(e))
      self.p_state.follow_edge('error')

  def upload(self):
    print(' [UPLOAD] Finishing recording...')
    self.recordThread.join()

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
    try:
      download(self.url, self.credentials, self.new_mids)
      self.new_mids = []
      print(' [DOWNLOAD] Finished downloading!')
      self.p_state.follow_edge('done')
    except Exception as e:
      print(' [ERROR] Upload failed with error:')
      print(e)
      self.p_state.follow_edge('error')

  def await_playback(self):
    self.on_hold.pause()
    mid = self.current_mids()[0]
    print(' [AWAIT_PLAYBACK] Awaiting playback for message {}...'.format(mid))

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

  def start_poll_thread(self):
    timeout = self.POLL_PERIOD - 1
    self.poll_thread = PollThread(lambda: self.poll(timeout))
    self.poll_thread.start()
    print(' [POLL] Starting poll thread!')

  def poll(self, timeout):
    print(' [POLL] Polling for new messages...')
    new_mids = poll(self.url, self.credentials, timeout)
    self.new_mids = [mid for mid in new_mids if mid not in self.current_mids()]

    if len(self.new_mids) > 0:
      print(' [POLL] New message(s) found!')
      print(self.new_mids)
      self.p_state.follow_edge('newMessage')
    else:
      print(' [POLL] No new messages found')
      if len(self.current_mids()) > 0:
        self.p_state.follow_edge('waitingMessage')
      else:
        self.p_state.follow_edge('done')

  def current_mids(self):
    mids = [int(n.split('.')[0]) for n in filenames('messages')]
    mids.sort()
    return mids

  def get_led_state(self):
    self.led_state['state'] = self.p_state.state
    return self.led_state
