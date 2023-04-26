"""
In this file, we define some basic gui-related functions

"""
import pygame
from extras.loader import *
from extras import sound

# Optimize images for speed by applying 'transformAlpha()' on all pieces.
def transformAlpha(window):
    for i in range(2):
        for key, value in CHESS.PIECES[i].items():
            CHESS.PIECES[i][key] = value.convert_alpha(window)

# Display the selection menu, get user input, and return the chosen piece.
def getUserSelection(window, side):
    window.blit(CHESS.CHOOSE, (130, 10))
    window.blit(CHESS.PIECES[side]["q"], (250, 0))
    window.blit(CHESS.PIECES[side]["b"], (300, 0))
    window.blit(CHESS.PIECES[side]["r"], (350, 0))
    window.blit(CHESS.PIECES[side]["n"], (400, 0))
    pygame.display.update((0, 0, 500, 50))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0 < event.pos[1] < 50:
                    if 250 < event.pos[0] < 300:
                        return "q"
                    elif 300 < event.pos[0] < 350:
                        return "b"
                    elif 350 < event.pos[0] < 400:
                        return "r"
                    elif 400 < event.pos[0] < 450:
                        return "n"

def displayTimeOut(window, side):
    pygame.draw.rect(window, (0, 0, 0), (100, 190, 300, 120))
    pygame.draw.rect(window, (255, 255, 255), (100, 190, 300, 120), 4)
    
    window.blit(CHESS.TIMEUP[0], (220, 200))
    window.blit(CHESS.TIMEUP[1], (105, 220))
    window.blit(CHESS.TIMEUP[2], (115, 240))
    
    window.blit(CHESS.OK, (230, 270))
    pygame.draw.rect(window, (255, 255, 255), (225, 270, 50, 30), 2)
    
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 225 < event.pos[0] < 275 and 270 < event.pos[1] < 300:
                    return

def displayClock(window, timer):
    if timer is None:
        return
    
    min1, sec1 = divmod(timer[0] // 1000, 60)
    min2, sec2 = divmod(timer[1] // 1000, 60)
    
    putLargeNum(window, format(min1, "02"), (100, 460), False)
    window.blit(CHESS.COL, (130, 460))
    putLargeNum(window, format(sec1, "02"), (140, 460), False)
    putLargeNum(window, format(min2, "02"), (210, 460), False)
    window.blit(CHESS.COL, (240, 460))
    putLargeNum(window, format(sec2, "02"), (250, 460), False)
    
    window.blit(CHESS.PIECES[0]["k"], (50, 450))
    window.blit(CHESS.PIECES[1]["k"], (278, 450))
    
    pygame.display.update()

# Draw the chessboard.
def renderBoard(window):
    window.fill((32, 32, 32))
    pygame.draw.rect(window, (119, 154, 88), (50, 50, 400, 400))
    for y in range(1, 9):
        for x in range(1, 9):
            if (x + y) % 2 == 0:
                pygame.draw.rect(window, (234, 235, 200), (50 * x, 50 * y, 50, 50))
                
# Render all pieces on the chessboard.
def placePieces(window, board, flipped):
    for side in range(2):
        for x, y, pieceType in board[side]:
            if flipped:
                x, y = 9 - x, 9 - y
            window.blit(CHESS.PIECES[side][pieceType], (x * 50, y * 50))

# Show a prompt screen when a user tries to quit, requiring them to choose Yes or No.
# Return True or False based on their choice.
def confirmQuit(window, message=None):
    pygame.draw.rect(window, (0, 0, 0), (110, 160, 280, 130))
    pygame.draw.rect(window, (255, 255, 255), (110, 160, 280, 130), 4)

    pygame.draw.rect(window, (255, 255, 255), (120, 160, 260, 60), 2)

    window.blit(CHESS.YES, (145, 240))
    window.blit(CHESS.NO, (305, 240))
    pygame.draw.rect(window, (255, 255, 255), (140, 240, 60, 28), 2)
    pygame.draw.rect(window, (255, 255, 255), (300, 240, 50, 28), 2)
    
    if message is None:
        window.blit(CHESS.MESSAGE[0], (130, 160))
        window.blit(CHESS.MESSAGE[1], (190, 190))

    elif message == -1:
        window.blit(CHESS.MESSAGE[0], (130, 160))
        window.blit(CHESS.MESSAGE[1], (190, 190))
        
        window.blit(CHESS.SAVE_ERR, (115, 270))
        
    else:
        window.blit(CHESS.MESSAGE2[0], (123, 160))
        window.blit(CHESS.MESSAGE2[1], (145, 190))
        
        window.blit(CHESS.MSG, (135, 270))
        putNum(window, message, (345, 270))

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 240 < event.pos[1] < 270:
                    if 140 < event.pos[0] < 200:
                        return True
                    elif 300 < event.pos[0] < 350:
                        return False

# Set up the initial game state.
def initializeGame(window, load):
    transformAlpha(window)
    sound.play_start(load)
    renderBoard(window)

    for j in range(8):
        window.blit(CHESS.PIECES[0]["p"], (0.5 * 100 * (j + 1), 225 + 1.25 * 100))
        window.blit(CHESS.PIECES[1]["p"], (0.5 * 100 * (j + 1), 225 - 1.25 * 100))

    for j, pc in enumerate(["r", "n", "b", "q", "k", "b", "n", "r"]):
        window.blit(CHESS.PIECES[0][pc], (0.5 * 100 * (j + 1), 225 + 1.75 * 100))
        window.blit(CHESS.PIECES[1][pc], (0.5 * 100 * (j + 1), 225 - 1.75 * 100))

    pygame.display.update()
