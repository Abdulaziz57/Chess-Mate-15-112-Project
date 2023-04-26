'''
In this file, we manage the chess gameplay for multiplayer section.
'''
import time
from chessGameplay.features import *

# main function for the chess game
def primaryFunction(gameWindow, gameMode, timer, gameLoad, moveString=""):
    initializeGame(gameWindow, gameLoad)
    
    moves = moveString.split()

    side, board, flags = convertMoves(moves)
    clock = pygame.time.Clock()
    sel = prevsel = [0, 0]

    if timer is not None:
        timer = list(timer)
    while True:
        looptime = getCurrentTime()
        clock.tick(25)
        
        timedelta = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                starttime = getCurrentTime()
                if confirmQuit(gameWindow):
                    return 0
                timedelta += getCurrentTime() - starttime

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 460 < x < 500 and 0 < y < 50:
                    starttime = getCurrentTime()
                    if confirmQuit(gameWindow):
                        return 1
                    timedelta += getCurrentTime() - starttime

                if 50 < x < 450 and 50 < y < 450:
                    x, y = x // 50, y // 50
                    if gameLoad["flip"] and side:
                        x, y = 9 - x, 9 - y

                    if isOccupied(side, board, [x, y]):
                        sound.play_click(gameLoad)

                    prevsel = sel
                    sel = [x, y]

                    if isMoveValid(side, board, flags, prevsel, sel):
                        starttime = getCurrentTime()
                        promote = getPromotion(gameWindow, side, board, prevsel, sel)
                        animateMove(gameWindow, side, board, prevsel, sel, gameLoad)
                        
                        timedelta += getCurrentTime() - starttime
                        timer = refreshGameTimer(side, gameMode, timer)

                        side, board, flags = performMove(
                            side, board, prevsel, sel, flags, promote)
                        moves.append(convertToAlgebraic(prevsel, sel, promote))

                else:
                    sel = [0, 0]
                    if 350 < x < 500 and 460 < y < 490:
                        starttime = getCurrentTime()
                        if confirmQuit(gameWindow, saveGame(moves, mode=gameMode, timer=timer)):
                            return 1
                        timedelta += getCurrentTime() - starttime
                        
                    elif 0 < x < 80 and 0 < y < 50 and gameLoad["enableUndo"]:
                        moves = revertMoves(moves)
                        side, board, flags = convertMoves(moves)

        displayGameScreen(gameWindow, side, board, flags, sel, gameLoad)
        timer = showTimer(gameWindow, side, gameMode, timer, looptime, timedelta)
