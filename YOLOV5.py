import time
import cv2
import numpy as np

import yolov5

model = yolov5.load("yolov5_model.pt")
#These values can be tested and modified to get optmimal accurate recognition result
# set model parameters
model.conf = 0.4  # NMS confidence threshold
model.iou = 0.3  # NMS IoU threshold
#model.agnostic = False  # NMS class-agnostic
#model.multi_label = False  # NMS multiple labels per box
model.max_det = 7  # maximum number of detections per image

from pyfirmata import Arduino, util

board=Arduino('COM3')
iterator=util.Iterator(board)
iterator.start()

def CountCars(img):
     vehicle_count_vertical=vehicle_count_horizontal=0

     results = model(img)

     results = model(img, size=1280)

     results = model(img, augment=True)
     boxes = results.xywh[0] # x1, y1, x2, y2

     vehicle_count_total=len(boxes)
     
     vertical=img[0:599,250:450]#[0:599,207:400]
     horizontal=img[155:260,0:799] #[300:370,0:799]
     #cv2.rectangle(img,(20,30),(70,90),(25,0,180),3)
     n=0
     prediction=results.pred[0][:,:4]
     for box in boxes:
         x, y, w, h, dummy1, dummy2 = box
         x1,y1,x2,y2=prediction[n]
         cv2.rectangle(img, (int(x1),int(y1)), (int(x2),int(y2)), (25, 0, 180), 3)

         if 250<x<450 and 0<y<599:
              vehicle_count_vertical+=1
         else:#if 155<y<260 and 0<x<799:
              vehicle_count_horizontal+=1
         n=n+1

     imgo=cv2.putText(img, "Vehicles: " + str(vehicle_count_total), (20, 50), 0, 1, (100, 200, 0), 3).copy()
     vertical=cv2.putText(vertical, "Vehicles: " + str(vehicle_count_vertical), (20, 50), 0, 1, (100, 200, 0), 3)
     horizontal=cv2.putText(horizontal,"Vehicles: " + str(vehicle_count_horizontal), (20, 50), 0, 1, (100, 200, 0), 3)

     cv2.imshow('Captured Image', imgo)
     cv2.waitKey(1)
     cv2.imshow('Vertical',vertical)
     cv2.waitKey(1)
     cv2.imshow('Horizontal',horizontal)
     
     cv2.waitKey(1)
     return vehicle_count_vertical,vehicle_count_horizontal
def signal():#Returns 1 if more vehicles vertically
     global signal
     timeinitial=timenow=time.time()                #0 if more vehicles horizontally  
     webcam=cv2.VideoCapture(0)        #Starts continuously capturing video
     while timenow<timeinitial+300:    #Runs for 300 seconds
         check,frame=webcam.read()                       
         #cv2.imshow('Captured Image',frame)
         cv2.waitKey(1)

         t=CountCars(frame)

         if t[0]>t[1]:
            board.digital[2].write(1)
            board.digital[3].write(0)
         else:
            board.digital[3].write(1)
            board.digital[2].write(0)

         time.sleep(20)

signal()
