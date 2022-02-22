# -*- coding: utf-8 -*-    
from cv2 import cv2
from os import listdir
from random import randint
from random import random
import numpy as np
import mss
import pyautogui
import time
import sys
from debug import Debug

VERSAO_SCRIPT = "1"

# Pause between actions
pyautogui.PAUSE = 0.2

# Account config
empty_qtd_spaceships = 32
qtd_send_spaceships = 8
cda = 100

global x_scroll
global y_scroll
global h_scroll
global w_scroll
global ship_clicks
global timesScrolled
global scrollChances
global timesTried
ship_clicks = 0
timesScrolled = 0
timesTried = 0
scrollChances = 15

dbg = Debug('debug.log')

def addRandomness(n, randomn_factor_size=None):
    if randomn_factor_size is None:
        randomness_percentage = 0.1
        randomn_factor_size = randomness_percentage * n
    random_factor = 2 * random() * randomn_factor_size
    if random_factor > 5:
        random_factor = 5
    without_average_random_factor = n - randomn_factor_size
    randomized_n = int(without_average_random_factor + random_factor)
    return int(randomized_n)

def moveToWithRandomness(x,y):
    pyautogui.moveTo(addRandomness(x,10),addRandomness(y,10),0.4)

def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string

def load_images(dir_path='./images/'):
    file_names = listdir(dir_path)
    targets = {}
    for file in file_names:
        path = 'images/' + file
        targets[remove_suffix(file, '.png')] = cv2.imread(path)
    return targets

def show(rectangles, img = None):
    if img is None:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            img = np.array(sct.grab(monitor))
    for (x, y, w, h) in rectangles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255,255), 2)
    cv2.imshow('img',img)
    cv2.waitKey(0)

def clickBtn(img,name=None, timeout=3, threshold = 0.7):
    if not name is None:
        pass
    start = time.time()
    while(True):
        matches = positions(img, threshold=threshold)
        if(len(matches)==0):
            hast_timed_out = time.time()-start > timeout
            if(hast_timed_out):
                if not name is None:
                    pass

                return False
            continue
        x,y,w,h = matches
        pos_click_x = x+w/2
        pos_click_y = y+h/2
        moveToWithRandomness(pos_click_x,pos_click_y)
        pyautogui.click()
        return True

def printSreen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))
        return sct_img[:,:,:3]

def positions(target, threshold=0.6, region=None):
    location = pyautogui.locateOnScreen(target, confidence=threshold, region=region)
    if location:
        x,y,w,h = location
        return (x, y, w, h)
    return []

def processLogin():
    dbg.console('Starting Login', 'INFO')
    sys.stdout.flush()
    loginSPG()
    playSPG()

def scroll(clickAndDragAmount):
    global timesScrolled
    global scrollChances
    flagScroll = positions(images['spg-flag-scroll'], 0.7)    
    if (len(flagScroll) > 0):
        x,y,w,h = flagScroll
        moveToWithRandomness(x,y)
        pyautogui.dragRel(0,clickAndDragAmount,duration=0.5, button='left')
        timesScrolled = timesScrolled + 1
        dbg.console('Searching available ships, chance: ' + str(scrollChances - timesScrolled), 'INFO')
        time.sleep(3)
    else:
        return


def loginSPG():
    global login_attempts    
    if login_attempts > 3:
        dbg.console('Too many login attempts, refreshing', 'CRITICAL')
        login_attempts = 0
        processLogin()
        return
    if clickBtn(images['connect-wallet'], name='connectWalletBtn', timeout = 10):
        dbg.console('Connect wallet button detected, logging in!', 'INFO')
        login_attempts = login_attempts + 1
    # if clickBtn(images['sign'], name='sign button', timeout=8):
    if clickBtn(images['assinar'], name='sign button', timeout=8):
        login_attempts = login_attempts + 1
        return
    if clickBtn(images['sign'], name='signBtn', timeout = 20):
        login_attempts = login_attempts + 1

def playSPG():
    if clickBtn(images['play'], name='okPlay', timeout=2):
        dbg.console('Starting game','INFO')

def login():
    if clickBtn(images['connect-wallet'], name='conectBtn', timeout=5):
        processLogin() 
        return True
    else:
        return False

# def isBossEight():
#     if(len(positions(images['boss-8-life'], threshold=0.9, region=(700, 180, 400, 100))) > 0):
#         dbg.console("Boss 8 found, starting over", 'INFO')
#         clickBtn(images['spg-surrender'])
#         clickBtn(images['confirm-surrender'])
#         return True
#     else: 
#         return False

def confirm():
    # isBossEight()
    confirm_action = False
    if clickBtn(images['confirm'], name='okBtn', timeout=1, threshold=0.9):
        dbg.console('Confirm encontrado','INFO')
        time.sleep(1) 
        endFight()  
        confirm_action = True
    if clickBtn(images['confirm-victory'], name='okVicBtn', timeout=1, threshold=0.6) or clickBtn(images['confirm-victory13'], name='okVicBtn', timeout=1, threshold=0.6) or clickBtn(images['confirm-victory14'], name='okVicBtn', timeout=1, threshold=0.6):
        dbg.console('Boss defeated!','INFO')
        confirm_action = True
        
    return confirm_action

def removeSpaceships():
    global ship_clicks
    time.sleep(0.5)
    ship_clicks = 0
    buttonRemove = positions(images['spg-x'], threshold=0.9)
    if screen_close():
        main()

    if len(buttonRemove) > 0:
        x,y,w,h = buttonRemove
        pos_click_x = x+w/2
        pos_click_y = y+h/2
        moveToWithRandomness(pos_click_x,pos_click_y)
        pyautogui.click()
        dbg.console("Removing spaceship", 'INFO')
        removeSpaceships()

def clickButtonsFight():
    global qtd_send_spaceships
    global ship_clicks
    global timesTried

    timesTried = timesTried + 1
    if timesTried > 10:
        main()

    buttonFight = positions(images['spg-go-fight'], 0.9)
    if(buttonFight):
        x,y,w,h = buttonFight
        moveToWithRandomness(x+(w/2),y+(h/2))
        pyautogui.click()
        dbg.console('Nave ' + str(ship_clicks + 1)+ ' selecionada', 'INFO')
        time.sleep(0.5)
        ship_clicks = ship_clicks + 1
        if ship_clicks >= qtd_send_spaceships:
            dbg.console('Team all set, starting fight!', 'INFO')
            time.sleep(1)
            goToFight()
        else:
            clickButtonsFight()
        return qtd_send_spaceships - ship_clicks
    else:
        if timesScrolled >= scrollChances:
            reloadSpaceship()
            refreshSpaceships(ship_clicks)
        else:
            scroll(-cda)
            clickButtonsFight()

def screen_close():
    if clickBtn(images['close']):
        dbg.console('Close found, restarting application.', 'CRITICAL')        
        return True
    else:
        return False

def reloadSpaceship():
    global timesScrolled
    timesScrolled = 0
    if len(positions(images['close'], 0.5)) > 0:
        if screen_close():
            main()
    elif len(positions(images['spg-base'], 0.7)) > 0:
        clickBtn(images['spg-base'], name='closeBtn', timeout=1)
        dbg.console('Going to base', 'INFO')
        time.sleep(3)
        clickBtn(images['spg-ship'], name='closeBtn', timeout=1)
        dbg.console('Going to ship lobby', 'INFO')
        time.sleep(3)        

def refreshSpaceships(qtd):
    global empty_qtd_spaceships
    global qtd_send_spaceships
    global ship_clicks
    global timesScrolled
    global timesTried

    dbg.console('Refreshing spaceship to Fight', 'INFO')
    timesTried = timesTried + 1
    if screen_close() or timesTried > 10:
        main()
    
    if qtd > 0:
        dbg.console('Ships ready to fight:' + str(ship_clicks), 'DEBUG')
        if ship_clicks == qtd_send_spaceships:
            time.sleep(2)
            goToFight()

    while timesScrolled <= scrollChances:
        clickButtonsFight()

    if ship_clicks == qtd_send_spaceships:
        empty_scrolls_attempts = 0
        time.sleep(2)
        goToFight()
    else:
        reloadSpaceship()
        refreshSpaceships(ship_clicks)
        
def goToFight():
    clickBtn(images['fight-boss'])
    time.sleep(2)
    clickBtn(images['confirm'])
    main(True)

def endFight():
    dbg.console("Ending fight", 'INFO')
    time.sleep(3) 
    goToSpaceShips()
    time.sleep(3) 
    if len(positions(images['spg-processing'], 0.9)) > 0:
        time.sleep(5) 
    if len(positions(images['fight-boss'], 0.9)) > 0:
        dbg.console('Checking spaceship in battle', 'INFO')
        removeSpaceships()
        time.sleep(1) 
        refreshSpaceships(0)
    else:
        pass

def goToSpaceShips():
    if clickBtn(images['ship']):
        global login_attempts
        login_attempts = 0

def fewShips():
    oneShipOnly = positions(images['1-15'], 0.9)
    twoShipsOnly = positions(images['2-15'], 0.9) 
    if(len(oneShipOnly) > 0 or len(twoShipsOnly) > 0):
        dbg.console('Few ships found in battle, going back to base', 'INFO')
        clickBtn(images['ship'])
        return True
    else:
        return False
                  

def main(started = False):
    global images    
    global login_attempts
    global timesTried
    login_attempts = 0
    images = load_images()

    timesTried = 0
    if started:
        dbg.console('Initiate attack.', 'INFO')
    else: 
        dbg.console('Bot started. Version: ' + str(VERSAO_SCRIPT), 'INFO')

    time_start = {
        "close" : 0,
        "login" : 0,
    }
    time_to_check = {
        "close" : 5,  
        "login" : 1,
    }

    while True:
        actual_time = time.time()

        action_found = False

        playSPG()
        # isBossEight()
        if actual_time - time_start["login"] > addRandomness(time_to_check['login'] * 1):
            sys.stdout.flush()
            time_start["login"] = actual_time
            if not login():
                if len(positions(images['fight-boss'], 0.9)) > 0:
                    dbg.console('Checking spaceship in battle', 'INFO')
                    removeSpaceships()
                    refreshSpaceships(0)
                    action_found = True
            else:
                action_found = True     

        if confirm():
            action_found = True 


        if fewShips():
            action_found = True       
        
        if actual_time - time_start["close"] > time_to_check['close']:
            time_start["close"] = actual_time
            if screen_close():
                action_found = True

        if action_found == False:
            dbg.console('No action found!', 'WARNING')

if __name__ == '__main__':
    main()