import cv2 as cv 

# create a variable called ip to store the ip address of the PiCar
ip = "192.168.0.10"

# create a VideoCapture object and tell it to use the ip address of the PiCar
# as well we use the %s format to insert the ip address into the string
cap = cv.VideoCapture("http://%s:8080/?action=stream" % ip)


while True:
    # get the next frame from the video stored in frame
    # ret is a boolean that tells us if the frame was successfully retrieved
    # ret is short for return
    ret, frame = cap.read()
    
    # display the frame
    cv.imshow("PiCar Video", frame)
    
    # convert the frame to the HSV color space
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    # can change the ranges to find other colors
    mask = cv.inRange(hsv, (40, 50, 90), (100, 255, 220))
    
    # display the mask
    cv.imshow("Mask", mask)
    
    # use the waitKey function to wait for a key press
    # if the key is q then we break out of the loop
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
