import time
import board
import digitalio
import random

'''
x
'''
motor1Dir = digitalio.DigitalInOut(board.A7)
motor1Dir.direction = digitalio.Direction.OUTPUT

motor1Step= digitalio.DigitalInOut(board.A6)
motor1Step.direction = digitalio.Direction.OUTPUT
'''
y
'''
motor2Dir = digitalio.DigitalInOut(board.A3)
motor2Dir.direction = digitalio.Direction.OUTPUT

motor2Step= digitalio.DigitalInOut(board.A2)
motor2Step.direction = digitalio.Direction.OUTPUT

motor1Dir.value = False
motor2Dir.value = False

currentPosX = 0
currentPosY = 0

def step(mStep,mDir,direction,motorNum):
    global currentPosX
    global currentPosY
    if motorNum == 0:
        if direction == True:
            currentPosX = currentPosX + 1
        else:
            currentPosX = currentPosX - 1
    elif motorNum == 1:
        if direction == True:
            currentPosY = currentPosY + 1
        else:
            currentPosY = currentPosY - 1
    mDir.value = direction
    mStep.value = True
    time.sleep(0.001)
    mStep.value = False
    time.sleep(0.001)
    print(str(currentPosX )+ " : " + str(currentPosY))

xPos = [100, 500, 100]
yPos = [100, 500, 100]
posLength = 3
posIndex = 0
xReached = False
yReached = False
endReached = False

while True:
    while endReached == False:
        if posIndex == posLength - 1:
            endReached = True

        if currentPosX < xPos[posIndex]:
            step(motor1Step, motor1Dir, True, 0)
        elif currentPosX > xPos[posindex]:
            step(motor1Step, motor1Dir, False, 0)
        else:
            xReached = True

        if currentPosY < yPos[posIndex]:
            step(motor2Step, motor2Dir, True, 0)
        elif currentPosY > yPos[posindex]:
            step(motor2Step, motor2Dir, False, 0)
        else:
            yReached = True

        if xReached == True & yReached == True:
            posIndex = posIndex + 1