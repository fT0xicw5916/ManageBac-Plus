from openpyxl import Workbook
import os
import datetime
import sys

sys.path.insert(0, "..")

from enums import ExcelFillColor as FC


def read_logs(path):
    stats = os.stat(path)
    created_time = datetime.datetime.fromtimestamp(stats.st_ctime)

    info = 0
    warning = 0
    error = 0
    cache_requested = 0
    login_success = 0
    grade_hit = 0
    new_credentials = 0
    new_score = 0
    tick = 0

    with open(path, 'r') as f:
        for line in f:
            if line.startswith("[INFO]"):
                info += 1
            elif line.startswith("[WARNING]"):
                warning += 1
            elif line.startswith("[ERROR]"):
                error += 1

            if "app.cache - Caching GPA data for" in line:
                cache_requested += 1
            elif "app.selen - Login success" in line:
                login_success += 1
            elif "app.selen - Grade hit:" in line:
                grade_hit += 1
            elif "app.credentials - New credentials entry created with" in line:
                new_credentials += 1
            elif "app.scores - New score entry created with" in line:
                new_score += 1

            if "app - Tick" in line:
                tick += 1

    return created_time, info, warning, error, cache_requested, login_success, grade_hit, new_credentials, new_score, tick


def main():
    os.system("cd ..; mkdir -p reports")

    created_time, info, warning, error, cache_requested, login_success, grade_hit, new_credentials, new_score, tick = read_logs("../logs.log")

    wb = Workbook()
    sheet = wb.active

    sheet["A1"], sheet["B1"] = "Info", info
    sheet["A1"].fill, sheet["B1"].fill = FC.GREEN.value, FC.GREEN.value
    sheet["A2"], sheet["B2"] = "Warning", warning
    sheet["A2"].fill, sheet["B2"].fill = FC.ORANGE.value, FC.ORANGE.value
    sheet["A3"], sheet["B3"] = "Error", error
    sheet["A3"].fill, sheet["B3"].fill = FC.RED.value, FC.RED.value

    sheet["A5"], sheet["B5"] = "Cache requested", cache_requested
    sheet["A6"], sheet["B6"] = "Login success", login_success
    sheet["A7"], sheet["B7"] = "Grade hit", grade_hit

    sheet["A9"], sheet["B9"] = "New credentials", new_credentials
    sheet["A10"], sheet["B10"] = "New score", new_score

    sheet["D1"], sheet["E1"] = "Tick", tick

    wb.save(f"../reports/REPORT_{created_time}.xlsx")


if __name__ == "__main__":
    main()
