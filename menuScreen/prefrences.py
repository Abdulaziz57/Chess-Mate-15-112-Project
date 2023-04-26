'''
In this file, we manage the preferences menu which is called when user clicks
preferences button on main menu.

'''

import os.path
import pygame
from extras.loader import PREF, BACK
from extras.utilities import roundedRectangle

featureKeys = ["sounds", "flip", "slideshow", "displayMoves", "enableUndo", "displayTimer"]

defaultPreferences = {"sounds": False, "flip": False,"slideshow": True,
    "displayMoves": True, "enableUndo": True, "displayTimer": False}


# This function stores user settings in a text file.
def storeSettings(settings):
    with open(os.path.join("res", "settings.txt"), "w") as f:
        for key, val in settings.items():
            f.write(key + " = " + str(val) + '\n')

# This function retrieves user settings from a text file
def retrieveSettings():
    path = os.path.join("res", "settings.txt")
    if not os.path.exists(path):
        open(path, "w").close()
    
    with open(path, "r") as f:
        userSettings = {}
        for line in f.read().splitlines():
            splitLine = line.split("=")
            if len(splitLine) == 2: 
                value = splitLine[1].strip().lower()
                if value == "true":
                    userSettings[splitLine[0].strip()] = True
                elif value == "false":
                    userSettings[splitLine[0].strip()] = False
            
        for key in userSettings:
            if key not in featureKeys:
                userSettings.pop(key)
        
        for key in featureKeys:
            if key not in userSettings:
                userSettings[key] = defaultPreferences[key]
        return userSettings

# This function shows an exit confirmation dialog when a user tries to close the application
def exitConfirmation(window):
    roundedRectangle(window, (255, 255, 255), (110, 160, 280, 130), 4, 4)

    window.blit(PREF.PROMPT[0], (130, 165))
    window.blit(PREF.PROMPT[1], (130, 190))

    window.blit(PREF.YES, (145, 240))
    window.blit(PREF.NO, (305, 240))
    pygame.draw.rect(window, (255, 255, 255), (140, 240, 60, 28), 2)
    pygame.draw.rect(window, (255, 255, 255), (300, 240, 45, 28), 2)

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 240 < event.pos[1] < 270:
                    if 140 < event.pos[0] < 200:
                        return True
                    elif 300 < event.pos[0] < 350:
                        return False

# This function shows the screen
def renderSettingsScreen(window, userPreferences):
    window.fill((0, 0, 0))

    roundedRectangle(window, (255, 255, 255), (70, 10, 350, 70), 20, 4)
    roundedRectangle(window, (255, 255, 255), (10, 85, 480, 360), 12, 4)

    window.blit(BACK, (460, 0))
    window.blit(PREF.HEAD, (110, 15))
    
    roundedRectangle(window, (255, 255, 255), (10, 450, 310, 40), 10, 3)
    window.blit(PREF.TIP, (20, 450))
    window.blit(PREF.TIP2, (55, 467))

    window.blit(PREF.SOUNDS, (90, 90))
    window.blit(PREF.FLIP, (25, 150))
    window.blit(PREF.SLIDESHOW, (40, 210))
    window.blit(PREF.MOVE, (100, 270))
    window.blit(PREF.UNDO, (25, 330))
    window.blit(PREF.CLOCK, (25, 390))

    for i in range(6):
        window.blit(PREF.COLON, (225, 90 + (i * 60)))
        if userPreferences[featureKeys[i]]:
            roundedRectangle(
                window, (255, 255, 255), (249, 92 + (60 * i), 80, 40), 8, 2)
        else:
            roundedRectangle(
                window, (255, 255, 255), (359, 92 + (60 * i), 90, 40), 8, 2)
        window.blit(PREF.TRUE, (250, 90 + (i * 60)))
        window.blit(PREF.FALSE, (360, 90 + (i * 60)))

    roundedRectangle(window, (255, 255, 255), (350, 452, 85, 40), 10, 2)
    window.blit(PREF.BSAVE, (350, 450))

    x, y = pygame.mouse.get_pos()
    if 100 < x < 220 and 90 < y < 130:
        pygame.draw.rect(window, (0, 0, 0), (30, 90, 195, 40))
        window.blit(PREF.SOUNDS_H[0], (45, 90))
        window.blit(PREF.SOUNDS_H[1], (80, 110))
    if 25 < x < 220 and 150 < y < 190:
        pygame.draw.rect(window, (0, 0, 0), (15, 150, 210, 50))
        window.blit(PREF.FLIP_H[0], (50, 150))
        window.blit(PREF.FLIP_H[1], (70, 170))
    if 40 < x < 220 and 210 < y < 250:
        pygame.draw.rect(window, (0, 0, 0), (15, 210, 210, 40))
        window.blit(PREF.SLIDESHOW_H[0], (40, 210))
        window.blit(PREF.SLIDESHOW_H[1], (30, 230))
    if 100 < x < 220 and 270 < y < 310:
        pygame.draw.rect(window, (0, 0, 0), (15, 270, 210, 40))
        window.blit(PREF.MOVE_H[0], (35, 270))
        window.blit(PREF.MOVE_H[1], (25, 290))
    if 25 < x < 220 and 330 < y < 370:
        pygame.draw.rect(window, (0, 0, 0), (15, 330, 210, 40))
        window.blit(PREF.UNDO_H[0], (60, 330))
        window.blit(PREF.UNDO_H[1], (85, 350))
    if 25 < x < 220 and 390 < y < 430:
        pygame.draw.rect(window, (0, 0, 0), (15, 390, 210, 40))
        window.blit(PREF.CLOCK_H[0], (50, 390))
        window.blit(PREF.CLOCK_H[1], (40, 410))

# This is the main function, called by the main menu
def settingsEntryPoint(window):
    userPreferences = retrieveSettings()
    settingsClock = pygame.time.Clock()
    while True:
        settingsClock.tick(24)
        renderSettingsScreen(window, userPreferences)
        for event in pygame.event.get():
            if event.type == pygame.QUIT and exitConfirmation(window):
                return 0
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 460 < x < 500 and 0 < y < 50 and exitConfirmation(window):
                    return 1

                if 350 < x < 425 and 450 < y < 490:
                    storeSettings(userPreferences)
                    return 1

                for i in range(6):
                    if 90 + i*60 < y < 130 + i*60:
                        if 250 < x < 330:
                            userPreferences[featureKeys[i]] = True
                        if 360 < x < 430:
                            userPreferences[featureKeys[i]] = False
        pygame.display.update()
