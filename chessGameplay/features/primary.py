"""
In this file, we define the core chess-related functions.

"""
# A simple function to make a copy of the board
def makeCopy(board):
    return [[list(j) for j in board[i]] for i in range(2)]       

# Returns the type of piece at a position, or None if the position is empty
def getPieceType(side, board, pos):
    for piece in board[side]:
        if piece[:2] == pos:
            return piece[2]

# Determines if the position is occupied by a piece of the given side
def isOccupied(side, board, pos):
    return getPieceType(side, board, pos) is not None

# Determines if the given positions are empty or not
def arePositionsEmpty(board, *posList):
    for pos in posList:
        for side in range(2):
            if isOccupied(side, board, pos):
                return False
    return True

# Determines if the king of a given side is in check
def isInCheck(side, board):
    for piece in board[side]:
        if piece[2] == "k":
            for i in board[not side]:
                if piece[:2] in possibleMoves(not side, board, i):
                    return True
            return False

# Determines all the possible legal moves available for the side
def getLegalMoves(side, board, flags):
    for piece in board[side]:
        for pos in legalMoves(side, board, piece, flags):
            yield [piece[:2], pos]

# Determines if a game has ended or not
def hasGameEnded(side, board, flags):
    for _ in getLegalMoves(side, board, flags):
        return False
    return True

# Moves a piece from one coordinate to another, handling captures, pawn promotions, and en passant
def movePiece(side, board, fro, to, promote="p"):
    UP = 8 if side else 1
    DOWN = 1 if side else 8
    ALLOW_ENP = fro[1] == 4 + side and to[0] != fro[0] and arePositionsEmpty(board, to)
    for piece in board[not side]:
        if piece[:2] == to:
            board[not side].remove(piece)
            break

    for piece in board[side]:
        if piece[:2] == fro:
            piece[:2] = to
            if piece[2] == "k":
                if fro[0] - to[0] == 2:
                    movePiece(side, board, [1, DOWN], [4, DOWN])
                elif to[0] - fro[0] == 2:
                    movePiece(side, board, [8, DOWN], [6, DOWN])

            if piece[2] == "p":
                if to[1] == UP:
                    board[side].remove(piece)
                    board[side].append([to[0], UP, promote])
                if ALLOW_ENP:
                    board[not side].remove([to[0], fro[1], "p"])
            break
    return board

# Determines if a move puts the player's own king in check
def isMoveSafe(side, board, fro, to):
    return not isInCheck(side, movePiece(side, makeCopy(board), fro, to))

# This function checks if a move is valid or not
def isMoveValid(player, gameBoard, statusFlags, startPos, endPos):
    if 0 < endPos[0] < 9 and 0 < endPos[1] < 9 and not isOccupied(player, gameBoard, endPos):
        piece = startPos + [getPieceType(player, gameBoard, startPos)]
        if endPos in possibleMoves(player, gameBoard, piece, statusFlags):
            return isMoveSafe(player, gameBoard, startPos, endPos)

# This executes the move, updates the status flags, and switches the player
def performMove(player, gameBoard, startPos, endPos, statusFlags, promotion="q"):
    updatedBoard = movePiece(player, makeCopy(gameBoard), startPos, endPos, promotion)
    updatedFlags = modifyFlags(player, updatedBoard, startPos, endPos, statusFlags)
    return not player, updatedBoard, updatedFlags

# This function updates all the status flags required for castling and en passant
def modifyFlags(player, gameBoard, startPos, endPos, statusFlags):
    castleStatus = list(statusFlags[0])
    if [5, 8, "k"] not in gameBoard[0] or [1, 8, "r"] not in gameBoard[0]:
        castleStatus[0] = False
    if [5, 8, "k"] not in gameBoard[0] or [8, 8, "r"] not in gameBoard[0]:
        castleStatus[1] = False
    if [5, 1, "k"] not in gameBoard[1] or [1, 1, "r"] not in gameBoard[1]:
        castleStatus[2] = False
    if [5, 1, "k"] not in gameBoard[1] or [8, 1, "r"] not in gameBoard[1]:
        castleStatus[3] = False

    enPassant = None
    if getPieceType(player, gameBoard, endPos) == "p":
        if startPos[1] - endPos[1] == 2:
            enPassant = [endPos[0], 6]
        elif endPos[1] - startPos[1] == 2:
            enPassant = [endPos[0], 3]

    return castleStatus, enPassant

# This generates all possible legal moves for that piece. 
def legalMoves(player, gameBoard, piece, statusFlags):
    for move in possibleMoves(player, gameBoard, piece, statusFlags):
        if 0 < move[0] < 9 and 0 < move[1] < 9 and not isOccupied(player, gameBoard, move):
            if isMoveSafe(player, gameBoard, piece[:2], move):
                yield move
    
# This yields all possible moves by the piece
def possibleMoves(player, gameBoard, piece, statusFlags=[None, None]):  
    x, y, ptype = piece
    if ptype == "p":
        if not player:
            if y == 7 and arePositionsEmpty(gameBoard, [x, 6], [x, 5]):
                yield [x, 5]
            if arePositionsEmpty(gameBoard, [x, y - 1]):
                yield [x, y - 1]
                
            for i in ([x + 1, y - 1], [x - 1, y - 1]):
                if isOccupied(1, gameBoard, i) or statusFlags[1] == i:
                    yield i
        else:
            if y == 2 and arePositionsEmpty(gameBoard, [x, 3], [x, 4]):
                yield [x, 4]
            if arePositionsEmpty(gameBoard, [x, y + 1]):
                yield [x, y + 1]

            for i in ([x + 1, y + 1], [x - 1, y + 1]):
                if isOccupied(0, gameBoard, i) or statusFlags[1] == i:
                    yield i

    elif ptype == "n":
        yield from (
            [x + 1, y + 2], [x + 1, y - 2], [x - 1, y + 2], [x - 1, y - 2],
            [x + 2, y + 1], [x + 2, y - 1], [x - 2, y + 1], [x - 2, y - 1]
        )

    elif ptype == "b":
        for i in range(1, 8):
            yield [x + i, y + i]
            if not arePositionsEmpty(gameBoard, [x + i, y + i]):
                break
        for i in range(1, 8):
            yield [x + i, y - i]
            if not arePositionsEmpty(gameBoard, [x + i, y - i]):
                break
        for i in range(1, 8):
            yield [x - i, y + i]
            if not arePositionsEmpty(gameBoard, [x - i, y + i]):
                break
        for i in range(1, 8):
            yield [x - i, y - i]
            if not arePositionsEmpty(gameBoard, [x - i, y - i]):
                break

    elif ptype == "r":
        for i in range(1, 8):
            yield [x + i, y]
            if not arePositionsEmpty(gameBoard, [x + i, y]):
                break
        for i in range(1, 8):
            yield [x - i, y]
            if not arePositionsEmpty(gameBoard, [x - i, y]):
                break
        for i in range(1, 8):
            yield [x, y + i]
            if not arePositionsEmpty(gameBoard, [x, y + i]):
                break
        for i in range(1, 8):
            yield [x, y - i]
            if not arePositionsEmpty(gameBoard, [x, y - i]):
                break

    elif ptype == "q":
        yield from possibleMoves(player, gameBoard, [x, y, "b"])
        yield from possibleMoves(player, gameBoard, [x, y, "r"])

    elif ptype == "k":
        if statusFlags[0] is not None and not isInCheck(player, gameBoard):
            if statusFlags[0][0] and arePositionsEmpty(gameBoard, [2, 8], [3, 8], [4, 8]):
                if isMoveSafe(0, gameBoard, [5, 8], [4, 8]):
                    yield [3, 8]
            if statusFlags[0][1] and arePositionsEmpty(gameBoard, [6, 8], [7, 8]):
                if isMoveSafe(0, gameBoard, [5, 8], [6, 8]):
                    yield [7, 8]
            if statusFlags[0][2] and arePositionsEmpty(gameBoard, [2, 1], [3, 1], [4, 1]):
                if isMoveSafe(1, gameBoard, [5, 1], [4, 1]):
                    yield [3, 1]
            if statusFlags[0][3] and arePositionsEmpty(gameBoard, [6, 1], [7, 1]):
                if isMoveSafe(1, gameBoard, [5, 1], [6, 1]):
                    yield [7, 1]

        yield from (
            [x - 1, y - 1], [x, y - 1], [x + 1, y - 1], [x - 1, y],
            [x - 1, y + 1], [x, y + 1], [x + 1, y + 1], [x + 1, y]
        )