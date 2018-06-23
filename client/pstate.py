class PState:
  STATE_GRAPH = { 
    'Standby': {
      'waitingMessage': 'AwaitingPlayback',
      'down': 'Recording',
      'poll': 'Polling',
    },
    'Recording': {
      'up': 'Uploading',
    },
    'Uploading': {
      'done': 'Standby',
    },
    'Downloading': {
      'done': 'AwaitingPlayback',
    },
    'AwaitingPlayback': {
      'down': 'Playing',
      'poll': 'Polling',
    },
    'Playing': {
      'done': 'Standby',
      'more': 'AwaitingPlayback',
    },
    'Polling': {
      'newMessage': 'Downloading',
      'done': 'Standby',
      'waitingMessage': 'AwaitingPlayback',
    },
  }

  def __init__(self, state):
    self.state = state
    self.state_callbacks = {}

  def set_state_callback(self, state, callback):
    self.state_callbacks[state] = callback

  def follow_edge(self, action):
    print(' FOLLOW EDGE {}'.format(action))
    try:
      self.state = self.STATE_GRAPH[self.state][action]
      print(' [STATE] switching to state {}'.format(self.state))
      self.state_callbacks.get(self.state, lambda: None)()
    except Exception:
      if (action == 'error'):
        self.state = 'Standby'
        print(' [STATE] switching to state {}'.format(self.state))
        self.state_callbacks.get(self.state, lambda: None)()
      else:
        print(' [INFO] {} is not a valid action for state {}'.format(action, self.state))
