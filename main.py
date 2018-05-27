# Important imports
from client import *

# Cheery channels
RED_PIN = 18
GREEN_PIN = 15
YELLOW_PIN = 14
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

# Eventful events
GPIO.add_event_detect(BUTTON_PIN,
  GPIO.BOTH,
  callback=pipopa.do_thing,
  bouncetime=20)

try:
  POLL_PERIOD = 3
  BLINK_PERIOD = 0.05
  poll_timer = 0
  while True:
    # Luscious LEDs
    update_leds(
      state = pipopa.get_led_state(),
      red = RED_PIN,
      green = GREEN_PIN,
      yellow = YELLOW_PIN,
    )

    # Putrid polling
    if poll_timer >= POLL_PERIOD:
      pipopa.p_state.follow_edge('poll')
      poll_timer = 0

    # Timid timing
    poll_timer += BLINK_PERIOD
    time.sleep(BLINK_PERIOD)
finally:
  GPIO.cleanup()
