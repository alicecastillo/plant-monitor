# Created by: Alice Castillo

# Description:
import requests
import time
from . import PlantResource


class BadAPICall(Exception):
    def __init__(self, error_code: str, text: str):
        self.code = error_code
        self.text = text

    def __str__(self) -> str:
        return f"Error: {self.code}, Text: {self.text}"

    def errorAccessingIndex(self):
        self.code = "200, but unexpected response [check text for formatting]"


class UVIndex(PlantResource):
    def __init__(self, name: str, subject: int):
        super().__init__(name, subject)
        self.zip = 63130

    def evaluate(self):
        pass

    def exportData(self):
        pass

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
                return b
