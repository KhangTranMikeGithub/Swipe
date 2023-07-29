import cv2
import mediapipe as mp
import handle
from tkinter import *
import time
import app
import sys

threshX = 30
threshY = 40
first = True
op = True

swiped = ['none', False]
count = 0
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
root = Tk()
mainApp = app.PDFViewer(root)
frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
centerX = int(frame_width / 2)
centerY = int(frame_height / 2)

def close():
    global op
    op = False
    root.destroy()
    cap.release()
    cv2.destroyAllWindows()
    sys.exit()
root.protocol("WM_DELETE_WINDOW", close)

while True and op == True:
    success, image = cap.read()
    if success:
        image = cv2.flip(image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        index_5 = 0
        index_8 = 0
        y5 = 0
        y8 = 0
        Fx = 0
        han = []
        if results.multi_hand_landmarks != None:
            bruh=0
            i = 0
            r = results.multi_hand_landmarks
            ra = results.multi_handedness
            for i in ra:
                handType=i.classification[0].label
                han.append(handType)
            if 'Right' in han:
                for id, lm in enumerate(r[han.index('Right')].landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if id == 5 :
                        index_5 = cx
                        y5 = cy
                
                    if id == 8 :
                        index_8 = cx
                        y8 = cy
                        Fx = cx
                straightX = abs(index_8 - index_5) < threshX
                straightY = abs(y8 - y5) > threshY
                if straightX == True and straightY == True and swiped == ['none', False] and count < 40:
                    if first == True:
                        obj = handle.Handle(Fx)
                        first = False
                    else:
                        swiped = obj.checkSwipe(Fx)
                    count += 1
                else:
                    if swiped == ['right', True]:
                        mainApp.next_page()
                        root.update()
                        time.sleep(0.3)
                    elif swiped == ['left', True]:
                        mainApp.previous_page()
                        root.update()
                        time.sleep(0.3)
                    first = True
                    swiped = ['none', False]
                    count = 0
        mainApp.showCanvas(success, image)
        root.update()