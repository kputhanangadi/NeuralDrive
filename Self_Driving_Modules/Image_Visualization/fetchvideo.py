# first we import OpenCV 
import cv2 as cv 

# we create a variable called ip to store the ip address of the PiCar
ip = "192.168.0.10"
# we create a VideoCapture object and tell it to use the ip address of the PiCar
# as well we use the %s format to insert the ip address into the string
cap = cv.VideoCapture("http://%s:8080/?action=stream" % ip)

# we create a while loop to get and display the video
while True:
    # we get the next frame from the video stored in frame
    # ret is a boolean that tells us if the frame was successfully retrieved
    # ret is short for return
    ret, frame = cap.read()
    # we display the frame
    cv.imshow("PiCar Video", frame)
    # we use the waitKey function to wait for a key press
    # if the key is q then we break out of the loop
    if cv.waitKey(1) & 0xFF == ord('q'):
        break