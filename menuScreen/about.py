'''
In this file, we manage the about menu which is called when user clicks
about button on main menu.
'''

import pygame
from extras.loader import ABOUT, BACK
from extras.utilities import roundedRectangle

# Display the screen content
def renderScreen(window):
    window.fill((0, 0, 0))
    roundedRectangle(window, (255, 255, 255), (70, 10, 360, 60), 16, 4)
    roundedRectangle(window, (255, 255, 255), (10, 80, 480, 410), 10, 4)

    window.blit(ABOUT.HEAD, (74, 12))
    for count, item in enumerate(ABOUT.TEXT):
        window.blit(item, (20, 90 + count * 18))

    window.blit(BACK, (460, 0))
    pygame.display.update()

# Main function, called from the main menu
def primaryFunction(window):
    renderScreen(window)
    gameClock = pygame.time.Clock()
    while True:
        gameClock.tick(24)
        for gameEvent in pygame.event.get():
            if gameEvent.type == pygame.QUIT:
                return 0
                
            elif gameEvent.type == pygame.MOUSEBUTTONDOWN:
                posX, posY = gameEvent.pos
                if 460 < posX < 500 and 0 < posY < 50:
                    return 1

