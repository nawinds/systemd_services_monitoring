import os

TOKEN = os.getenv("TOKEN", None)
LOCAL_PATH = os.getcwd()
AIOGRAM_LOGS_PATH = f"{LOCAL_PATH}/logs/aiogram.log"
DB_PATH = f"{LOCAL_PATH}/modules/data/db/main.db"
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", None).split()))

if not os.path.exists(f"{LOCAL_PATH}/logs"):
    os.mkdir(f"{LOCAL_PATH}/logs")
if not os.path.exists(f"{LOCAL_PATH}/modules/db"):
    os.mkdir(f"{LOCAL_PATH}/modules/db")
