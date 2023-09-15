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

# the center of the steering for my car is 78 degrees yours may be different
center = 96

sio.emit('steer', center)
sio.emit('drive', 50)
time.sleep(7.1)
sio.emit('drive', 0)

sio.emit('steer', 20)
sio.emit('drive', 50)
time.sleep(1.2)
sio.emit('drive', 0)


#time.sleep(0.5)
sio.emit('drive', -50)
sio.emit('steer', 128)
time.sleep(1.2)
sio.emit('drive', 0)

#time.sleep(0.5)
sio.emit('drive', 50)
sio.emit('steer', 20)
time.sleep(1)

sio.emit('steer', center)
sio.emit('drive', 0)

sio.emit('steer', center)
sio.emit('drive', 50)
time.sleep(7.1)
sio.emit('drive', 0)

time.sleep(2)
