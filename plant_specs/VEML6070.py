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
                uv_index = self.sensor.get_index(uv_raw)
                print("At {0}, UV Index {1}".format(sec, uv_index))
            except RuntimeError as er:
                print(er.args[0])

    def writeLogFile(self, species_filename: str, subj_num: int):
        uv_reqs = self.getSpeciesFile(species_filename)["UV"]
        filename = self.getFileDate(subj_num)


    def hitAPI(self) -> int:
        url = "https://enviro.epa.gov/enviro/efservice/getEnvirofactsUVDAILY/ZIP/{0}/json".format(self.zip)
        response = requests.get(url)

        # doesn't work
        tries = 0
        while response.status_code != 200:
            if tries > 3:
                return BadAPICall(response.status_code, response.text)
            time.sleep(2)
            response = requests.get(url)
            tries += 1

        if response.status_code == 200:
            # good request
            try:
                r_json = response.json()
                return int(r_json[0]['UV_INDEX'])
            except Exception as e:
                b = BadAPICall(response.status_code, response.text)
                b.errorAccessingIndex()
                raise b
