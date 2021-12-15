# Created by: Alice Castillo

# Description: Generic base class for any plant.
import json

class Plant():
    def __init__(self, num: int, reqs: list = []):
        self.getData(num)
        self.num = num
        self.name = ""
        self.reqs = []

    def loadData(self, num: int):
        f = open("current_subjects/subject_{0}.json".format(num), "r")
        f_json = json.load(f)
        self.name = f_json["name"]
        self.reqs = f_json["requirements"]

    def checkResources(self):
        # -    Water moisture and temperature 2x / hr, 24 x 1 day
        # -    Sunlight logging 4 x / hr DURING DAYLIGHT
        pass

    def writeUpdate(self):
        pass
