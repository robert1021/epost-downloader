import subprocess
import os
import shutil
import zipfile
from config import app_version, zip_name, app_name

if __name__ == "__main__":
    try:
        process = subprocess.run([
            "pyinstaller",
            "--onefile",
            "--noconsole",
            "--add-data", "frontend;frontend",
            "--add-data", "backend;backend",
            "--add-data", r"utilities.py;.",
            "--add-data", r"constants.py;.",
            "--add-data", r"vtp.py;.",
            "--add-data", r"date_validation.py;.",
            "--add-data", r"vtp_log_parser.py;.",
            "--add-data", r"enums.py;.",
            "--add-data", r"browser_automation.py;.",
            "--add-data", r"categorize_messages.py;.",
            "--add-data", r"CALENDAR_2010-2039.csv;.",
            "--add-data", r"config.py;.",
            "--add-data", r"dates_data.py;.",
            "--add-data", r"federal_calendar.py;.",
            "--add-data", r"styling.py;.",
            "--add-data", r"web_scrape_messages.py;.",
            "--add-data", r"xlsx_builder.py;.",
            "--hidden-import=eel",
            "--hidden-import=logging",
            "--hidden-import=tkinter",
            "--hidden-import=tkinter.filedialog",
            "--hidden-import=openpyxl",
            "--hidden-import=fpdf",
            "--hidden-import=selenium",
            "--hidden-import=win32com.client",
            "--hidden-import=pygetwindow",
            "--hidden-import=zipfile",
            "--hidden-import=selenium.webdriver.chrome",
            "--hidden-import=selenium.webdriver.chrome.service",
            "--hidden-import=selenium.webdriver.common.keys",
            "--hidden-import=selenium.webdriver.common.by",
            "--hidden-import=selenium.webdriver.support.ui",
            "--hidden-import=selenium.webdriver.support.expected_conditions",
            "--hidden-import=selenium.webdriver",
            r"--icon=frontend\images\automate-business.ico",
            "main.py"
        ], text=True, check=True)

        # create epost folder
        os.mkdir("epost")
        shutil.copytree("epostconnect", "epost/epostconnect")

        log_path = "epostconnect/vtp/logs"
        # Delete log files
        for file in os.listdir(log_path):
            os.remove(os.path.join(log_path, file))

        shutil.rmtree("build")
        os.remove("main.spec")
        os.rename("dist/main.exe", f"{app_name} v{app_version}.exe")

        # Create zip
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as z:
            # Add epost folder
            for root, dirs, files in os.walk("epost"):
                for file in files:
                    z.write(os.path.join(root, file))
                for directory in dirs:
                    z.write(os.path.join(root, directory))

            # Add files
            z.write("RELEASE_NOTES.txt")
            z.write(f"{app_name} v{app_version}.exe")

        shutil.rmtree("dist")
        shutil.rmtree("epost")
        os.remove(f"{app_name} v{app_version}.exe")

    except Exception as e:
        print("Error:", e)
