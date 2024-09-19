import cv2
import numpy as np
import time

from vehicle_detector import VehicleDetector
vd = VehicleDetector()
     
from pyfirmata import Arduino, util

board=Arduino('COM3')
iterator=util.Iterator(board)
iterator.start()

def CountCars(img):

     vehicle_boxes = vd.detect_vehicles(img)
     vehicle_count_total = len(vehicle_boxes)
     vehicle_count_vertical=0
     vehicle_count_horizontal=0
     #This sectioning has to be modified based on camera positioning to get vertical segment and horizontal segment of the road. 
     vertical=img[0:599,310:500]
     horizontal=img[155:260,0:799] 


     for box in vehicle_boxes:
         x, y, w, h = box

         cv2.rectangle(img, (x, y), (x +w, y +h), (25, 0, 180), 3)

         if 207<x<400 and 0<y<599:
              vehicle_count_vertical+=1
         else:
              vehicle_count_horizontal+=1

     imgo=cv2.putText(img, "Vehicles: " + str(vehicle_count_total), (20, 50), 0, 1, (100, 200, 0), 3).copy()
     vertical=cv2.putText(vertical, "Vehicles: " + str(vehicle_count_vertical), (20, 50), 0, 1, (100, 200, 0), 3)
     horizontal=cv2.putText(horizontal,"Vehicles: " + str(vehicle_count_horizontal), (20, 50), 0, 1, (100, 200, 0), 3)

     cv2.imshow('Captured Image', imgo)
     cv2.imshow('Vertical',vertical)
     cv2.imshow('Horizontal',horizontal)
     
     cv2.waitKey(1)
     return vehicle_count_vertical,vehicle_count_horizontal
def signal():#Returns 1 if more vehicles vertically
     global signal
     timeinitial=timenow=time.time()                #0 if more vehicles horizontally  
     webcam=cv2.VideoCapture(0)        #Starts continuously capturing video
     while timenow<timeinitial+300:    #Runs for 300 seconds
         check,frame=webcam.read()                       
         cv2.imshow('Captured Image',frame)
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




