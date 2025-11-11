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
    radar = 0
    notebook = 0
    uploads = 0
    downloads = 0
    illegal_uploads = 0
    database_resets = 0
    new_class = 0
    selenium_errors = 0
    mochi = 0
    login_failed = 0
    pwn_attempts = 0

    with open(path, 'r') as f:
        for line in f:

            # General info
            if line.startswith("[INFO]"):
                info += 1
            elif line.startswith("[WARNING]"):
                warning += 1
            elif line.startswith("[ERROR]"):
                error += 1

            # GPA data
            if "app.cache - Caching GPA data for" in line:
                cache_requested += 1
            elif "app.selen - Login success" in line:
                login_success += 1
            elif "app.selen - Grade hit:" in line:
                grade_hit += 1

            # Database
            if "app.credentials - New credentials entry created with" in line:
                new_credentials += 1
            elif "app.scores - New class table created" in line:
                new_class += 1
            elif "app.scores - New score entry created with" in line:
                new_score += 1
            elif "app.mochi - New mochi entry created" in line:
                mochi += 1
            elif "app.notebooks - New notebooks entry created" in line:
                notebook += 1
            elif "database RESET" in line:
                database_resets += 1

            # Tick
            if "app - Tick" in line:
                tick += 1

            # Utilities
            if "app - Radar graph at" in line:
                radar += 1

            # Upload/download
            if "app - Upload requested" in line:
                uploads += 1
            elif "app - Download requested" in line:
                downloads += 1
            elif "app - Illegal upload requested" in line:
                illegal_uploads += 1

            # Errors
            if "selenium.common.exceptions" in line or "Selenium error:" in line:
                selenium_errors += 1
            elif "app - Login failed with" in line:
                login_failed += 1
            elif "404 Not Found: The requested URL was not" in line:
                pwn_attempts += 1

    return created_time, info, warning, error, cache_requested, login_success, grade_hit, new_credentials, new_score, tick, radar, notebook, uploads, downloads, illegal_uploads, database_resets, new_class, selenium_errors, mochi, login_failed, pwn_attempts


def main():
    os.system("cd ..; mkdir -p reports")

    created_time, info, warning, error, cache_requested, login_success, grade_hit, new_credentials, new_score, tick, radar, notebook, uploads, downloads, illegal_uploads, database_resets, new_class, selenium_errors, mochi, login_failed, pwn_attempts = read_logs("../logs.log")

    wb = Workbook()
    sheet = wb.active

    # General info
    sheet["A1"], sheet["B1"] = "Info", info
    sheet["A1"].fill, sheet["B1"].fill = FC.GREEN.value, FC.GREEN.value
    sheet["A2"], sheet["B2"] = "Warning", warning
    sheet["A2"].fill, sheet["B2"].fill = FC.ORANGE.value, FC.ORANGE.value
    sheet["A3"], sheet["B3"] = "Error", error
    sheet["A3"].fill, sheet["B3"].fill = FC.RED.value, FC.RED.value

    # GPA data
    sheet["A5"], sheet["B5"] = "Cache requested", cache_requested
    sheet["A6"], sheet["B6"] = "Login success", login_success
    sheet["A7"], sheet["B7"] = "Grade hit", grade_hit

    # Database
    sheet["A9"], sheet["B9"] = "New credentials", new_credentials
    sheet["A10"], sheet["B10"] = "New class", new_class
    sheet["A11"], sheet["B11"] = "New score", new_score
    sheet["A12"], sheet["B12"] = "Mochi", mochi
    sheet["A13"], sheet["B13"] = "Notebook", notebook
    sheet["A14"], sheet["B14"] = "Database resets", database_resets
    sheet["A14"].fill, sheet["B14"].fill = FC.ORANGE.value, FC.ORANGE.value

    # Tick
    sheet["D1"], sheet["E1"] = "Tick", tick
    sheet["D1"].fill, sheet["E1"].fill = FC.LIGHT_GREY.value, FC.LIGHT_GREY.value

    # Utilities
    sheet["D3"], sheet["E3"] = "Radar", radar

    # Upload/download
    sheet["D5"], sheet["E5"] = "Uploads", uploads
    sheet["D6"], sheet["E6"] = "Downloads", downloads
    sheet["D7"], sheet["E7"] = "Illegal uploads", illegal_uploads
    sheet["D7"].fill, sheet["E7"].fill = FC.RED.value, FC.RED.value

    # Errors
    sheet["G1"], sheet["H1"] = "Selenium errors", selenium_errors
    sheet["G1"].fill, sheet["H1"].fill = FC.RED.value, FC.RED.value
    sheet["G2"], sheet["H2"] = "Login failed", login_failed
    sheet["G2"].fill, sheet["H2"].fill = FC.RED.value, FC.RED.value
    sheet["G3"], sheet["H3"] = "Pwn attempts", pwn_attempts
    sheet["G3"].fill, sheet["H3"].fill = FC.RED.value, FC.RED.value

    wb.save(f"../reports/REPORT_{created_time}.xlsx")


if __name__ == "__main__":
    main()
