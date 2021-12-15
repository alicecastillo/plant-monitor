# Created by: Alice Castillo

# Description: Generic base class for any resource.


class PlantResource():
    def __init__(self, name: str, subject: int):
        self.name = name
        self.subject = subject
        self.readings = []

    def getReading(self, reading):
        pass

    def evaluate(self):
        pass

    def exportData(self):
        pass
