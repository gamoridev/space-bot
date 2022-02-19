import pyautogui
import time

# pyautogui.displayMousePosition()
while True:
    location = pyautogui.locateOnScreen('images/play.png', confidence=0.6)
    if location:
        x,y,w,h = location
        print(x,y,w,h)
    else:
        print([])
    time.sleep(1)
