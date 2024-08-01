from pathlib import Path

from dotenv import load_dotenv

import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

ADMINS = list(map(lambda admin_id: int(admin_id), os.getenv("ADMINS").split(" ")))

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANEL_USERNAME = os.getenv("CHANEL_USERNAME")

DB_URL = os.getenv("DB_URL")
DB_ECHO = False
