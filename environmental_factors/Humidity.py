# For applications in “extreme” areas (0-20% or 80-100% humidity),
# the DHT22 should be used, as it also supports these areas in contrast to the DHT11

# Created by: Alice Castillo

# Description:



class Humidity(environmental_factors.PlantResource):
    def __init__(self, name: str, subject: int):
        super().__init__(name, subject)

    def getReading(self, reading):
        pass

    def evaluate(self):
        pass

    def exportData(self):
        pass
