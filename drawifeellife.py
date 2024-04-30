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
xPos = [0, -407, -407, 0, 0, 
-1628, -1628, -1221, -1628, -1628, -1221, -1221, -814, -814, 
-2849, -2849, -2442, -2849, -2849, -2442, -2849, -2849, -2035, -2035,
-4070, -4070, -4070, -3663, -4070, -4070, -3663, -4070, -4070, -3256, -3256,
-4884, -4884, -5291, -5291, -4477, -4477,
-407, -407,
-1628, -1628, -814, -814, -407,
-2442, -2442, -2035, -2035,
-4070, -4070, -3256, -3256, -4070, -4070, -3256, -3256, -2849, -2849,
-5291, -5291, -4884, -4884, -5291, -5291, -4884, -4884, -5291, -5291, -4477, -4477,
0, 0]

yPos = [16500, 16500, 12000, 12000, 16500,
16500, 15000, 15000, 15000, 13500, 13500, 12000, 12000, 16500,
16500, 15000, 15000, 15000, 13500, 13500, 13500, 12000, 12000, 16500,
16500, 15000, 15000, 15000, 15000, 13500, 13500, 13500, 12000, 12000, 16500,
16500, 13500, 13500, 12000, 12000, 16500,
16500, 1500,
1500, 3000, 3000, 10500, 10500,
10500, 1500, 1500, 10500,
10500, 9000, 9000, 7500, 7500, 6000, 6000, 1500, 1500, 10500,
10500, 9000, 9000, 7500, 7500, 6000, 6000, 4500, 4500, 1500, 1500, 10500,
10500, 0]

posLength = 76
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
'''
I
0, 16500
-407, 16500
-407, 12000
0, 12000
0, 16500
F 
-1628, 16500
-1628, 15000
-1221, 15000
-1628, 15000
-1628, 13500
-1221, 13500
-1221, 12000
-814, 12000
-814, 16500
E 
-2849, 16500
-2849, 15000
-2442, 15000
-2849, 15000
-2849, 13500
-2442, 13500
-2849, 13500
-2849, 12000
-2035, 12000
-2035, 16500
E 
-4070, 16500
-4070, 15000
-4070, 15000
-3663, 15000
-4070, 15000
-4070, 13500
-3663, 13500
-4070, 13500
-4070, 12000
-3256, 12000
-3256, 16500
L 
-4884, 16500
-4884, 13500
-5291, 13500
-5291, 12000
-4477, 12000
-4477, 16500
Move Left
-407, 16500
Move Down 
-407, 1500
L 
-1628, 1500
-1628, 3000
-814, 3000
-814, 10500
-407, 10500
I 
-2442, 10500
-2442, 1500
-2035, 1500
-2035, 10500
F 
-4070, 10500
-4070, 9000
-3256, 9000
-3256, 7500
-4070, 7500
-4070, 6000
-3256, 6000
-3256, 1500
-2849, 1500
-2849, 10500
E 
-5291, 10500
-5291, 9000
-4884, 9000
-4884, 7500
-5291, 7500
-5291, 6000
-4884, 6000
-4884, 4500
-5291, 4500
-5291, 1500
-4477, 1500
-4477, 10500
Move Left 
0, 10500
Move Down 
0, 0
'''