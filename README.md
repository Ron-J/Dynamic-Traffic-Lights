# Dynamic-Traffic-Lights
Smart traffic light system
Project using OpenCV, YOLOV4 / YOLOV5 ML Model

Components used:
•	Computer for processing real time pictures
•	Arduino board for transmitting Computer output to Traffic Lights
•	Webcam
Modules Used:
•	OpenCV – For image processing
•	numpy – For image processing
•	time -For periodic traffic lights control
•	PyFrimata – For Arduino communication on Ethernet cabel
Code Description:

1. Using YOLOV4
The main function in this is signal() which captures the image processes the image by calling CountCars() and activates the required Arduino pins. It is made to function for 300s (1min) and has 20sec delay between each image capture using time.sleep(<>) function. It uses PyFirmata module to communicate with the Arduino board which already has been flashed with ‘Standard Frimata’ from the example library in Arduino IDE. 
The function CountCars() uses the detect_vehicles() function from vehicle_detector.py to return the “boxes” (list of ‘[the bottom left x,y co-ordinates height, width]) and then  separates the image given as argument into the vertical segment of the road and the horizontal segment of the road and finds how many cars lie in each segment.  It at the same time rectangles the cars using cv2.rectangle() function and displays the boxed whole image, as well as the boxed vertical and horizontal segments with the number of cars detected in the image for user understanding.

vehicle_detector.py uses a pretrained model which is contained in ‘yolov4.weights’ file. 

2. YOLOV5 MODEL
The code working is same except for the vehicle detection model which is present inside the same code instead of in 2 different ones. The information returned is also in different formats instead of (x,y,h,w) as in the first one.  It is also possible with little prior experience to train a YOLO model using roboflow tool and tutorials for it for customised detection 
