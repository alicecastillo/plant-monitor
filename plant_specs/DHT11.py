# Created by: Alice Castillo

# Description:

# sys lib
import time

# venv lib
import board
import adafruit_dht

# Local base class import
from plant_specs.Sensor import Sensor

class DHT11(Sensor):
    def __init__(self, cur_time: int):
        super().__init__(cur_time, 2)
        self.sensor = adafruit_dht.DHT11(board.D4, use_pulseio=False)

    def convertToF(self, c) -> float:
        return c * (9 / 5) + 32

    def runSensor(self, sec: int):
        if self.readyToRead(sec):
            try:
                temp_f = self.convertToF(self.sensor.temperature)
                humidity = self.sensor.humidity

            except RuntimeError as er:
                print(er.args[0])
                return

            except Exception as e:
                self.releaseSensor()
                raise e
