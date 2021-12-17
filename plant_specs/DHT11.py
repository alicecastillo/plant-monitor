# Created by: Alice Castillo

# Description: Specific to the Inland DHT11 sensor.

# sys lib
from datetime import datetime

# venv lib
import board
import adafruit_dht
from openpyxl import Workbook, load_workbook

# Local base class import
from plant_specs.Sensor import Sensor
from plant_specs.subject_logs.LogFile import LogFile, EvalColor

class DHT11(Sensor):
    def __init__(self, cur_time: int):
        super().__init__(cur_time, 2)
        self.sensor = adafruit_dht.DHT11(board.D4, use_pulseio=False)
        self.logs = [[], []] # [ humidity,  temp ]

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


    def getLogLists(self, logs_index, range, col_name):
        log_data = [
            self.getAvg(self.logs[logs_index]),
            self.getMedian(self.logs[logs_index])
        ]

        log_colors = self.getLogColors(self, log_data, range)
        return log_data, log_colors


    def writeLogFile(self, species_filename: str, log_file: LogFile):
        # Humidity
        humidity_log_data, humidity_log_colors = self.getLogLists(
            0,
            self.getSpeciesFile(species_filename)[0]["optimal"],
            "Humidity"
        )
        log_file.insertCol("Humidity", humidity_log_data, humidity_log_colors)

        # Temperature
        temp_log_data, temp_log_colors = self.getLogLists(
            1,
            self.getSpeciesFile(species_filename)[1]["optimal"],
            "Temperature"
        )
        log_file.insertCol("Humidity", temp_log_data, temp_log_colors)
