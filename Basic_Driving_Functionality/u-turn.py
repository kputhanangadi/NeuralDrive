import socketio 
import time

# create a socketio object
# socketio is a module that allows us to easily use websockets.
# Websockets are a protocol that allows two programs to communicate with each other in real time
# Over the internet. 
sio = socketio.Client()

# try to connect to the PiCar
try:
    sio.connect('http://192.168.0.10:3000')
    
# print out an error message and exit the program
except:
    print("Failed to connect to PiCar")
    print("Check that your laptop is connected to the PiCar network")
    exit()

# point wheels forward 
sio.emit('steer', 90)
time.sleep(2)
# drive forwards
sio.emit('drive', 50)
time.sleep(5)
sio.emit('drive', 0)

# point wheels forward
sio.emit('steer', 90)
time.sleep(2)
# point wheels left and drive to 
# do a u-turn
sio.emit('steer', 20)
sio.emit('drive', 50)
time.sleep(3)
# stop and reposition the wheels
sio.emit('drive', 0)
sio.emit('steer', 90)

# drive back to the start point 
sio.emit('drive', 50)
time.sleep(5)
sio.emit('drive', 0)
