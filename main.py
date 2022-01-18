import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import cvzone

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)
colorR= (255 ,0 ,255)

cx, cy, w, h = 100,100 , 200 ,200
class DragRec():
    def __init__(self, posCenter, size=[200,200]):
        self.posCenter = posCenter
        self.size = size
    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            self.posCenter = cursor






recList =[]
for i in range(5):
    recList.append(DragRec([i*250+150, 150]))
while True:
    succes, img= cap.read()
    img = cv2.flip(img , 1)
    img = detector.findHands(img)
    lmlist, _ = detector.findPosition(img)
    if lmlist:
        l, _, _ = detector.findDistance(8, 12, img, draw=False)
        print(l)


        if l <30:

            cursor = lmlist[8]
            for rec in recList:
                rec.update(cursor)

#to make solid shapes
    #for rec in recList:
     #   cx, cy = rec.posCenter
      #  w, h = rec.size
       # cv2.rectangle(img, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), colorR, cv2.FILLED)
        #cvzone.cornerRect(img, (cx-w//2, cy-h//2, w, h), 20, rt=0)
    imgNew = np.zeros_like(img, np.uint8)
    for rec in recList:
       cx, cy = rec.posCenter
       w, h = rec.size
       cv2.rectangle(imgNew, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), colorR, cv2.FILLED)
       cvzone.cornerRect(imgNew, (cx-w//2, cy-h//2, w, h), 20, rt=0)
    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask]=cv2.addWeighted(img , alpha, imgNew, 1-alpha, 0)[mask]


    cv2.imshow("Image", out)
    cv2.waitKey(1)