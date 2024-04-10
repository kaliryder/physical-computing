import time
import board
import digitalio

class A4988:
    def __init__(self, DIR, STEP):
        """This class represents an A4988 stepper motor driver. It uses two output pins
        for direction and step control signals."""

        self._dir  = digitalio.DigitalInOut(DIR)
        self._step = digitalio.DigitalInOut(STEP)

        self._dir.direction  = digitalio.Direction.OUTPUT
        self._step.direction = digitalio.Direction.OUTPUT

        self._dir.value = False
        self._step.value = False

    def step(self, forward=True):
        """Emit one step pulse, with an optional direction flag."""
        self._dir.value = forward

        # Create a short pulse on the step pin. Note that CircuitPython is slow
        # enough that normal execution delay is sufficient without actually
        # sleeping.
        self._step.value = True
        # time.sleep(1e-6)
        self._step.value = False

    def move_sync(self, steps, speed=1000.0):
        """Move the stepper motor the signed number of steps forward or backward at the
        speed specified in steps per second. N.B. this function will not return
        until the move is done, so it is not compatible with asynchronous event
        loops.
        """

        self._dir.value = (steps >= 0)
        time_per_step = 1.0 / speed
        for count in range(abs(steps)):
            self._step.value = True
            # time.sleep(1e-6)
            self._step.value = False
            time.sleep(time_per_step)

    def deinit(self):
        """Manage resource release as part of object lifecycle."""
        self._dir.deinit()
        self._step.deinit()
        self._dir  = None
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

speed = 700

while True:
    # Move X-axis motor
    print(f"Moving X-axis motor at {speed} steps/sec.")
    stepper_x.move_sync(2000, speed)
    time.sleep(1.0)
    stepper_x.move_sync(-2000, speed)
    time.sleep(1.0)
    # Move Y-axis motor
    print(f"Moving Y-axis motor at {speed} steps/sec.")
    stepper_y.move_sync(-7000, speed)
    time.sleep(1.0)
    stepper_y.move_sync(7000, speed)
    time.sleep(1.0)