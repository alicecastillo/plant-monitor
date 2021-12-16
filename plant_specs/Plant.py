# Created by: Alice Castillo

# Description: Generic base class for any plant.
import json
import os

class Plant():
    def __init__(self, num: int, reqs: list = []):
        self.loadData(num)
        self.num = num
        self.species = ""
        self.reqs = []

    def loadData(self, num: int):
        # get subject file
        sub_json = self.readJSONFile("plant_specs/current_subjects/subject_{0}.json".format(num))
        self.species = sub_json["species"]

        # get species file
        species_json = self.readJSONFile("plant_specs/species/{0}.json".format(sub_json["species_filename"]))
        self.reqs = species_json["requirements"]

    def checkResources(self):
        # -    Water moisture and temperature 2x / hr, 24 x 1 day
        # -    Sunlight logging 4 x / hr DURING DAYLIGHT
        pass

    def writeUpdate(self):
        pass

    def readJSONFile(self, path):
        f = open(os.path.join(os.getcwd(), path), "r")
        return json.load(f)

    def getReadings(self, cur_time: int):

        pass


    def writeLogs(self):
        pass