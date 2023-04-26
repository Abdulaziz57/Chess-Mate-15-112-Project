'''
In this file, we manage the chess gameplay for singleplayer section

'''

from chessGameplay.features import *

# Execute main code for single-player chess game
def primaryFunction(gameWindow, currentPlayer, gameLoad, moveString=""):
    initializeGame(gameWindow, gameLoad)

    moves = moveString.split()
    side, board, flags = convertMoves(moves)

    clock = pygame.time.Clock()
    sel = prevsel = [0, 0]
    while True:
        clock.tick(25)
        end = hasGameEnded(side, board, flags)
        for event in pygame.event.get():
            if event.type == pygame.QUIT and confirmQuit(gameWindow):
                return 0
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 460 < x < 500 and 0 < y < 50 and confirmQuit(gameWindow):
                    return 1

                if 50 < x < 450 and 50 < y < 450:
                    x, y = x // 50, y // 50
                    if gameLoad["flip"] and currentPlayer:
                        x, y = 9 - x, 9 - y

                    if isOccupied(side, board, [x, y]):
                        sound.play_click(gameLoad)

                    prevsel = sel
                    sel = [x, y]

                    if (side == currentPlayer
                        and isMoveValid(side, board, flags, prevsel, sel)):
                        promote = getPromotion(gameWindow, side, board, prevsel, sel)
                        animateMove(gameWindow, side, board, prevsel, sel, gameLoad, currentPlayer)

                        side, board, flags = performMove(
                            side, board, prevsel, sel, flags, promote)
                        moves.append(convertToAlgebraic(prevsel, sel, promote))

                elif side == currentPlayer or end:
                    sel = [0, 0]
                    if 350 < x < 500 and 460 < y < 490:
                        if confirmQuit(gameWindow, saveGame(moves, "single", currentPlayer)):
                            return 1
                    elif 0 < x < 80 and 0 < y < 50 and gameLoad["enableUndo"]:
                        moves = revertMoves(moves, 2) if side == currentPlayer else revertMoves(moves)
                        side, board, flags = convertMoves(moves)

        displayGameScreen(gameWindow, side, board, flags, sel, gameLoad, currentPlayer)
        
        end = hasGameEnded(side, board, flags)
        if side != currentPlayer and not end:
            fro, to = miniMaxSearch(side, board, flags)
            animateMove(gameWindow, side, board, fro, to, gameLoad, currentPlayer)

            promote = getPromotion(gameWindow, side, board, fro, to, True)
            side, board, flags = performMove(side, board, fro, to, flags)

            moves.append(convertToAlgebraic(fro, to, promote))
            sel = [0, 0]


