"""
In this file, we define a few other non-gui My-PyChess helper functions.
"""

from datetime import datetime
import os
import time

letterList = ["", "a", "b", "c", "d", "e", "f", "g", "h"]

# Convert algebraic notation back to game data format
def convertToAlgebraic(fromPos, toPos, promotion=None):
    algebraic = letterList[fromPos[0]] + str(9 - fromPos[1]) + letterList[toPos[0]] + str(9 - toPos[1])
    if promotion is not None:
        return algebraic + promotion
    return algebraic

# decode does the opposite of encode()
def convertFromAlgebraic(algebraicData):
    # Check for valid algebraic notation
    if not all(char in letterList or char.isdigit() for char in algebraicData):
        return None

    result = [[letterList.index(algebraicData[0]), 9 - int(algebraicData[1])],
              [letterList.index(algebraicData[2]), 9 - int(algebraicData[3])],]

    if len(algebraicData) == 5:
        result.append(algebraicData[4])
    else:
        result.append(None)
    return result
    
# Initialize the chess board variables
def initializeChessBoard():
    color = False
    chessBoard = [
    [
    [1, 7, "p"], [2, 7, "p"], [3, 7, "p"], [4, 7, "p"],
    [5, 7, "p"], [6, 7, "p"], [7, 7, "p"], [8, 7, "p"],
    [1, 8, "r"], [2, 8, "n"], [3, 8, "b"], [4, 8, "q"],
    [5, 8, "k"], [6, 8, "b"], [7, 8, "n"], [8, 8, "r"],
    ], [
    [1, 2, "p"], [2, 2, "p"], [3, 2, "p"], [4, 2, "p"],
    [5, 2, "p"], [6, 2, "p"], [7, 2, "p"], [8, 2, "p"],
    [1, 1, "r"], [2, 1, "n"], [3, 1, "b"], [4, 1, "q"],
    [5, 1, "k"], [6, 1, "b"], [7, 1, "n"], [8, 1, "r"],
    ]
    ]
    statusFlags = [[True for _ in range(4)], None]
    return color, chessBoard, statusFlags

#Undo the specified number of moves
def revertMoves(moveList, moveCount=1):
    if len(moveList) in range(moveCount):
        return moveList
    else:
        return moveList[:-moveCount]

# Get time in rounded milliseconds
def getCurrentTime():
    return round(time.perf_counter() * 1000)

# Update the game-timer after each move
def refreshGameTimer(color, mode, currentTimer):
    if currentTimer is None:
        return None
    
    updatedTimer = list(currentTimer)
    if mode != -1:
        updatedTimer[color] += (mode * 1000)
    return updatedTimer

def saveGame(moves, gametype="multi", player=0, level=0,
             mode=None, timer=None, cnt=0):
    if cnt >= 20:
        return -1

    name = os.path.join("res", "savedGames", "game" + str(cnt) + ".txt")
    if os.path.isfile(name):
        return saveGame(moves, gametype, player, level, mode, timer, cnt + 1)
    
    else:
        if gametype == "single":
            gametype += " " + str(player)

        dt = datetime.now()
        date = "/".join(map(str, [dt.day, dt.month, dt.year]))
        time = ":".join(map(str, [dt.hour, dt.minute, dt.second]))
        datentime = " ".join([date, time])

        movestr = " ".join(moves)
        
        temp = []
        if mode is not None:
            temp.append(str(mode))
        
            if timer is not None:
                temp.extend(map(str, timer))
            
        temp = " ".join(temp)
        text = "\n".join([gametype, datentime, movestr, temp])
              
        with open(name, "w") as file:
            file.write(text)
        return cnt