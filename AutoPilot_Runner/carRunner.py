import argparse
import socketio
import cv2 as cv
import numpy as np
import keras as ks
from copy import deepcopy
from time import time
from threading import Thread
import sys

import urllib 

mask = None
sio = None
steering = 90

def main():
    printBanner()
    args = parseArgs()
    printConfig(args)
    global sio
    sio = tryConnect(args.ip_address)


    predictionThread = Thread(target=predictSteering, args=(sio, args.neural_network_file,), daemon=True)
    predictionThread.start()

    addControls()
    captureVideo(args.ip_address)

def captureVideo(ip):
    fps = 0
    new_frame_time = 2
    prev_frame_time = 1
    global mask 
    try:
        stream = urllib.request.urlopen('http://192.168.0.10:8080/stream')
    except:
        print("Error displaying frame")
        print("Have you connected to the PiCar?")
        print("Is %s the correct ip address?" % ip)
        exit()

    bytes = b''

    while 1:     
        new_frame_time = time()
        bytes += stream.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]
            frame = cv.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv.IMREAD_COLOR)
            mask = imageProcessing(frame)
            cv.putText(frame, "FPS:" + str(round(fps, ndigits=2)), (50,50), cv.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255))
            cv.imshow("PiCar Video", frame)
            cv.imshow("PiCar Mask", mask)
            sio.emit("steer", steering)
            if cv.waitKey(1) == 27:
                exit(0) 

        
        #we calculate the fps
        fps = lerp(fps, safe_div(1,(new_frame_time - prev_frame_time)), 0.001)
        prev_frame_time = new_frame_time
        

def safe_div(x,y):
    if y==0: return 0
    return x/y


def lerp(a, b, t):
    return a + (b - a) * t

def predictSteering(sio, model_name):
    global steering
    print("Loading Neural Network")
    model = ks.models.load_model(model_name)
    while 1:

        maskref = deepcopy(mask)

            # check dsize of mask
        try:
            maskref = cv.resize(maskref, (100, 66))
            maskref = np.array(maskref)
            maskref = np.expand_dims(maskref, axis=2)
            maskref = np.expand_dims(maskref, axis=0)
            steering = float(model(maskref)[0][0])
            sys.stdout.write("\rSent steering value: %s      " % round(steering, 2))
            sys.stdout.flush()
        except:
            # print the exeption 
            print(sys.exc_info()[0])
            print("Prediction Error")
            continue

def imageProcessing(frame):
    # we get the trackbar values
    hl = cv.getTrackbarPos('Hue Lower', 'Controls')
    sl = cv.getTrackbarPos('Sat Lower', 'Controls')
    vl = cv.getTrackbarPos('Val Lower', 'Controls')
    hu = cv.getTrackbarPos('Hue Upper', 'Controls')
    su = cv.getTrackbarPos('Sat Upper', 'Controls')
    vu = cv.getTrackbarPos('Val Upper', 'Controls')
    # we convert the frame to the HSV color space
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # blur the image to remove noise
    blur = cv.GaussianBlur(hsv, (5, 5), 0)
    ## mask the image to get only the desired colors
    mask = cv.inRange(blur, (hl, sl, vl), (hu, su, vu))
    ## we erode and dilate to remove noise
    erode = cv.erode(mask, np.ones((5, 5), np.uint8), iterations=1)
    dilate = cv.dilate(erode, np.ones((5, 5), np.uint8), iterations=1)
    # we smooth the image with some gaussian blur
    blur = cv.GaussianBlur(dilate, (5, 5), 0)

    return blur

def null(x):
    pass

def updateSpeed(x):
    sio.emit("drive", x)

def addControls():
    # create cv2 window
    cv.namedWindow('Controls', cv.WINDOW_NORMAL)
    cv.resizeWindow('Controls', 300, 300)
    cv.createTrackbar('Hue Lower', 'Controls', 40, 255, null)
    cv.createTrackbar('Sat Lower', 'Controls', 25, 255, null) 
    cv.createTrackbar('Val Lower', 'Controls', 73, 255, null)

    cv.createTrackbar('Hue Upper', 'Controls', 93, 255, null)
    cv.createTrackbar('Sat Upper', 'Controls', 194, 255, null)
    cv.createTrackbar('Val Upper', 'Controls', 245, 255, null)

    cv.createTrackbar('Speed', 'Controls', 0, 100, updateSpeed)
def printInfo(cap, ip):
    print("----------------------------- Car Information ----------------------------")
    print("Camera FPS:", cap.get(cv.CAP_PROP_FPS))
    print("Camera width:", cap.get(cv.CAP_PROP_FRAME_WIDTH))
    print("Camera height:", cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    print("--------------------------------------------------------------------------")
    print("Capturing video from {}".format(ip))
    print("Press 'q' to quit")
    print("----------------------------- Sending Commands ---------------------------")

def tryConnect(ip):
    # we try to connect to the PiCar
    sio = socketio.Client()
    try:
        sio.connect('http://%s:3000' % ip)
    # if we fail we print out an error message and exit the program
    except:
        print("Failed to connect to PiCar Socket Error")
        print("Check that your laptop is connected to the PiCar network")
        exit()
    return sio

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--neural_network_file', type=str, default='model.h5', required=False, help='Neural network file name')
    parser.add_argument('-i', '--ip_address', type=str, default="192.168.0.10", required=False, help='Car ip address')
    parser.add_argument('-s', '--speed', type=int, default=50, required=False, help='Car speed value from 0 to 100')
    return parser.parse_args()

def printConfig(args):
    print("--------------------------------- Config ---------------------------------")
    print("Neural network file name: {}".format(args.neural_network_file))
    print("Car ip address: {}".format(args.ip_address))
    print("Car speed: {}".format(args.speed))
    print("--------------------------------------------------------------------------")

def printBanner():
    # print raw string
    print(r"""
       ____ ___ ____             ____                              
      |  _ \_ _/ ___|__ _ _ __  |  _ \ _   _ _ __  _ __   ___ _ __ 
      | |_) | | |   / _` | '__| | |_) | | | | '_ \| '_ \ / _ \ '__|
      |  __/| | |__| (_| | |    |  _ <| |_| | | | | | | |  __/ |   
      |_|  |___\____\__,_|_|    |_| \_\\__,_|_| |_|_| |_|\___|_|   
      ______________________________________________________________                                                         
""")

if __name__ == '__main__':
    main()
