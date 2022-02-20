import pyautogui
import time

# pyautogui.displayMousePosition()
# image = pyautogui.screenshot(region=(700, 180, 400, 100))
# image.save("./teste.png")
while True:
    location = pyautogui.locateOnScreen('images/boss-8-life.png', confidence=0.9)
    if location:
        x,y,w,h = location
        print(x,y,w,h)
    else:
        print([])
    time.sleep(1)
