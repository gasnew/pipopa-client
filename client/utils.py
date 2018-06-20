import RPi.GPIO as GPIO
import time
import pyaudio
import wave
import sys
import requests
import os
import random
from os import walk
from sys import byteorder
from array import array
from struct import pack
from pygame import mixer

def normalize(snd_data):
  # Attenuate spikes and amplify maximally
  MAXIMUM = 2**15
  THRESHOLD = MAXIMUM * 0.12

  tempered = [i if abs(i) < THRESHOLD else THRESHOLD * abs(i) / i for i in snd_data]
  maximum = max(abs(i) for i in tempered)
  scale_factor = float(MAXIMUM)/maximum

  r = array('h')
  for i in tempered:
    val = i*scale_factor
    if abs(i) >= THRESHOLD:
      val = 0

    try:
      r.append(int(val))
    except Exception as e:
      r.append(0)

  return r

def record(check_abort):
  CHUNK = 512
  FORMAT = pyaudio.paInt16
  CHANNELS = 1
  RATE = 44100
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

  try:
    data_all = array('h')
    while not check_abort():
      # little endian, signed short
      data_chunk = array('h', stream.read(CHUNK))
      if byteorder == 'big':
        data_chunk.byteswap()
      data_all.extend(data_chunk)
  except Exception as e:
    print(e)

  print("* done recording")

  stream.stop_stream()
  stream.close()
  p.terminate()

  data_all = normalize(data_all)

  frames = pack('<' + ('h' * len(data_all)), *data_all)
  wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
  wf.setnchannels(CHANNELS)
  wf.setsampwidth(p.get_sample_size(FORMAT))
  wf.setframerate(RATE)
  wf.writeframes(frames)
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

def login(s, url, credentials, timeout=None):
  r = s.post('{}/login'.format(url), credentials, timeout=timeout)

def upload(url, credentials, recipient):
  s = requests.session()

  # Log in
  login(s, url, credentials)

  # Create message
  message = {
    'recipient': recipient,
  }
  r2 = s.post('{}/messages/new'.format(url), message)

  # Upload audio
  mid = r2.json()['id']
  with open('output.wav', 'rb') as f:
    r3 = s.post('{}/messages/upload/{}'.format(url, mid), data=f)

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

def poll(url, credentials, timeout):
  try:
    s = requests.session()

    # Log in
    login(s, url, credentials, timeout)

    # retrieve waiting messages
    r2 = s.get('{}/messages/waiting'.format(url), timeout=timeout)
    mids = [m['id'] for m in r2.json()['messages']]
  except Exception as e:
    print(' [ERROR] {}'.format(e))
    mids = []

  return mids

def mark_read(url, credentials, mid):
  s = requests.session()

  # Log in
  login(s, url, credentials)

  # Mark message as read
  r = s.get('{}/messages/mark-read/{}'.format(url, mid))

def filenames(folder):
  (_, _, filenames) = walk(folder).next()
  return filenames
