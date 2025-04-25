# wase_core/spell_updater.py

import requests
import os
import time
import csv

# Import the icon downloader function
from wase_core.icon_downloader import get_icons

CSV_URL = "https://wago.tools/db2/Spell/csv"
LOCAL_CSV = "wase_data/spells.csv"
ICON_DIR = "wase_data/icons"
DEFAULT_ICON = os.path.join(ICON_DIR, "INV_Misc_QuestionMark.blp")
MAX_AGE_SECONDS = 86400  # 1 day

def is_csv_fresh():
    if not os.path.exists(LOCAL_CSV):
        return False
    modified_time = os.path.getmtime(LOCAL_CSV)
    return (time.time() - modified_time) < MAX_AGE_SECONDS

def download_spell_csv():
    print("Downloading latest spells.csv from Wago.tools...")
    response = requests.get(CSV_URL)
    if response.status_code == 200:
        os.makedirs("wase_data", exist_ok=True)
        with open(LOCAL_CSV, 'wb') as f:
            f.write(response.content)
        print("Downloaded and saved spells.csv.")
    else:
        raise Exception(f"Failed to download CSV. Status: {response.status_code}")

def parse_spell_csv():
    spells = {}
    with open(LOCAL_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            spellID = int(row['ID'])
            spellName = row.get('NameSubtext_lang') or f"Spell {spellID}"
            if not spellName:
                continue  # Skip unnamed spells
            iconPath = DEFAULT_ICON  # Placeholder icon logic
            castTime = 0
            minRange = 0
            maxRange = 40
            spells[spellID] = (spellName, iconPath, castTime, minRange, maxRange, spellID)
    print(f"Parsed {len(spells)} spells from CSV.")
    return spells

def ensure_spells_loaded():
    # Ensure icons are available first
    print("Ensuring icons are available...")
    get_icons()

    if not is_csv_fresh():
        download_spell_csv()
    return parse_spell_csv()
