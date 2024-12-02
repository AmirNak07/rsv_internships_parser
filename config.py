import json
import os
import sys

from dotenv import load_dotenv

load_dotenv(dotenv_path="config/.env", override=True)

INTERNSHIPS_PAGE_URL = "https://rsv.ru/internships/"
INTERNSHIPS_API_URL = "https://projects2.rsv.ru/api/v1/internship"
REGIONS_API = "https://data.rsv.ru/catalog/get/region"
SKILS_API = "https://progress.rsv.ru/api/v1/competence?fields[]=id&fields[]=name&filter[type]=hard"
PAGE_PARAM = {"isOpenVacancy": "true"}
API_PARAM = {"filter[includeDraft]": "false", "take": 9, "skip": 0, "filter[isOpenVacancy]": "true"}
OFFSET_PARAM = 9
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
SHEET_NAME = os.environ.get("SHEET_NAME")
with open("config/logs.json", "r", encoding="utf-8") as file:
    LOGS_CONFIG = json.load(file)

for handler in LOGS_CONFIG["handlers"]:
    if handler["sink"] == "sys.stdout":
        handler["sink"] = sys.stdout
