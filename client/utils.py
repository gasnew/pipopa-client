import RPi.GPIO as GPIO
import time
import pyaudio
import wave
import sys
import requests
import os

def normalize(snd_data):
  "Average the volume out"
  MAXIMUM = 16384
  scale_factor = float(MAXIMUM)/max(abs(i) for i in snd_data)

  r = array('h')
  for i in snd_data:
    r.append(int(i*scale_factor))
  return r

def record():
  CHUNK = 512
  FORMAT = pyaudio.paInt16
  CHANNELS = 1
  RATE = 44100
  RECORD_SECONDS = 3
  WAVE_OUTPUT_FILENAME = "output.wav"

  if sys.platform == 'darwin':
    CHANNELS = 1

  p = pyaudio.PyAudio()

  stream = p.open(format=FORMAT,
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  frames_per_buffer=CHUNK)

  print("* recording")

  frames = []

  for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

  print("* done recording")

  stream.stop_stream()
  stream.close()
  p.terminate()

  joined_frames = b''.join(frames)
  #joined_frames = normalize(joined_frames)

  wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
  wf.setnchannels(CHANNELS)
  wf.setsampwidth(p.get_sample_size(FORMAT))
  wf.setframerate(RATE)
  wf.writeframes(joined_frames)
  wf.close()

def playback(mid):
  CHUNK = 512

  path = '{}/../messages'.format(os.path.dirname(os.path.abspath(__file__)))
  filename = '{}/{}.wav'.format(path, mid)
  wf = wave.open(filename, 'rb')

  # instantiate PyAudio (1)
  p = pyaudio.PyAudio()

  # open stream (2)
  stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                  channels=wf.getnchannels(),
                  rate=wf.getframerate(),
                  output=True)

  # read data
  data = wf.readframes(CHUNK)

  # play stream (3)
  while len(data) > 0:
    stream.write(data)
    data = wf.readframes(CHUNK)

  # stop stream (4)
  stream.stop_stream()
  stream.close()

  # close PyAudio (5)
  p.terminate()

def delete(mid):
  path = '{}/../messages'.format(os.path.dirname(os.path.abspath(__file__)))
  filename = '{}/{}.wav'.format(path, mid)
  os.unlink(filename)

def login(s, url, credentials):
  r = s.post('{}/login'.format(url), credentials)
  print(r.status_code)
  print('Logged in!')

def upload(url, credentials, recipient):
  s = requests.session()

  # Log in
  login(s, url, credentials)

  # Create message
  message = {
    'recipient': recipient,
  }
  r2 = s.post('{}/messages/new'.format(url), message)
  print('Message created?')
  print(r2.status_code)
  print(r2.text)

  # Upload audio
  mid = r2.json()['id']
  with open('output.wav', 'rb') as f:
    r3 = s.post('{}/messages/upload/{}'.format(url, mid), data=f)

  print(r3.status_code)
  print('POSTED!!!')

def download(url, credentials, mids):
  s = requests.session()

  # Log in
  login(s, url, credentials)

  # download those files
  path = '{}/../messages'.format(os.path.dirname(os.path.abspath(__file__)))
  for mid in mids:
    print('message {}'.format(mid))

    filename = '{}/{}.wav'.format(path, mid)
    r3 = s.get('{}/messages/download/{}'.format(url, mid), stream=True)
    if r3.status_code == 200:
      with open(filename, 'wb') as f:
        for chunk in r3.iter_content(chunk_size=512): 
          if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    print(r3.status_code)

  print('FILES DOWNLOADED!!')

def poll(url, credentials):
  s = requests.session()

  # Log in
  login(s, url, credentials)

  # retrieve waiting messages
  r2 = s.get('{}/messages/waiting'.format(url))
  print(r2.status_code)
  mids = [m['id'] for m in r2.json()['messages']]

  return mids

def mark_read(url, credentials, mid):
  s = requests.session()

  # Log in
  login(s, url, credentials)

  # Mark message as read
  r = s.get('{}/messages/mark-read/{}'.format(url, mid))
  print(r.status_code)
