class PState:
  STATE_GRAPH = { 
    'Standby': {
      'down': 'Recording',
      'messageReady': 'Pending',
    },
    'Recording': {
      #'up': 'Uploading',
      'done': 'Uploading',
    },
    'Uploading': {
      'done': 'Standby',
    },
    'Pending': {
      'down': 'Playing',
    },
    'Playing': {
      'done': 'Standby',
    },
  }

  def __init__(self, state):
    self.state = state
    self.state_callbacks = {}

  def set_state_callback(self, state, callback):
    self.state_callbacks[state] = callback

  def follow_edge(self, action):
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
