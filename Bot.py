import time
import threading
import mouse
from ultralytics import YOLO
import pyautogui as pg

target = "goldencookie"

# Load YOLO model
model = YOLO("best.pt")


def coords_maker(boxes)->list:
    coords = []

    for box in boxes:
        print(f"Box: {box}\n")

        xmin, ymin, xmax, ymax = box
        
        if (xmin+xmax)/2 < 163 or (xmin+xmax)/2 > 2007: ## checks to see if its not a big cookie, throws out coordinates
            del xmin, ymin, xmax, ymax
        else:    
            for num in xmin, ymin, xmax, ymax:
                coords.append(int(num))

    print(f"Coords: {coords}\n")
    
    return coords


def clicker():
    while True:
        pg.moveTo(388, 757)
        mouse.click('left')

def screenshot_predict_click():

    screenshot = pg.screenshot()

    results = model.predict(source=screenshot, conf=0.5)

    names = results[0].names ## dictionary, 2 categories
    names = names.values()
    boxes = results[0].boxes.xyxy.tolist() ## box coordinate lists within one list

    coords = coords_maker(boxes)
        
    for i in range(0, len(coords), 4): ## step by 4 to access pairs of 4
        xmin, ymin, xmax, ymax = coords[i], coords[i+1], coords[i+2], coords[i+3] ## correct xyxy order
        x_center = int((xmin+xmax)/2)
        y_center = int((ymin+ymax)/2)            
        print(f"Obj center coords: {x_center}, {y_center}")

        ## click
        pg.leftClick(x_center, y_center)

t1 = threading.Thread(target=clicker, daemon=True)  ## this clicker daemon thread will stop when I ctrlC screenshot_predict_click (main thread)
t1.start()

# ## code in try block is "selected" for error handling, except block handles the error without raising a python error
try:
    while True:
        screenshot_predict_click()
        time.sleep(10)
except KeyboardInterrupt:
    pass

