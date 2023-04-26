"""
In this file, we implement a basic chess player algorithm in python.

"""

from chessGameplay.features.primary import *
from chessGameplay.features.constants import *

maxValue = 1000000
searchDepth = 2

# Calculates a simple score for a given board state
def calculateScore(chessBoard):
    totalScore = 0
    for xPos, yPos, chessPiece in chessBoard[0]:
        if chessPiece == "p":
            totalScore += 1 + whitePawnEval[yPos - 1][xPos - 1]
        elif chessPiece == "b":
            totalScore += 9 + whiteBishopEval[yPos - 1][xPos - 1]
        elif chessPiece == "n":
            totalScore += 9 + knightEval[yPos - 1][xPos - 1]
        elif chessPiece == "r":
            totalScore += 14 + whiteRookEval[yPos - 1][xPos - 1]
        elif chessPiece == "q":
            totalScore += 25 + queenEval[yPos - 1][xPos - 1]
        elif chessPiece == "k":
            totalScore += 200 + whiteKingEval[yPos - 1][xPos - 1]

    for xPos, yPos, chessPiece in chessBoard[1]:
        if chessPiece == "p":
            totalScore -= 1 + blackPawnEval[yPos - 1][xPos - 1]
        elif chessPiece == "b":
            totalScore -= 9 + blackBishopEval[yPos - 1][xPos - 1]
        elif chessPiece == "n":
            totalScore -= 9 + knightEval[yPos - 1][xPos - 1]
        elif chessPiece == "r":
            totalScore -= 14 + blackRookEval[yPos - 1][xPos - 1]
        elif chessPiece == "q":
            totalScore -= 25 + queenEval[yPos - 1][xPos - 1]
        elif chessPiece == "k":
            totalScore -= 200 + blackKingEval[yPos - 1][xPos - 1]

    return totalScore

# MiniMax algorithm implementation with alpha-beta pruning
def miniMaxSearch(player, chessBoard, gameFlags, depth=searchDepth, alpha=-maxValue, beta=maxValue):
    if depth == 0:
        return calculateScore(chessBoard)

    if not player:
        bestScore = -maxValue
        for start, end in getLegalMoves(player, chessBoard, gameFlags):
            moveData = performMove(player, chessBoard, start, end, gameFlags)
            nodeScore = miniMaxSearch(*moveData, depth - 1, alpha, beta)
            if nodeScore > bestScore:
                bestScore = nodeScore
                if depth == searchDepth:
                    optimalMove = (start, end)
            alpha = max(alpha, bestScore)
            if alpha >= beta:
                break

    else:
        bestScore = maxValue
        for start, end in getLegalMoves(player, chessBoard, gameFlags):
            moveData = performMove(player, chessBoard, start, end, gameFlags)
            nodeScore = miniMaxSearch(*moveData, depth - 1, alpha, beta)
            if nodeScore < bestScore:
                bestScore = nodeScore
                if depth == searchDepth:
                    optimalMove = (start, end)
            beta = min(beta, bestScore)
            if alpha >= beta:
                break

    if depth == searchDepth:
        return optimalMove
    else:
        return bestScore
