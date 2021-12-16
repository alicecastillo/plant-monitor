# Created by: Alice Castillo

# Description: Generic base class for any plant.
import json
import os
import time
from datetime import datetime
import xlsxwriter
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Fill, PatternFill

# Import sensor classes
from plant_specs.VEML6070 import VEML6070
from plant_specs.DHT11 import DHT11


def createExcelFile(filename: str) -> None:
    # create file
    try:
        wb = load_workbook(f'{filename}.xlsx')
    except FileNotFoundError as e:
        # Create Excel file through xlsxwriter
        workbook = xlsxwriter.Workbook(f'{filename}.xlsx')
        workbook.close()

        # Now modify to add sheets for all sensors (This could be generalized in future)
        wb = load_workbook(f'{filename}.xlsx')
        sheets = ["Daily Evaluation", "Humidity", "Temperature", "UV Level"]
        for sheet in sheets:
            ws = wb.create_sheet(title=sheet)
            header = ws.row_dimensions[1]
            header.font = Font(bold=True, color="FFFFFF")
            header.fill = PatternFill("solid", fgColor="000000")
        wb.save(f'{filename}.xlsx')
        wb = load_workbook(f'{filename}.xlsx')
        wb.close()

        # Remove default-add "Sheet1"
        wb = load_workbook(f'{filename}.xlsx')
        if wb.sheetnames[0] == "Sheet1":
            wb.remove(wb[wb.sheetnames[0]]) # Remove "Sheet1"
        wb.save(f'{filename}.xlsx')

    # Close and exit
    wb.close()


def colNumToLetters(col_num: int) -> str:
    """ Converts a column num to Excel's lettering system.
        Ex: Col 1 = 'A'
    """
    if col_num > 26:
        return "{}{}".format(chr(col_num//26 + 64), chr(col_num%26 + 64))
    return "{}".format(chr(col_num % 26 + 64))


# def getNextCol(filename: str, sheet: str) -> int:
#     wb = load_workbook(f'{filename}.xlsx')
#     return wb[sheet].max_column+1



def insertCol(filename, sheet, data):
    wb = load_workbook(f'{filename}.xlsx')
    ws = wb[sheet]
    next_col = wb[sheet].max_column+1
    ws.insert_cols(next_col)
    for count, d in enumerate(data):
        ws["{}{}".format(colNumToLetters(next_col), count+2)] = d
    wb.save(f'{filename}.xlsx')
    wb.close()



class Plant():
    def __init__(self, num: int, reqs: list = []):
        self.loadData(num)
        self.num = num
        self.species_filepath, self.species_filename = "", ""
        self.last_ht_check, self.last_uv_check, self.last_water = 0, 0, 0

    def loadData(self, num: int):
        # get subject file
        sub_json = self.readJSONFile("plant_specs/current_subjects/subject_{0}.json".format(num))
        self.last_ht_check = sub_json["last_ht_check"]
        self.last_uv_check = sub_json["last_uv_check"]
        self.last_water = sub_json["last_water"]

        # move this to outside method if possible later
        #self.species_filepath = "plant_specs/species/{0}.json".format(sub_json["species_filename"])
        self.species_filename = sub_json["species_filename"]

    def checkResources(self):
        # -    Water moisture and temperature 2x / hr, 24 x 1 day
        # -    Sunlight logging 4 x / hr DURING DAYLIGHT
        pass

    def writeUpdate(self):
        pass

    def readJSONFile(self, path):
        f = open(os.path.join(os.getcwd(), path), "r")
        return json.load(f)

    def getReadings(self, cur_time: int) -> None:
        sensors = [VEML6070(cur_time)]
        cur_min = int(datetime.fromtimestamp(cur_time).strftime("%M"))
        if cur_min % 30:
            sensors.append(DHT11(cur_time))

        #if int(datetime.fromtimestamp(cur_time).strftime("%H")) cur_min == 0:
        #     # create Excel file
        createExcelFile("SUBJECT{0}_{1}_logs".format(self.num, datetime.fromtimestamp(cur_time).strftime("%b_%d_%Y")))

        for i in range(60):
            for sensor in sensors:
                sensor.runSensor(i)
            time.sleep(1)
        for sensor in sensors:
            sensor.writeLogFile(self.species_filename, self.num)



    def writeLogs(self):
        pass