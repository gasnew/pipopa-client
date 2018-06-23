# Important imports
from client import *

# Cheery channels
BUTTON_PIN = 23

# Interesting inits
GPIO.setmode(GPIO.BCM) # make diagram life happy

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(YELLOW_PIN, GPIO.OUT)

# Impeccable initializations
pipopa = PiPoPa('garrett', 'garrett', 'jesse')
#pipopa = PiPoPa('jesse', 'jesse', 'garrett')
#pipopa = PiPoPa('test', 'test', 'test')
leds = LEDs(pipopa.get_led_state)

# Eventful events
GPIO.add_event_detect(BUTTON_PIN,
  GPIO.BOTH,
  callback=pipopa.do_thing,
  bouncetime=20)

try:
  # Luscious LEDs
  leds.start()

  # Preposterous PiPoPa
  pipopa.start()
finally:
  GPIO.cleanup()
