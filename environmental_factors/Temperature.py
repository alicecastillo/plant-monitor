# Created by: Alice Castillo

# Description:

from . import PlantResource


class Temperature(PlantResource):
    def __init__(self, name: str, subject: int):
        super().__init__(name, subject)

    def getReading(self, reading):
        pass

    def evaluate(self):
        pass

    def exportData(self):
        pass
