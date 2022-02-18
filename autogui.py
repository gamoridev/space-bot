import pyautogui
import time

# pyautogui.displayMousePosition()
while True:
    location = pyautogui.locateOnScreen('img_compare/boss-8.png', confidence=0.6)
    if location:
        x,y,w,h = location
        print(x,y,w,h)
    else:
        print([])
    time.sleep(1)
