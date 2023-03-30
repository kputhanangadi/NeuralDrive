# we create a while loop to get and display the video
while True:
    # we get the next frame from the video stored in frame
    # ret is a boolean that tells us if the frame was successfully retrieved
    # ret is short for return
    ret, frame = cap.read()
    # we display the frame
    cv.imshow("PiCar Video", frame)
    # now we convert the frame to the HSV color space
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # I found that these ranges work well for green
    # However you can change the ranges to find other colors
   
    redmask = cv.inRange(hsv, (-30, 50, 100), (30, 255, 300))

    bluemask = cv.inRange(hsv, (105, 50, 60), (185, 255, 300))

    greenmask = cv.inRange(hsv, (40, 50, 70), (100, 255, 300))

    # now we display the mask
    cv.imshow("RedMask", redmask)
    # now we display the mask
    cv.imshow("Bluemask", bluemask)
    # now we display the mask
    cv.imshow("GreenMask", greenmask)

    
    # we use the waitKey function to wait for a key press
    # if the key is q then we break out of the loop
    if cv.waitKey(1) & 0xFF == ord('q'):
        break