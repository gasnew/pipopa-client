from utils import *
import random

class OnHold():
  RAD_PERIOD = 2
  INFO_PERIOD = 7

  def __init__(self):
    mixer.init()

    self.song_names = filenames('hold')
    self.song_names.sort()
    self.current_song_name = self.song_names[-1]
    self.paused = False
    self.play_count = 0
    self.rad_countdown = self.RAD_PERIOD

  def play(self):
    try:
      if self.rad_countdown == 0:
        name = 'rad/{}'.format(random.choice(filenames('hold/rad')))
        self.rad_countdown = self.RAD_PERIOD
      else:
        names = self.song_names
        name = names[(names.index(self.current_song_name) + 1) % len(names)]
        self.current_song_name = name
        self.rad_countdown -= 1
        self.play_count += 1

      path = '{}/../hold/{}'.format(os.path.dirname(os.path.abspath(__file__)), name)
      mixer.music.load(path)
      mixer.music.play()

      print(' [HOLD] Starting new song ({}): {}'.format(self.play_count, name))
    except Exception as e:
      print('AHHHH')
      print(e)

  def pause(self):
    mixer.music.pause()
    self.paused = True
    print(' [HOLD] Pausing on-hold music...')
