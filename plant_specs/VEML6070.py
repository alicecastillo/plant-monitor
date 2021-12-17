# Created by: Alice Castillo

# Description: Specific to the Adafruit VEML6070 sensor.

# sys lib
import time
import requests

# venv lib
import board
import busio
import adafruit_veml6070
from openpyxl import Workbook

# Local base class import
from plant_specs.Sensor import Sensor
from plant_specs.subject_logs.LogFile import LogFile, EvalColor

class BadAPICall(Exception):
    def __init__(self, error_code: str, text: str):
        self.code = error_code
        self.text = text

    def __str__(self) -> str:
        return f"Error: {self.code}, Text: {self.text}"

    def errorAccessingIndex(self):
        self.code = "200, but unexpected response [check text for formatting]"


class VEML6070(Sensor):
    def __init__(self,  cur_time: int):
        super().__init__(cur_time, 5)
        self.sensor = adafruit_veml6070.VEML6070(busio.I2C(board.SCL, board.SDA))
        self.zip = 63130


    def setZip(self, zip: int) -> None:
        self.zip = zip


    def runSensor(self, sec: int):
        if self.readyToRead(sec):
            try:
                uv_raw = self.sensor.uv_raw
                #uv_index = self.sensor.get_index(uv_raw)
                self.logs.append(float(uv_raw))
                print("At {0}, UV Index {1}".format(sec, uv_raw))
            except RuntimeError as er:
                print(er.args[0])

    def writeLogFile(self, species_filename: str, log_file: LogFile):
        print("VEML6070 writing logs")
        uv_reqs = self.getSpeciesFile(species_filename)[2]["optimal"]

        log_data = [
            self.getAvg(self.logs),
            self.getMedian(self.logs)
        ]

        api_data = ""
        for i in range(3):
            print("try: {}".format(i))
            try:
                api = self.hitAPI()
                api_data = api
                break
            except BadAPICall as bac:
                api_data = f"{bac}"
            except Exception as e:
                api_data = "Error: {}".format(e.code)
                break
            time.sleep(1)
        log_data.append(api_data)
        print(log_data)

        log_colors = self.getLogColors(log_data, uv_reqs)
        log_file.insertCol("UV Level", log_data, log_colors)
        
        print("VEML6070 fin ---")


    def hitAPI(self):
        return "Error: bad"
        try:
            url = "https://enviro.epa.gov/enviro/efservice/getEnvirofactsUVDAILY/ZIP/{0}/json".format(self.zip)
            response = requests.get(url)
            if response.status_code == 200:
                # good request
                try:
                    r_json = response.json()
                    return int(r_json[0]['UV_INDEX'])
                except Exception as e:
                    b = BadAPICall(response.status_code, response.text)
                    b.errorAccessingIndex()
                    raise b
            else:
                raise BadAPICall(response.status_code, response.reason)
        except Exception as e:
            raise e
