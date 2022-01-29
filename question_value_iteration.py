from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import time
import random


"""
    Function for printing an 2D array to terminal
"""
def Print2DArray(arr):
    for row in arr:
        print(row)


"""
    Function for reading grid information from a text file
    
    data_type int or float
"""
def ReadGridFromText(file_path, data_type=int):
    data = []
    try:
        with open(file_path, "r") as dosya:
            text = dosya.read().splitlines()
            rowCount, columnCount = map(int, text[0].split())
            for i in range(1, rowCount+1):
                data.append( list(map(data_type, text[i].split())) )
            
    except IOError as e:
        print("Unable to open file ", file_path, ",", e)
        exit(1)
    
    
    return data



"""
    Function for drawing the grid with its statae values
"""
def DrawStateImage(stateValues, occupancyMap, terminalStateMask, numRows, numCols):
    width = 500
    height = 500
    numRows = numRows
    numCols = numCols
    
    dWidth = int(width/numCols)
    dHeight = int(height/numRows)

    #  create empty image
    img = Image.new(mode="RGBA", size=(width, height), color=(255, 255, 255, 255))
    
    #  initialize drawer object
    draw = ImageDraw.Draw(img)

    y_start = 0
    y_end = height
    y_step = int(height / numRows)
    
    x_start = 0
    x_end = width
    x_step = int(width / numCols)


    #  draw horizontal lines
    for y in range(y_start, y_end, y_step):
        line = ((x_start, y), (x_end, y))
        draw.line(line, fill=(0, 0, 0, 255))
    
    #  draw vertical lines
    for x in range(x_start, x_end, x_step):
        line = ((x, y_start), (x, y_end))
        draw.line(line, fill=(0, 0, 0, 255))
    
    #  draw borders expilicity
    bottomLine = ((0, height-1), (width, height-1))
    draw.line(bottomLine, fill=(0, 0, 0, 255))
    rightLine = ((width-1, 0), (width-1, height-1))
    draw.line(rightLine, fill=(0, 0, 0, 255))
    
    
    #  used when drawing rectangles so rectangle does not overlap with border completely
    borderMarginX = 1
    borderMarginY = 1
    
    for rowIndex in range(numRows):
        for colIndex in range(numCols):
            topLeftX = (width/numCols) * colIndex
            topLeftY = (height/numRows) * rowIndex
            #print("({}, {})".format(topLeftX, topLeftY))
            centerX = topLeftX + dWidth/2
            centerY = topLeftY + dHeight/2
            botRightX = topLeftX + dWidth
            botRightY = topLeftY + dHeight
            
            
            #  check if cell is blocked
            if (occupancyMap[rowIndex][colIndex] != 0):
                #  draw a gray rectangle block
                draw.rectangle([topLeftX+borderMarginX, topLeftY+borderMarginY, botRightX-borderMarginX, botRightY-borderMarginY], fill=(127, 127, 127, 255))
            else:
                #  check if state is a terminal state
                if (terminalStateMask[rowIndex][colIndex] != 0):
                    #  terminal state
                    #check whether value of terminal state is positive or negative
                    if (stateValues[rowIndex][colIndex] > 0):
                        #  draw a green rectangle
                        #draw.rectangle([topLeftX+borderMarginX, topLeftY+borderMarginY, botRightX-borderMarginX, botRightY-borderMarginY], fill=(0, 200, 0, 255))
                        pass
                    elif (stateValues[rowIndex][colIndex] < 0):
                        #  draw a blue rectangle
                        #draw.rectangle([topLeftX+borderMarginX, topLeftY+borderMarginY, botRightX-borderMarginX, botRightY-borderMarginY], fill=(0, 0, 200, 255))
                        pass
                else:
                    #  not a terminal state
                    pass
                
                #  draw value of the state
                #draw.text((centerX, centerY), "{:.3f}".format(stateValues[rowIndex][colIndex]), font=ImageFont.truetype("Arial.ttf", 12), fill=(255, 0, 0, 255))
                draw.text((centerX, centerY), "{:.3f}".format(stateValues[rowIndex][colIndex]), font=ImageFont.truetype("LiberationSans-Regular.ttf", 12), fill=(255, 0, 0, 255))

  
    #img.save("q_values_100.png")
    img.show()
    
    return img
















"""
    All 2D grid arrays are row-major. For example:
        currentStateValues[i1][i2] gives you value of the cell at
        position row=i1, column=i2.
        In the given homework files, your grid has 3 rows and 4 columns.

    occupancyMap: 2D array, 1 if cell is occupied (blocked), and 0 if 
        cell is empty. Blocked means your agent can not go through that cell.
    
    currentStateValues: 2D array (of floats), 
        currentStateValues[row][column] corresponds to value of grid
        cell at (row, column).
    
    terminalStateMask: 2D array, 1 if cell is a terminal cell, 0 otherwise.
    
    stepCost: A penalty for each action your agent performs. This penalty
        is applied even if you end up in the same state (like when you 
        try to walk towards a wall or out of bounds).
    
    stepCostFactor: stepCost factor in the Bellman equation, see lecture
        slides for details.
"""

def GridValueIteration(occupancyMap, currentStateValues, terminalStateMask, stepCost=-0.04, stepCostFactor=1.0):
    #  read dimension information of our grid environment
    rowCount = len(occupancyMap)
    columnCount = len(occupancyMap[0])
    
    #  create an array of zeroes with the same size
    #you will fill this array with new values calculated in this function
    newStateValues = [ [0.0]*columnCount for i in range(rowCount) ]
    newStateValues[0][3] = 1.0
    newStateValues[1][3] = -1.0

    
    """
        YOUR CODE STARTS BELOW
    """
    directions = [(1,0), (-1,0), (0,-1), (0,1)]
    DOWN = directions[0]
    UP  = directions[1]
    LEFT = directions[2]
    RIGHT = directions[3]

    for i in range(rowCount):
        for j in range(columnCount):   
            if (i,j) == (0,3) or (i,j) == (1,3) or (i,j) == (1,1):
                continue 
            stepCost_temp = []
            for dir in directions:
                if dir == DOWN or dir == UP: 
                    dir_1 = LEFT
                    dir_2 = RIGHT
                if dir == LEFT or dir == RIGHT: 
                    dir_1 = UP
                    dir_2 = DOWN

                # Checks main direction that we want to go
                nextdir = (dir[0]+i, dir[1]+j)
                if nextdir == (1,1) or nextdir[0] < 0 or nextdir[1] < 0 or nextdir[0] > rowCount-1 or nextdir[1] > columnCount-1:
                    nextdir = (i,j)
                nextdir_value = currentStateValues[nextdir[0]][nextdir[1]]
                stepCost += 0.8 * nextdir_value * 1.0

                # Checks the first side position
                nextdir_1 = (dir_1[0] + i, dir_1[1] + j)
                if nextdir_1 == (1,1) or nextdir_1[0] < 0 or nextdir_1[1] < 0 or nextdir_1[0] > rowCount-1 or nextdir_1[1] > columnCount-1:
                    nextdir_1 = (i,j)
                nextdir_1_value = currentStateValues[nextdir_1[0]][nextdir_1[1]]
                stepCost += 0.1 * nextdir_1_value * 1.0

                # Checks the second side position
                nextdir_2 = (dir_2[0] + i, dir_2[1] + j)
                if nextdir_2 == (1,1) or nextdir_2[0] < 0 or nextdir_2[1] < 0 or nextdir_2[0] > rowCount-1 or nextdir_2[1] > columnCount-1:
                    nextdir_2 = (i,j)
                nextdir_2_value = currentStateValues[nextdir_2[0]][nextdir_2[1]]
                stepCost += 0.1 * nextdir_2_value * 1.0
                
                # Takes the maximum of stepCost for the state
                stepCost_temp.append(stepCost)
                newStateValues[i][j] = max(stepCost_temp)
                stepCost = -0.04

    """
        YOUR CODE ENDS HERE
    """
    
    return newStateValues

        
        





















#  read map info from file
occupancyMap = ReadGridFromText("map.txt", int)
print("--- 2D Map Array ---")
Print2DArray(occupancyMap)

#  read initial state values from file
initialStateValues = ReadGridFromText("initial_state_values.txt", float)    
print("--- Initial State Values Array ---")
Print2DArray(initialStateValues)

#  read information of which states are terminal state 
terminalStateMask = ReadGridFromText("terminal_state_mask.txt", int)
print("--- Terminal State Mask ---")
Print2DArray(terminalStateMask)

#  get grid dimension info
numRows = len(occupancyMap)
numCols = len(occupancyMap[0])  #  assuming all rows have same number of columns


#  create a new variable for current state values
stateValues = initialStateValues


#  perform value iteration for 200 iterations
for i in range(200):
    stateValues = GridValueIteration(occupancyMap, stateValues, terminalStateMask, stepCost=-0.04, stepCostFactor=1.0)

#  draw final values of each state
DrawStateImage(stateValues, occupancyMap, terminalStateMask, numRows=numRows, numCols=numCols)
