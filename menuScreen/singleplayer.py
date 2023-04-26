'''

In this file, we manage the single player menu which is called when user clicks
singleplayer button on main menu.
'''

import os.path
import random

import pygame

from extras.loader import SINGLE, BACK, putLargeNum
from extras.utilities import roundedRectangle


# This shows the screen
def showScreen(win, sel, sel2, lvl):
    win.fill((0, 0, 0))

    roundedRectangle(win, (255, 255, 255), (70, 5, 340, 60), 15, 4)
    win.blit(SINGLE.HEAD, (100, 7))
    win.blit(BACK, (460, 0))

    roundedRectangle(win, (255, 255, 255), (10, 70, 480, 180), 12, 4)
    for cnt, i in enumerate(SINGLE.PARA1):
        y = 75 + cnt * 17
        win.blit(i, (20, y))
    win.blit(SINGLE.CHOOSE, (90, 160))
    win.blit(SINGLE.SELECT, (200, 150))
    pygame.draw.rect(win, (50, 100, 150), (200 + sel*50, 150, 50, 50), 3)

    roundedRectangle(win, (255, 255, 255), (170, 210, 140, 30), 7, 3)
    win.blit(SINGLE.START, (170, 210))

# This is the main function, called from main menu
def main(win):
    sel = sel2 = 0
    lvl = 1
    clock = pygame.time.Clock()
    while True:
        clock.tick(24)
        showScreen(win, sel, sel2, lvl)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 460 < x < 500 and 0 < y < 50:
                    return 1

                if 160 < y < 210 and 200 < x < 350:
                    sel = (x // 50) - 4

                if 430 < y < 480 and 150 < x < 300:
                    sel2 = (x // 50) - 3

                if 380 < y < 410:
                    for i in range(9):
                        if 110 + i*35 < x < 135 + i*35:
                            lvl = i + 1

                if 170 < x < 310 and 220 < y < 250:
                    if sel == 2:
                        return True, random.randint(0, 1)
                    else:
                        return True, sel
        pygame.display.update()
