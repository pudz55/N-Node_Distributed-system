from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import threading
import random
from jsonrpclib import Server
from Vectorclock import Vectorclock
deviceXVector = [0,0,0] 

#This thread listen to Messages
def listenToTheMessages(incomingvector):
    global deviceXVector
    print("Vector clock Before device X Receiving a Message")
    print(deviceXVector)
    #Maximum of two vectors are taken elementwise 
    deviceXVector  = list(map(max, zip(deviceXVector, incomingvector)))
    deviceXVector[0]=deviceXVector[0]+1
    print("Vector clock After device X Receiving a Message")
    print(deviceXVector)
    
#This thread sends message to devices
def sendMessageToTheServer():
    deviceY = Server('http://localhost:8874')
    deviceZ = Server('http://localhost:8875')
    while True:
        device = int(input("Enter Device Number to send a Message"))
        if device == 1: ## If Internal Event happens my method is called
            listenToTheMessages(deviceXVector)
        if device == 2: ## Send Message to Device Y
            print("Vector clock Before device X Sending a Message")
            print(deviceXVector)
            deviceXVector[0]=deviceXVector[0]+1
            deviceY.listenToTheMessages(deviceXVector)
            print("Vector clock After device X Sending a Message")
            print(deviceXVector)

        if device == 3:  ##Send Message to Device Z
            print("Vector clock Before device X Sending a Message")
            print(deviceXVector)
            deviceXVector[0]=deviceXVector[0]+1
            deviceZ.listenToTheMessages(deviceXVector)
            print("Vector clock After device X Sending a Message")
            print(deviceXVector)


#Creating the RPC Server for the Device X
localhost = '127.0.0.1'
deviceX = SimpleJSONRPCServer(('localhost', 8873))
th1 = threading.Thread(target=sendMessageToTheServer, args=())
th1.start()
deviceX.register_function(listenToTheMessages)
print("device X is Up and Running")
#calling vectorclock class
clock = Vectorclock() 
deviceXVector[0] = clock.getDeviceXTime()
deviceXVector[1] = clock.getDeviceYTime()
deviceXVector[2] = clock.getDeviceZTime()
print("Device X's Current Vector is: ",deviceXVector)
deviceX.serve_forever()



