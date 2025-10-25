import math

shortWallWidth = 400
shortWallHeight = 220

longWallWidth = 500
longWallHeight = 240


claddingHeightStr = input("What height are the boards? (mm) ")
claddingHeightInt = (int(claddingHeightStr) / 1000) # we want meters

claddingLengthStr = input("What length are the boards? (cm) ")
claddingLengthInt = (int(claddingLengthStr) / 100) # we want meters

costStr = input("What is the cost per piece? ")
costInt = int(costStr)

print()

def dothething (width, height):
    # Get the square meters
    sqmtr = ((height / 100) * (width / 100))
    print ("The wall is ", sqmtr, "m²")

    # Calculate the linear meters
    linearMeters = (sqmtr /  claddingHeightInt)
    #print (linearMeters , " linear meters")

    # How many boards do we need?
    boardCount = ((linearMeters / claddingLengthInt) * 2)
    return (boardCount)
    
boardCount1 = dothething(shortWallWidth, shortWallHeight)
print ("boards required for the short walls:", boardCount1)
print()

boardCount2 = dothething(longWallWidth, longWallHeight)
print ("boards required for the long walls:", boardCount2)
print()

totalBoardCount = math.ceil(boardCount1 + boardCount2)
print ("You will need", totalBoardCount, "pieces of cladding")
print ("Total cost:", (costInt * totalBoardCount))
