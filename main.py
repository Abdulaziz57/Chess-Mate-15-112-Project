"""
Run this file to launch the program.
In this file, we handle the main menu which gets displayed at runtime.
"""
import sys  
import pygame
import chessGameplay
import menuScreen
from extras.loader import MAIN
from extras import sound

sys.stdout.flush()

# Some initialisation
pygame.init()
clock = pygame.time.Clock()

# Initialise display, set the caption and icon. Use SCALED if on pygame 2.
if pygame.version.vernum[0] >= 2:
    win = pygame.display.set_mode((500, 500), pygame.SCALED)
else:
    win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("ChessMate")

# Coordinates of buttons in rectangle notation.
sngl = (260, 140, 220, 40)
mult = (280, 200, 200, 40)
onln = (360, 260, 120, 40)
load = (280, 320, 200, 40)
pref = (0, 450, 210, 40)
abt = (390, 450, 110, 40)
hwto = (410, 410, 90, 30)
stok = (0, 410, 240, 30)

# This is the function that displays the main screen.
def showMain(prefs):
    global cnt, img

    win.blit(MAIN.BG[img], (0, 0))

    if prefs["slideshow"]:
        cnt += 1
        if cnt >= 150:
            s = pygame.Surface((500, 500))
            s.set_alpha((cnt - 150) * 4)
            s.fill((0, 0, 0))
            win.blit(s, (0, 0))

        if cnt == 210:
            cnt = 0
            img = 0 if img == 3 else img + 1
    else:
        cnt = -150
        img = 0

    win.blit(MAIN.HEADING, (50, 20))
    pygame.draw.line(win, (255, 255, 255), (50, 100), (450, 100), 4)

    win.blit(MAIN.SINGLE, sngl[:2])
    win.blit(MAIN.MULTI, mult[:2])
    win.blit(MAIN.LOAD, load[:2])
    win.blit(MAIN.ABOUT, abt[:2])
    win.blit(MAIN.PREF, pref[:2])
    
# Initialize a few more variables
cnt = 0
img = 0
run = True

prefs = menuScreen.prefrences.retrieveSettings()
music = sound.Music()
music.play(prefs)

while run:
    # Start the game loop at 30fps, show the screen every time at first
    clock.tick(30)
    showMain(prefs)

    x, y = pygame.mouse.get_pos()

    if sngl[0] < x < sum(sngl[::2]) and sngl[1] < y < sum(sngl[1::2]):
        win.blit(MAIN.SINGLE_H, sngl[:2])

    if mult[0] < x < sum(mult[::2]) and mult[1] < y < sum(mult[1::2]):
        win.blit(MAIN.MULTI_H, mult[:2])


    if load[0] < x < sum(load[::2]) and load[1] < y < sum(load[1::2]):
        win.blit(MAIN.LOAD_H, load[:2])

    if pref[0] < x < sum(pref[::2]) and pref[1] < y < sum(pref[1::2]):
        win.blit(MAIN.PREF_H, pref[:2])

    if abt[0] < x < sum(abt[::2]) and abt[1] < y < sum(abt[1::2]):
        win.blit(MAIN.ABOUT_H, abt[:2])

    # Begin pygame event loop to catch all events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if sngl[0] < x < sum(sngl[::2]) and sngl[1] < y < sum(sngl[1::2]):
                sound.play_click(prefs)
                ret = menuScreen.splayermenu(win)
                if ret == 0:
                    run = False
                elif ret != 1:
                    if ret[0]:
                        run = chessGameplay.singleplayer(win, ret[1], prefs)

            elif mult[0] < x < sum(mult[::2]) and mult[1] < y < sum(mult[1::2]):
                sound.play_click(prefs)
                ret = menuScreen.timermenu(win, prefs)
                if ret == 0:
                    run = False
                elif ret != 1:
                    run = chessGameplay.multiplayer(win, ret[0], ret[1], prefs)

            elif load[0] < x < sum(load[::2]) and load[1] < y < sum(load[1::2]):
                sound.play_click(prefs)
                ret = menuScreen.loadgamemenu(win)
                if ret == 0:
                    run = False

                elif ret != 1:
                    if ret[0] == "multi":
                        run = chessGameplay.multiplayer(win, *ret[1:3], prefs, ret[3])
                    elif ret[0] == "single":
                        run = chessGameplay.singleplayer(win, ret[1], prefs, ret[2])

            elif pref[0] < x < sum(pref[::2]) and pref[1] < y < sum(pref[1::2]):
                sound.play_click(prefs)
                run = menuScreen.prefmenu(win)
                
                prefs = menuScreen.prefrences.retrieveSettings()
                if music.is_playing():
                    if not prefs["sounds"]:
                        music.stop()
                else:
                    music.play(prefs)

            elif abt[0] < x < sum(abt[::2]) and abt[1] < y < sum(abt[1::2]):
                sound.play_click(prefs)
                run = menuScreen.aboutmenu(win)

            elif stok[0] < x < sum(stok[::2]) and stok[1] < y < sum(stok[1::2]):
                sound.play_click(prefs)
                run = menuScreen.sfmenu(win)

    # Update the screen every frame
    pygame.display.flip()

# Stop music, quit pygame after the loop is done
music.stop()
pygame.quit()
