from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import threading
import random
from jsonrpclib import Server
from Vectorclock import Vectorclock

deviceYVector = [0,0,0] 

#This thread listen to Messages
def listenToTheMessages(incomingvector):
    global deviceYVector
    print("Vector clock Before device Y Receiving a Message")
    print(deviceYVector)
    #Maximum of two vectors are taken elementwise 
    deviceYVector  = list(map(max, zip(deviceYVector, incomingvector)))
    deviceYVector[1]=deviceYVector[1]+1
    print("Vector clock After device Y Receiving a Message")
    print(deviceYVector)
    
#This thread sends message to devices
def sendMessageToTheServer():
    deviceX = Server('http://localhost:8873')
    deviceZ = Server('http://localhost:8875')
    while True:
        device = int(input("Enter Device Number to send a Message"))
        if device == 2: ## If Internal Event happens my method is called
            listenToTheMessages(deviceYVector)
        if device == 1: ## Send Message to Device X
            print("Vector clock Before device Y Sending a Message")
            print(deviceYVector)
            deviceYVector[1]=deviceYVector[1]+1
            deviceX.listenToTheMessages(deviceYVector)
            print("Vector clock After device Y Sending a Message")
            print(deviceYVector)

        if device == 3:  ##Send Message to Device Z
            print("Vector clock Before device Y Sending a Message")
            print(deviceYVector)
            deviceYVector[1]=deviceYVector[1]+1
            deviceZ.listenToTheMessages(deviceYVector)
            print("Vector clock After device Y Sending a Message")
            print(deviceYVector)

#Creating the RPC Server for the Device Y
localhost = '127.0.0.1'
deviceY = SimpleJSONRPCServer(('localhost', 8874))
th1 = threading.Thread(target=sendMessageToTheServer, args=())
th1.start()
deviceY.register_function(listenToTheMessages)
print("device Y is Up and Running")
#calling vectorclock class
clock = Vectorclock() 
deviceYVector[0] = clock.getDeviceXTime()
deviceYVector[1] = clock.getDeviceYTime()
deviceYVector[2] = clock.getDeviceZTime()
print("Device Y's Current Vector is: ",deviceYVector)
deviceY.serve_forever()





