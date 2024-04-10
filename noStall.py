import time
import board
import digitalio

class A4988:
    def __init__(self, DIR, STEP):
        """This class represents an A4988 stepper motor driver. It uses two output pins
        for direction and step control signals."""

        self._dir = digitalio.DigitalInOut(DIR)
        self._step = digitalio.DigitalInOut(STEP)
        self._dir.direction = digitalio.Direction.OUTPUT
        self._step.direction = digitalio.Direction.OUTPUT

        self._dir.value = False
        self._step.value = False

    def step(self, forward=True):
        """Emit one step pulse, with an optional direction flag."""
        self._dir.value = forward
        self._step.value = True
        time.sleep(0.001)  # Sleep for 1 millisecond for the pulse
        self._step.value = False

    def move_sync(self, steps, speed=1000.0, acceleration=50):
        """Move the stepper motor the signed number of steps forward or backward at the
        speed specified in steps per second, with acceleration."""

        # Determine the initial speed (start slow)
        current_speed = acceleration

        # Accelerate
        while current_speed < speed:
            self.step(steps > 0)
            time.sleep(1.0 / current_speed)
            current_speed += acceleration

        # Move at constant speed
        time_per_step = 1.0 / speed
        for _ in range(abs(steps)):
            self.step(steps > 0)
            time.sleep(time_per_step)

        # Decelerate (optional, you can add a decelerate function similarly to accelerate)

    def deinit(self):
        """Manage resource release as part of object lifecycle."""
        self._dir.deinit()
        self._step.deinit()
        self._dir = None
        self._step = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Automatically deinitializes the hardware when exiting a context.
        self.deinit()

# Initialize two stepper motors
stepper_x = A4988(DIR=board.A7, STEP=board.A6)  # X-axis motor
stepper_y = A4988(DIR=board.A3, STEP=board.A2)  # Y-axis motor

print("Starting stepper motor test.")

# Speed and acceleration configuration
speed = 1000
acceleration = 90  # steps/sec^2

try:
    while True:
        # Move X-axis motor
        print(f"Moving X-axis motor at {speed} steps/sec with acceleration.")
        stepper_x.move_sync(1000, speed, acceleration)
        time.sleep(1.0)
        stepper_x.move_sync(-1000, speed, acceleration)
        time.sleep(1.0)

        # Move Y-axis motor
        print(f"Moving Y-axis motor at {speed} steps/sec with acceleration.")
        stepper_y.move_sync(1000, speed, acceleration)
        time.sleep(1.0)
        stepper_y.move_sync(-1000, speed, acceleration)
        time.sleep(1.0)

except KeyboardInterrupt:
    # If the user hits Ctrl-C, exit the loop and deinitialize.
    print("Exiting program.")

finally:
    # Clean up
    stepper_x.deinit()
    stepper_y.deinit()
    print("Steppers deinitialized.")