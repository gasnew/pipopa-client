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
leds = LEDs(pipopa.get_led_state)

# Eventful events
GPIO.add_event_detect(BUTTON_PIN,
  GPIO.BOTH,
  callback=pipopa.do_thing,
  bouncetime=20)

try:
  # Luscious LEDs
  leds.start()

  POLL_PERIOD = 3
  while True:
    # Putrid polling
    pipopa.p_state.follow_edge('poll')

    # Timid timing
    time.sleep(POLL_PERIOD)
finally:
  GPIO.cleanup()
