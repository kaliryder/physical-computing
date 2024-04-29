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
xPos = [500, 100, 500]
yPos = [500, 100, 500]
posLength = 3
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
            step(motor2Step, motor2Dir, direction, 2)
            print(f"Stepping X to {'increase' if direction else 'decrease'}: {currentPosX}")
        if not yReached:
            direction = (currentPosY < yPos[posIndex])
            step(motor1Step, motor1Dir, direction, 1)
            print(f"Stepping Y to {'increase' if direction else 'decrease'}: {currentPosY}")

        # Check if both have reached after stepping
        if currentPosX == xPos[posIndex] and currentPosY == yPos[posIndex]:
            if posIndex < posLength - 1:
                posIndex += 1
                xReached, yReached = False, False  # Reset for the next position
                print(f"Target reached. Moving to new target: X={xPos[posIndex]}, Y={yPos[posIndex]}")
            else:
                print("Final position reached.")