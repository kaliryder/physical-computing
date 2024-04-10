import time
import board
import digitalio
import random

class A4988:
    def __init__(self, DIR, STEP):
        """This class represents an A4988 stepper motor driver. It uses two output pins
        for direction and step control signals. STARTS TOP LEFT"""

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

# Function to move to an absolute position
def move_to_position(current_pos, target_pos, speed):
    x_steps = target_pos[0] - current_pos[0]
    y_steps = target_pos[1] - current_pos[1]
    
    # Calculate the total steps needed
    total_steps = max(abs(x_steps), abs(y_steps))
    
    # Calculate the step increments for each axis
    x_step_inc = x_steps / total_steps
    y_step_inc = y_steps / total_steps
    
    # Perform the movement
    for _ in range(total_steps):
        if abs(x_step_inc) > 0:
            stepper_x.step(x_step_inc > 0)
        if abs(y_step_inc) > 0:
            stepper_y.step(y_step_inc > 0)
        time.sleep(1.0 / speed)  # This sleep determines the speed of the stepper
    
    return target_pos

# Generate random points
def generate_random_points(num_points, x_range, y_range):
    return [(random.randint(0, x_range), random.randint(0, y_range)) for _ in range(num_points)]

# Speed and acceleration configuration (may need to adjust based on your system)
speed = 800  # Speed for individual motor steps
# Note: Acceleration is not used in this synchronized stepping function

# Define the grid range
x_range = 4000  # Maximum steps to the right
y_range = 4000  # Maximum steps down from the top

# Starting position at top left corner
current_position = (0, y_range)

# Generate 10 random points within the grid
points = generate_random_points(10, x_range, y_range)

# Move the pencil through each point
for point in points:
    print(f"Moving to point {point}")
    current_position = move_to_position(current_position, point, speed)
    time.sleep(1)  # Pause at the point

# Return to starting position at the top left corner
print("Returning to starting position (0, 8000)")
move_to_position(current_position, (0, y_range), speed)

print("Sequence complete.")