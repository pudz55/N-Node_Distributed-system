from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import threading
import random
from jsonrpclib import Server
from Vectorclock import Vectorclock

deviceZVector = [0,0,0]

#This thread listen to Messages
def listenToTheMessages(incomingvector):
    global deviceZVector
    print("Vector clock Before device Z Receiving a Message")
    print(deviceZVector)
    #Maximum of two vectors are taken elementwise 
    deviceZVector  = list(map(max, zip(deviceZVector, incomingvector)))
    deviceZVector[2]=deviceZVector[2]+1
    print("Vector clock After device Z Receiving a Message")
    print(deviceZVector)
    
#This thread sends message to devices
def sendMessageToTheServer():
    deviceX = Server('http://localhost:8873')
    deviceY = Server('http://localhost:8874')
    while True:
        device = int(input("Enter Device Number to send a Message"))
        if device == 3: ## If Internal Event happens my method is called
            listenToTheMessages(deviceZVector)
        if device == 1: ## Send Message to Device X
            print("Vector clock Before device Z Sending a Message")
            print(deviceZVector)
            deviceZVector[2]=deviceZVector[2]+1
            deviceX.listenToTheMessages(deviceZVector)
            print("Vector clock After device Z Sending a Message")
            print(deviceZVector)

        if device == 2:  ##Send Message to Device Y
            print("Vector clock Before device Z Sending a Message")
            print(deviceZVector)
            deviceZVector[2]=deviceZVector[2]+1
            deviceY.listenToTheMessages(deviceZVector)
            print("Vector clock After device Z Sending a Message")
            print(deviceZVector)

#Creating the RPC Server for the Device Z
deviceZ = SimpleJSONRPCServer(('localhost', 8875))
th1 = threading.Thread(target=sendMessageToTheServer, args=())
th1.start()
deviceZ.register_function(listenToTheMessages)
print("device Z is Up and Running")
#calling vectorclock class
clock = Vectorclock() 
deviceZVector[0] = clock.getDeviceXTime()
deviceZVector[1] = clock.getDeviceYTime()
deviceZVector[2] = clock.getDeviceZTime()
print("Device Z's Current Vector is: ",deviceZVector)
deviceZ.serve_forever()
