import time
import board
import digitalio

# Y setup
motor1Dir = digitalio.DigitalInOut(board.A7)
motor1Dir.direction = digitalio.Direction.OUTPUT

motor1Step= digitalio.DigitalInOut(board.A6)
motor1Step.direction = digitalio.Direction.OUTPUT

# X setup
motor2Dir = digitalio.DigitalInOut(board.A3)
motor2Dir.direction = digitalio.Direction.OUTPUT

motor2Step= digitalio.DigitalInOut(board.A2)
motor2Step.direction = digitalio.Direction.OUTPUT

# Initialize
motor1Dir.value = False
motor2Dir.value = False

currentPosX = 0
currentPosY = 0

# Step function setup
def step(mStep,mDir,direction,motorNum):
    global currentPosX
    global currentPosY
    if motorNum == 1:
        if direction == True:
            currentPosY = currentPosY + 1
        else:
            currentPosY = currentPosY - 1
    elif motorNum == 2:
        if direction == True:
            currentPosX = currentPosX + 1
        else:
            currentPosX = currentPosX - 1
    mDir.value = direction
    mStep.value = True
    time.sleep(0.001)
    mStep.value = False
    time.sleep(0.001)
    print(str(currentPosX )+ " : " + str(currentPosY))

# Step info setup
xPos = [1000, 3000, 500]
yPos = [1000, 3000, 500]
posLength = 3
posIndex = 0
xReached = False
yReached = False
endReached = False
steps = 0

while True:
    step(motor1Step, motor1Dir, False, 1)
    steps += 1
    print("steps: " + str(steps))
