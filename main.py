# Important imports
from client import *

# Cheery channels
RED_PIN = 18
BUTTON_PIN = 23

# Interesting inits
GPIO.setmode(GPIO.BCM) # make diagram life happy

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Impeccable initializations
#pipopa = PiPoPa('garrett', 'garrett', 'jesse')
pipopa = PiPoPa('jesse', 'jesse', 'garrett')

# Eventful events
GPIO.add_event_detect(BUTTON_PIN,
  GPIO.BOTH,
  callback=pipopa.do_thing,
  bouncetime=20)

while True:
  pipopa.p_state.follow_edge('poll')
  time.sleep(3)
