import RPi.GPIO as GPIO

STATE_MAPS = {
  'Standby': {
  },
  'Recording': {
    'red': 'on',
  },
  'Uploading': {
    'period': 1,
    'yellow': 'blink',
  },
  'Downloading': {
    'yellow': 'blink',
  },
  'AwaitingPlayback': {
    'period': 20,
    'green': 'blink',
  },
  'Playing': {
    'green': 'on',
  },
  'Polling': {
    'yellow': 'on',
  },
}

def update_leds(state, red, green, yellow):
  channels = {
    'red': red,
    'green': green,
    'yellow': yellow,
  }
  state_map = STATE_MAPS[state['state']]
  for channel_name in channels:
    channel_map = state_map.get(channel_name, 'off')
    channel = channels[channel_name]

    if channel_map == 'on':
      state[channel_name] = True
    elif channel_map == 'blink':
      if state['period_counter'] >= state_map.get('period', 1):
        state[channel_name] = False if state[channel_name] else True
        state['period_counter'] = 0
      state['period_counter'] += 1
    else:
      state[channel_name] = False

    GPIO.output(channel, state[channel_name])
