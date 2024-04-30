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
        mDir.value = direction
        mStep.value = True
        time.sleep(0.000001)
        mStep.value = False
        time.sleep(0.000001)
        print(str(currentPosX )+ " : " + str(currentPosY))
    elif motorNum == 2:
        if direction == True:
            currentPosX = currentPosX + 1
        else:
            currentPosX = currentPosX - 1
        mDir.value = direction
        mStep.value = True
        time.sleep(0.000001)
        mStep.value = False
        time.sleep(0.000001)
        print(str(currentPosX )+ " : " + str(currentPosY))

# Step info setup
xPos = [-1221, -2849, -4477, -2849, -1221, -4477, -2849, 0]
yPos = [3000, 15000, 3000, 3000, 15000, 15000, 3000, 0]
posLength = 8
posIndex = 0
xReached = False
yReached = False
endReached = False

while True:
    while not endReached:
        if posIndex >= posLength:
            endReached = True
            print("Sequence completed.")
            break

        # Determine if the target is reached for both axes
        xReached = (currentPosX == xPos[posIndex])
        yReached = (currentPosY == yPos[posIndex])

        if not xReached:
            direction = (currentPosX < xPos[posIndex])
            time.sleep(0.000001)
            step(motor2Step, motor2Dir, direction, 2)
            time.sleep(0.000001)
            print(f"Stepping X to {'increase' if direction else 'decrease'}: {currentPosX}")
        if not yReached:
            direction = (currentPosY < yPos[posIndex])
            time.sleep(0.000001)
            step(motor1Step, motor1Dir, direction, 1)
            time.sleep(0.000001)
            print(f"Stepping Y to {'increase' if direction else 'decrease'}: {currentPosY}")

        # Check if both have reached after stepping
        if currentPosX == xPos[posIndex] and (currentPosY == yPos[posIndex]):
            posIndex += 1
            xReached, yReached = False, False  # Reset for the next position
            print(f"Target reached. Moving to new target: X={xPos[posIndex]}, Y={yPos[posIndex]}")