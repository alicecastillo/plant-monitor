# Created by: Alice Castillo

# Description: Generic base class for any plant.
import json
import os

class Sensor():
    def __init__(self, cur_time: int, sleep_interval: int):
        self.cur_time = cur_time
        self.sleep_interval = sleep_interval

        # non init
        self.logs, self.sensor, self.log_file = None, None, ""

    def runSensor(self, sec: int):
        pass

    def returnResults(self) -> tuple:
        return self.log_file

    def getSleepInterval(self):
        return self.sleep_interval

    def readyToRead(self, sec):
#         if not sec%self.sleep_interval:
#             print("Ready to run at {0}".format(sec))
        return not sec%self.sleep_interval

    def releaseSensor(self):
        if self.sensor:
            self.sensor.exit()
