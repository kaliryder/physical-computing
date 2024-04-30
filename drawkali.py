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
xPos = [-407, -407, -814, -814, ,-1221, -1628, -1221 -1628, -1221, -814, -814, -407, -1628, -2442, -2849, -3663, -3256, -2849, -2442, -2035, -1628, -2442, -2849, -2645, -2442, -3663, -3663, -4070, -4070, -4884, -4884, -3663, -4884, -4884, -5291, -5291, -4884, 0]
yPos = [3000, 15000, 15000, 9000, 15000, 15000, 9000, 3000, 3000, 9000, 3000, 3000, 3000, 15000, 15000, 3000, 3000, 7500, 7500, 3000, 3000, 9000, 9000, 12000, 9000, 3000, 15000, 15000, 4500, 4500, 3000, 3000, 3000, 15000, 15000, 3000, 3000, 0]
posLength = 38
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