import os

TOKEN = os.getenv("TOKEN", None)
LOCAL_PATH = os.getcwd()
AIOGRAM_LOGS_PATH = f"{LOCAL_PATH}/logs/aiogram.log"
DB_PATH = f"{LOCAL_PATH}/modules/data/db/main.db"
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", None).split()))
CONTACT_MAIL = "me@nawinds.top"

if not os.path.exists(f"{LOCAL_PATH}/logs"):
    os.mkdir(f"{LOCAL_PATH}/logs")
if not os.path.exists(f"{LOCAL_PATH}/modules/data/db"):
    os.mkdir(f"{LOCAL_PATH}/modules/data/db")
if not os.path.exists(f"{LOCAL_PATH}/temp"):
    os.mkdir(f"{LOCAL_PATH}/temp")
with open("temp/alerted.txt", "w", encoding="utf-8") as f:
    f.write("")
