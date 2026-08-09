import json
import os
import re


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "dtc_codes.json")


def load_dtc_data():

    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def find_dtc(code):

    dtc_data = load_dtc_data()

    code = code.upper().strip()

    for dtc in dtc_data:
        if dtc["code"] == code:
            return dtc

    return None


def extract_dtc_code(text):

    match = re.search(r"\b[PCBU][0-9]{4}\b", text.upper())

    if match:
        return match.group(0)

    return None