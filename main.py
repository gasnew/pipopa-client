# Important imports
from client import *

# Cheery channels
RED_PIN = 18
BUTTON_PIN = 23

# Interesting inits
GPIO.setmode(GPIO.BCM) # make diagram life happy

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Impeccable initializations
pipopa = PiPoPa()

# Eventful events
GPIO.add_event_detect(BUTTON_PIN,
  GPIO.BOTH,
  callback=pipopa.do_thing,
  bouncetime=20)

while True:
  time.sleep(5)
