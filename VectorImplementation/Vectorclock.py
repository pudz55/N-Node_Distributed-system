import random


class Vectorclock:
    def getDeviceXTime(self):
        self.deviceXTime = random.randint(1, 15)
        return self.deviceXTime

    def getDeviceYTime(self):
        self.deviceYTime = random.randint(1, 15)
        return self.deviceYTime

    def getDeviceZTime(self):
        self.deviceZTime = random.randint(1, 15)
        return self.deviceZTime