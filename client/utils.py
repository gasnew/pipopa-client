import RPi.GPIO as GPIO
import time
import pyaudio
import wave
import sys
import requests

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
  RECORD_SECONDS = 5
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

def playback():
  CHUNK = 512

  if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

  wf = wave.open(sys.argv[1], 'rb')

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

def upload():
  # Log in
  s = requests.session()
  url = 'http://192.168.0.146:8080'
  credentials = {
    'username': 'garrett',
    'password': 'garrett',
  }
  r1 = s.post('{}/login'.format(url), credentials)
  print(r1.status_code)
  print(r1.text)
  print('Logged in!')

  # Create message
  message = {
    'recipient': 'jesse',
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

def download():
  # Log in
  s = requests.session()
  url = 'http://192.168.0.146:8080'
  credentials = {
    'username': 'jesse',
    'password': 'jesse',
  }
  r1 = s.post('{}/login'.format(url), credentials)
  print(r1.status_code)
  print(r1.text)
  print('Logged in!')

  # retrieve waiting messages
  r2 = s.get('{}/messages/waiting'.format(url))
  print('Messages:')
  print(r2.status_code)
  print(r2.text)
  mids = [m['id'] for m in r2.json()['messages']]

  # download those files
  for mid in mids:
    print('message {}'.format(mid))

    filename = '{}.wav'.format(mid)
    r3 = s.get('{}/messages/download/{}'.format(url, mid), stream=True)
    with open(filename, 'wb') as f:
      for chunk in r3.iter_content(chunk_size=512): 
        if chunk: # filter out keep-alive new chunks
          f.write(chunk)
    print(r3.status_code)

  print('FILES DOWNLOADED!!')
