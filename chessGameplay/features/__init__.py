"""
In this file, we import all the useful functions for chess.
"""

from chessGameplay.features.primary import *
from chessGameplay.features.gui import *
from chessGameplay.features.utitlities import *
from chessGameplay.features.ai import *

# This converts a string of moves nto the notation used by the game.
def convertMoves(moveList):
    side, chessBoard, gameFlags = initializeChessBoard()

    for start, end, promotion in map(convertFromAlgebraic, moveList):
        side, chessBoard, gameFlags = performMove(side, chessBoard, start, end, gameFlags, promotion)

    return side, chessBoard, gameFlags

# getPromotion() first checks whether a pawn has reached promotion state
# Then, if the game is multiplayer, getPromotion() returns getChoice()
def getPromotion(window, side, board, startPos, endPos, single=False):
    if getPieceType(side, board, startPos) == "p":
        if (side == 0 and endPos[1] == 1) or (side == 1 and endPos[1] == 8):
            if single:
                return "q"
            else:
                return getUserSelection(window, side)

def showTimer(window, side, mode, timer, startTime, timeDelta):
    if timer is None:
        pygame.display.update()
        return None

    updatedTimer = list(timer)
    elapsedTime = getCurrentTime() - (startTime + timeDelta)
    if mode == -1:
        updatedTimer[side] += elapsedTime
        if updatedTimer[side] >= 3600000:
            updatedTimer[side] = 3599000

    else:
        updatedTimer[side] -= elapsedTime
        if updatedTimer[side] < 0:
            displayTimeOut(window, side)
            return None

    displayClock(window, updatedTimer)
    return updatedTimer

# This is a GUI function that draws squares marking the legal moves of a piece.
def displayAvailableMoves(window, side, board, position, flags, flipBoard):
    piece = position + [getPieceType(side, board, position)]
    for i in legalMoves(side, board, piece, flags):
        x = 470 - i[0] * 50 if flipBoard else i[0] * 50 + 20
        y = 470 - i[1] * 50 if flipBoard else i[1] * 50 + 20
        pygame.draw.rect(window, (0, 255, 0), (x, y, 10, 10))

# This function makes a gentle animation of a piece that is getting moved.
def animateMove(window, side, board, startPos, endPos, resources, player=None):
    sound.play_drag(resources)
    if player is None:
        flip = side and resources["flip"]
    else:
        flip = player and resources["flip"]

    chessPiece = CHESS.PIECES[side][getPieceType(side, board, startPos)]
    x1, y1 = startPos[0] * 50, startPos[1] * 50
    x2, y2 = endPos[0] * 50, endPos[1] * 50
    if flip:
        x1, y1 = 450 - x1, 450 - y1
        x2, y2 = 450 - x2, 450 - y2

    stepX = (x2 - x1) / 50
    stepY = (y2 - y1) / 50

    color = (180, 100, 30) if (startPos[0] + startPos[1]) % 2 else (220, 240, 240)

    clock = pygame.time.Clock()
    for i in range(51):
        clock.tick_busy_loop(100)
        renderBoard(window)
        placePieces(window, board, flip)

        pygame.draw.rect(window, color, (x1, y1, 50, 50))
        window.blit(chessPiece, (x1 + (i * stepX), y1 + (i * stepY)))
        pygame.display.update()
    sound.play_move(resources)

# This is a compilation of all gui functions. This handles the display of the
# screen when chess gameplay takes place. 
def displayGameScreen(window, activeSide, boardState, gameFlags, selectedPos, resources, player=None, single=False):
    isMultiplayer = False
    if player is None:
        isMultiplayer = True
        player = activeSide

    boardFlipped = resources["flip"] and player

    renderBoard(window)
    window.blit(BACK, (460, 0))

    if not isMultiplayer:
        window.blit(CHESS.TURN[int(activeSide == player)], (10, 460))
    
    if not single:
        if resources["enableUndo"]:
            window.blit(CHESS.UNDO, (10, 12))
        window.blit(CHESS.SAVE, (350, 462))

    if hasGameEnded(activeSide, boardState, gameFlags):
        if isInCheck(activeSide, boardState):
            window.blit(CHESS.CHECKMATE, (100, 12))
            window.blit(CHESS.LOST, (320, 12))
            window.blit(CHESS.PIECES[activeSide]["k"], (270, 0))
        else:
            window.blit(CHESS.STALEMATE, (160, 12))
    else:
        if single:
            window.blit(CHESS.DRAW, (10, 12))
            window.blit(CHESS.RESIGN, (400, 462))

        if isInCheck(activeSide, boardState):
            window.blit(CHESS.CHECK, (200, 12))

        if isOccupied(activeSide, boardState, selectedPos) and activeSide == player:
            x = (9 - selectedPos[0]) * 50 if boardFlipped else selectedPos[0] * 50
            y = (9 - selectedPos[1]) * 50 if boardFlipped else selectedPos[1] * 50
            pygame.draw.rect(window, (255, 255, 0), (x, y, 50, 50))

    placePieces(window, boardState, boardFlipped)
    if resources["displayMoves"] and activeSide == player:
        displayAvailableMoves(window, activeSide, boardState, selectedPos, gameFlags, boardFlipped)

    if not isMultiplayer:
        pygame.display.update()

