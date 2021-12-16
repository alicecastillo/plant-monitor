# Created by: Alice Castillo

# Description: Specific to the Inland DHT11 sensor.

# sys lib
import time

# venv lib
import board
import adafruit_dht
import pandas as pd
from openpyxl import Workbook, load_workbook

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
                print("At {0}, H {1} and T {2}".format(sec, temp_f, humidity))

            except RuntimeError as er:
                print(er.args[0])
                return

            except Exception as e:
                self.releaseSensor()
                raise e

    def writeLogFile(self, species_filename: str, subj_num: int):
        humidity_reqs = self.getSpeciesFile(species_filename)["Humidity"]
        temp_reqs = self.getSpeciesFile(species_filename)["Temperature"]

        filename = self.getFileDate(subj_num)

        humidity_dict = {"Humidity": [0, 1, 2, 3, 4]}
        humidity_df = pd.DataFrame(data=humidity_dict)

        # add stying
        wb = load_workbook(f'{filename}.xlsx')
        hum = wb['Humidity']
        #hum.append([])
        temp = wb['Humidity']
        #temp.append([])
        wb.save(f'{filename}.xlsx')

