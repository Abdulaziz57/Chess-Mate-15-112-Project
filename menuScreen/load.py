'''
In this file, we manage the loadgame menu which is called when user clicks
loadgame button on main menu.

'''

import os
import pygame
from extras.loader import LOADGAME, BACK, putLargeNum, putDT
from extras.utilities import roundedRectangle

# This function searches for saved games
def findSavedGames():
    for i in range(20):
        path = os.path.join("res", "savedGames", "game" + str(i) + ".txt")
        if os.path.exists(path):
            with open(path, "r") as f:
                data = f.read().splitlines()[:2]
            yield (i, data[0].split(" ")[0], data[1])

# This function removes a game.
def removeGame(gameId):
    fileName = os.path.join("res", "savedGames", "game" + str(gameId) + ".txt")
    if os.path.exists(fileName):
        os.remove(fileName)

# This function loads the game, returns the necessary data
def retrieveGame(gameId):
    fileName = os.path.join("res", "savedGames", "game" + str(gameId) + ".txt")
    if os.path.exists(fileName):
        with open(fileName, "r") as file:
            lines = file.read().splitlines()
        
        if len(lines) < 4:
            lines.extend([""] * (4 - len(lines)))
            
        if lines[0].strip() == "multi":
            temp = list(map(int, lines[3].strip().split()))
            if len(temp) == 0:
                return "multi", None, None, lines[2]
            
            elif len(temp) == 1:
                return "multi", temp[0], None, lines[2]
            
            else:
                return "multi", temp[0], temp[1:], lines[2]
                
        else:
            temp = lines[0].strip().split()
            return [temp[0]] + list(map(int, temp[1:])) + [lines[2]]
    else:
        return None
    
# This asks the user for confirmation while deleting a game
def confirmDeletion(window):
    roundedRectangle(window, (255, 255, 255), (110, 160, 280, 130), 10, 4)
    
    window.blit(LOADGAME.MESSAGE[0], (116, 160))
    window.blit(LOADGAME.MESSAGE[1], (118, 190))
        
    window.blit(LOADGAME.YES, (145, 240))
    window.blit(LOADGAME.NO, (305, 240))
    pygame.draw.rect(window, (255, 255, 255), (140, 240, 60, 28), 2)
    pygame.draw.rect(window, (255, 255, 255), (300, 240, 46, 28), 2)

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 240 < event.pos[1] < 270:
                    if 140 < event.pos[0] < 200:
                        return True
                    elif 300 < event.pos[0] < 350:
                        return False

# This function displays the screen
def displayScreen(window, page, scanned):
    window.fill((0, 0, 0))
    roundedRectangle(window, (255, 255, 255), (70, 15, 340, 60), 15, 4)
    window.blit(BACK, (460, 0))
    window.blit(LOADGAME.HEAD, (100, 18))
    window.blit(LOADGAME.LIST, (125, 80))
    pygame.draw.line(window, (255, 255, 255), (125, 122), (360, 122), 3)
    
    if not scanned:
        window.blit(LOADGAME.EMPTY, (40, 130))
    
    for cnt, i in enumerate(scanned):
        if cnt // 5 == page:
            num = 60 * (cnt % 5) + 120
            
            roundedRectangle(window, (255, 255, 255), (10, num, 480, 50), 10, 3)
            
            window.blit(LOADGAME.GAME, (15, num + 8))
            putLargeNum(window, i[0], (90, num + 8))
            pygame.draw.line(window, (255, 255, 255), (118, num + 5),
                             (118, num + 45), 2)
            
            window.blit(LOADGAME.TYPHEAD, (122, num + 2))
            window.blit(LOADGAME.TYP[i[1]], (122, num + 23))
            pygame.draw.line(window, (255, 255, 255), (226, num + 5),
                             (226, num + 45), 2)
            
            window.blit(LOADGAME.DATE, (230, num + 2))
            window.blit(LOADGAME.TIME, (230, num + 23))
            putDT(window, i[2], (278, num + 2))
            
            roundedRectangle(window, (255, 255, 255), (362, num + 5, 40, 40), 6, 2)
            window.blit(LOADGAME.DEL, (366, num + 9))
            roundedRectangle(window, (255, 255, 255), (405, num + 5, 80, 40), 6, 2)
            window.blit(LOADGAME.LOAD, (410, num + 10))
    
    roundedRectangle(window, (255, 255, 255), (160, 430, 20, 46), 6, 2)
    window.blit(LOADGAME.LEFT, (160, 430))
    roundedRectangle(window, (255, 255, 255), (320, 430, 20, 46), 6, 2)
    window.blit(LOADGAME.RIGHT, (320, 430))
        
    roundedRectangle(window, (255, 255, 255), (187, 430, 125, 46), 10, 2)
    window.blit(LOADGAME.PAGE[page], (190, 430))    
    pygame.display.update()

# This is the main function, called by the main menu
def main(window):
    scan = tuple(findSavedGames())
    pages = (len(scan) - 1) // 5
    pages = max(pages, 0)
    pg = 0
    clock = pygame.time.Clock()
    while True:
        clock.tick(24)
        displayScreen(window, pg, scan)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                
                if 460 < x < 500 and 0 < y < 50:
                    return 1
                
                if 430 < y < 476:
                    if 160 < x < 180:
                        pg = pages if pg == 0 else pg - 1
                    elif 320 < x < 340:
                        pg = 0 if pg == pages else pg + 1
                
                if 362 < x < 402:
                    for i in range(5):
                        if 120 + 60*i < y < 160 + 60*i:
                            if scan == tuple(findSavedGames()):
                                if 5*pg + i < len(scan):
                                    if confirmDeletion(window):
                                        removeGame(scan[5*pg + i][0])
                                    scan = tuple(findSavedGames())
                                    pages = (len(scan) - 1) // 5
                                    pages = max(pages, 0)
                                    if pg > pages:
                                        pg = pages                  
                                    break
                            
                elif 405 < x < 485:
                    for i in range(5):
                        if 120 + 60*i < y < 160 + 60*i:
                            newScan = tuple(findSavedGames())
                            if 5*pg + i < len(newScan):
                                return retrieveGame(newScan[5*pg + i][0])
                            