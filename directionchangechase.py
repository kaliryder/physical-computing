import time
import board
import digitalio
import neopixel
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.chase import Chase

# Colors
YELLOW = (255, 255, 0)
NEON_BLUE = (31, 81, 255)

# LED setup
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# Button setup
switch = digitalio.DigitalInOut(board.BUTTON_A)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.DOWN

# Mode setup
wasPressed = False
mode = 0

# Pixels setup
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1, auto_write=False)

# Animation setup
pulse = Pulse(pixels, speed=0.1, color=YELLOW, period=3)
chase = Chase(pixels, speed=0.08, color=YELLOW, size=3, spacing=6)

# Color fading function
def fade_color(color1, color2, mix):
    return tuple(int(c1 * (1 - mix) + c2 * mix) for c1, c2 in zip(color1, color2))

# Fading and direction change variables
fade_duration = 2.0  # Duration of the fade in seconds
fade_start = time.monotonic()
direction_change_interval = 2.0  # Direction change interval in seconds
last_direction_change = time.monotonic()

# Initial direction
chase_direction = True

# Mode switching
while True:
    print("current mode: " + str(mode))
    if switch.value:
        wasPressed = True
    else:
        if wasPressed:
            wasPressed = False
            mode += 1
            fade_start = time.monotonic()  # Restart fade timing
            last_direction_change = time.monotonic()  # Restart direction change timing

    if mode == 0:
        led.value = False
        pixels.fill((0, 0, 0))
        pixels.show()
    elif mode == 1:
        pulse.animate()
        pixels.show()
    elif mode == 2:
        # Calculate the mix ratio for fading
        time_passed = (time.monotonic() - fade_start) % fade_duration
        mix_ratio = abs(1 - 2 * (time_passed / fade_duration))

        # Calculate the current color
        current_color = fade_color(YELLOW, NEON_BLUE, mix_ratio)
        chase.color = current_color

        # Check for direction change
        if time.monotonic() - last_direction_change > direction_change_interval:
            chase_direction = not chase_direction
            last_direction_change = time.monotonic()

        # Set direction
        chase.reverse = chase_direction

        chase.animate()
        pixels.show()
    else:
        mode = 0

    time.sleep(0.01)  # debounce delay