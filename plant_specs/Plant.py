# Created by: Alice Castillo

# Description: Generic base class for any plant.
import json
import os
import time
from datetime import datetime

# Import sensor classes
from plant_specs.VEML6070 import VEML6070
from plant_specs.DHT11 import DHT11


class Plant():
    def __init__(self, num: int, reqs: list = []):
        self.loadData(num)
        self.num = num
        self.species = ""
        self.last_ht_check, self.last_uv_check, self.last_water = 0, 0, 0

    def loadData(self, num: int):
        # get subject file
        sub_json = self.readJSONFile("plant_specs/current_subjects/subject_{0}.json".format(num))
        self.last_ht_check = sub_json["last_ht_check"]
        self.last_uv_check = sub_json["last_uv_check"]
        self.last_water = sub_json["last_water"]
        self.species = sub_json["species"]

        # get species file
        # species_json = self.readJSONFile("plant_specs/species/{0}.json".format(sub_json["species_filename"]))
        # self.reqs = species_json["requirements"]

    def checkResources(self):
        # -    Water moisture and temperature 2x / hr, 24 x 1 day
        # -    Sunlight logging 4 x / hr DURING DAYLIGHT
        pass

    def writeUpdate(self):
        pass

    def readJSONFile(self, path):
        f = open(os.path.join(os.getcwd(), path), "r")
        return json.load(f)

    def getReadings(self, cur_time: int) -> None:
        sensors = [VEML6070(cur_time)]
        cur_min = int(datetime.fromtimestamp(cur_time).strftime("%M"))
        if cur_min%30:
            sensors.append(DHT11(cur_time))
        for i in range(60):
            for sensor in sensors:
                sensor.runSensor(i)
            time.sleep(1)


    def writeLogs(self):
        pass