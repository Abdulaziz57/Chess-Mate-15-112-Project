"""
This file loads all the images and texts that are used.
"""

import os.path
import pygame

# Initialize pygame.font module and load the font file.
pygame.font.init()
FONT = os.path.join("res", "Asimov.otf")

# Load different sizes of the font.
head = pygame.font.Font(FONT, 80)
large = pygame.font.Font(FONT, 50)
medium = pygame.font.Font(FONT, 38)
small = pygame.font.Font(FONT, 27)
vsmall = pygame.font.Font(FONT, 17)

# Define RGB color constants for use.
WHITE = (255, 255, 255)
GREY = (180, 180, 180)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (200, 20, 20)

# Define a few constants that contain loaded texts of numbers and chararters.
NUM = [vsmall.render(str(i), True, WHITE) for i in range(10)]
LNUM = [small.render(str(i), True, WHITE) for i in range(10)]
BLNUM = [small.render(str(i), True, BLACK) for i in range(10)]
SLASH = vsmall.render("/", True, WHITE)
COLON = vsmall.render(":", True, WHITE)

# This function displays a number in a position, very small sized text used.
def putNum(win, num, pos):
    for cnt, i in enumerate(list(str(num))):
        win.blit(NUM[int(i)], (pos[0] + (cnt * 9), pos[1]))

def renderText(text, font, position):
    renderedText = font.render(text, True, WHITE)
    background_surface = pygame.Surface(renderedText.get_size(), pygame.SRCALPHA)
    background_surface.fill(BLACK)
    background_surface.blit(renderedText, (0, 0))
    return background_surface, position

# This function displays a number in a position, Small sized text used.
def putLargeNum(win, num, pos, white=True):
    for cnt, i in enumerate(list(str(num))):
        if white:
            win.blit(LNUM[int(i)], (pos[0] + (cnt * 14), pos[1]))
        else:
            win.blit(BLNUM[int(i)], (pos[0] + (cnt * 14), pos[1]))

# This function displays the date and time in a position on the screen.
def putDT(win, DT, pos):
    var = DT.split()
    date = var[0].split("/")
    time = var[1].split(":")

    for cnt, num in enumerate(map(lambda x: format(int(x), "02"), date)):
        putNum(win, num, (pos[0] + 24 * cnt - 5, pos[1]))

    win.blit(SLASH, (pos[0] + 13, pos[1]))
    win.blit(SLASH, (pos[0] + 35, pos[1]))

    for cnt, num in enumerate(map(lambda x: format(int(x), "02"), time)):
        putNum(win, num, (pos[0] + 24 * cnt, pos[1] + 21))

    win.blit(COLON, (pos[0] + 20, pos[1] + 21))
    win.blit(COLON, (pos[0] + 44, pos[1] + 21))

# This splits a string at regular intervals of "index" characters
def splitstr(string, index=57):
    data = []
    while len(string) >= index:
        data.append(string[:index])
        string = string[index:]
    data.append(string)
    return data

# Defined important globals for loading background image sprites.
BGSPRITE = pygame.image.load(os.path.join("res", "img", "bgsprites.jpg"))
PSPRITE = pygame.image.load(os.path.join("res", "img", "piecesprite.png"))

# Load global image for back
BACK = pygame.image.load(os.path.join("res", "img", "back.png"))

class CHESS:
    PIECES = ({}, {})
    for i, ptype in enumerate(["k", "q", "b", "n", "r", "p"]):
        for side in range(2):
            PIECES[side][ptype] = PSPRITE.subsurface((i * 50, side * 50, 50, 50))

    CHECK = small.render("CHECK!", True, BLACK)
    STALEMATE = small.render("STALEMATE!", True, BLACK)
    CHECKMATE = small.render("CHECKMATE!", True, BLACK)
    LOST = small.render("LOST", True, BLACK)
    CHOOSE = small.render("CHOOSE:", True, BLACK)
    SAVE = small.render("Save Game", True, WHITE)
    UNDO = small.render("Undo", True, WHITE)

    MESSAGE = (
        small.render("Do you want to quit", True, WHITE),
        small.render("this game?", True, WHITE),
    )
    
    MESSAGE2 = (
        small.render("Game saved. Now do", True, WHITE),
        small.render("you want to quit?", True, WHITE),
    )

    YES = small.render("YES", True, WHITE)
    NO = small.render("NO", True, WHITE)
    MSG = vsmall.render("Game will be saved with ID", True, WHITE)
    SAVE_ERR = vsmall.render("ERROR: SaveGame Limit Exeeded", True, WHITE)

    TURN = (
        small.render("Others turn", True, WHITE),
        small.render("Your turn", True, WHITE),
    )

    DRAW = small.render("Draw", True, BLACK)
    RESIGN = small.render("Resign", True, BLACK)
    
    TIMEUP = (
        vsmall.render("Time Up!", True, WHITE),
        vsmall.render("Technically the game is over, but you", True, WHITE),
        vsmall.render("can still continue if you wish to - :)", True, WHITE),
    )
    
    OK = small.render("Ok", True, WHITE)
    COL = small.render(":", True, BLACK)

class LOADGAME:
    HEAD = large.render("Load Games", True, WHITE)
    LIST = medium.render("List of Games", True, WHITE)
    EMPTY = small.render("There are no saved games yet.....", True, WHITE)
    GAME = small.render("Game", True, WHITE)
    TYPHEAD = vsmall.render("Game Type:", True, WHITE)
    TYP = {
        "single": vsmall.render("SinglePlayer", True, WHITE),
        "mysingle": vsmall.render("SinglePlayer", True, WHITE),
        "multi": vsmall.render("MultiPlayer", True, WHITE),
    }
    DATE = vsmall.render("Date-", True, WHITE)
    TIME = vsmall.render("Time-", True, WHITE)

    DEL = pygame.image.load(os.path.join("res", "img", "delete.jpg"))
    LOAD = small.render("LOAD", True, WHITE)

    MESSAGE = (
        small.render("Are you sure that you", True, WHITE),
        small.render("want to delete game?", True, WHITE),
    )
    YES = small.render("YES", True, WHITE)
    NO = small.render("NO", True, WHITE)

    LEFT = medium.render("<", True, WHITE)
    RIGHT = medium.render(">", True, WHITE)
    PAGE = [medium.render("Page " + str(i), True, WHITE) for i in range(1, 5)]

class MAIN:
    HEADING = head.render("ChessMate", True, WHITE)
    BG = [BGSPRITE.subsurface((i * 500, 0, 500, 500)) for i in range(4)]

    SINGLE, SINGLE_POS = renderText("SinglePlayer", medium, (0, 0))
    MULTI, MULTI_POS = renderText("MultiPlayer", medium, (0, 0))
    LOAD, LOAD_POS = renderText("Load Game", medium, (0, 0))
    ABOUT, ABOUT_POS = renderText("About", medium, (0, 0))
    PREF, PREF_POS = renderText("Preferences", medium, (0, 0))

    SINGLE_H = medium.render("SinglePlayer", True, GREY)
    MULTI_H = medium.render("MultiPlayer", True, GREY)
    LOAD_H = medium.render("Load Game", True, GREY)
    ABOUT_H = medium.render("About", True, GREY)
    PREF_H = medium.render("Preferences", True, GREY)

class PREF:
    HEAD = large.render("Preferences", True, WHITE)

    SOUNDS = medium.render("Sounds", True, WHITE)
    FLIP = medium.render("Flip screen", True, WHITE)
    CLOCK = medium.render("Show Clock", True, WHITE)
    SLIDESHOW = medium.render("Slideshow", True, WHITE)
    MOVE = medium.render("Moves", True, WHITE)
    UNDO = medium.render("Allow undo", True, WHITE)

    COLON = medium.render(":", True, WHITE)

    TRUE = medium.render("True", True, WHITE)
    FALSE = medium.render("False", True, WHITE)

    SOUNDS_H = (
        vsmall.render("Play different sounds", True, WHITE),
        vsmall.render("and music", True, WHITE),
    )
    FLIP_H = (
        vsmall.render("This flips the screen", True, WHITE),
        vsmall.render("after each move", True, WHITE),
    )
    CLOCK_H = (
        vsmall.render("Show a clock in chess", True, WHITE),
        vsmall.render("when timer is disabled", True, WHITE),
    )
    SLIDESHOW_H = (
        vsmall.render("This shows a slide of", True, WHITE),
        vsmall.render("backgrounds on screen", True, WHITE),
    )
    MOVE_H = (
        vsmall.render("This shows all the legal", True, WHITE),
        vsmall.render("moves of a selected piece", True, WHITE),
    )
    UNDO_H = (
        vsmall.render("This allowes undo if", True, WHITE),
        vsmall.render("set to be true", True, WHITE),
    )

    BSAVE = medium.render("Save", True, WHITE)
    TIP = vsmall.render("TIP: Hover the mouse over the feature", True, WHITE)
    TIP2 = vsmall.render("name to know more about it.", True, WHITE)

    PROMPT = (
        vsmall.render("Are you sure you want to leave?", True, WHITE),
        vsmall.render("Any changes will not be saved.", True, WHITE),
    )

    YES = small.render("YES", True, WHITE)
    NO = small.render("NO", True, WHITE)


class SINGLE:
    HEAD = large.render("Singleplayer", True, WHITE)
    SELECT = pygame.image.load(os.path.join("res", "img", "select.jpg"))
    CHOOSE = small.render("Choose:", True, WHITE)
    START = small.render("Start Game", True, WHITE)
    OR = medium.render("OR", True, WHITE)
    
    with open(os.path.join("res", "texts", "single1.txt")) as f:
        PARA1 = [vsmall.render(i, True, WHITE) for i in f.read().splitlines()]
        
    LEVEL = small.render("Level:", True, WHITE)

    BACK = vsmall.render("Go Back", True, WHITE)
    OK = vsmall.render("Ok", True, WHITE)
    NOTNOW = vsmall.render("Not Now", True, WHITE)


class ABOUT:
    HEAD = medium.render("About ChessMate", True, WHITE)

    with open(os.path.join("res", "texts", "about.txt"), "r") as f:
        TEXT = [vsmall.render(i, True, WHITE) for i in f.read().splitlines()]
        
class TIMER:
    HEAD = large.render("Timer Menu", True, WHITE)
    
    YES = small.render("Yes", True, WHITE)
    NO = small.render("No", True, WHITE)
    
    PROMPT = vsmall.render("Do you want to set timer?", True, WHITE)

    with open(os.path.join("res", "texts", "timer.txt"), "r") as f:
        TEXT = [vsmall.render(i, True, WHITE) for i in f.read().splitlines()]
    

pygame.font.quit()
