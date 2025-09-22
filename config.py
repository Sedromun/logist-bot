import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import pandas as pd
from pydantic import SecretStr
from aiogram.client.bot import DefaultBotProperties
from cryptography.fernet import Fernet

from utils.basic import normalize_rc_name


logging.basicConfig(level=logging.INFO)

load_dotenv()


# -- bot --

BOT_TOKEN: SecretStr = SecretStr(os.getenv("API_TOKEN"))
bot = Bot(
    BOT_TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode='HTML', link_preview_is_disabled=True)
)
dp = Dispatcher()


# -- database --

DB_USER = str(os.getenv("DB_USER"))
DB_URL = str(os.getenv("DB_URL"))
DB_PASSWORD = str(os.getenv("DB_PASSWORD"))
DB_NAME = str(os.getenv("DB_NAME"))

# -- codes --

ADMIN_SECRET_CODE = str(os.getenv("ADMIN_SECRET_CODE"))
SECRET_START = str(os.getenv("SECRET_START"))
SECRET_END = str(os.getenv("SECRET_END"))

# -- FERNET --

CRYPTO_KEY = str(os.getenv("CRYPTO_KEY"))
FERNET = Fernet(CRYPTO_KEY)

# -- Roles --

ROLE_NAMES = {"Партнер": "partner", "Склад": "warehouse"}

LIMITS_FILE = 'limits.csv'
limits_df = pd.read_csv(LIMITS_FILE)
CITIES_NAMES = [normalize_rc_name(k) for k in limits_df['РЦ']]
CITIES = {name: id for id, name in enumerate(CITIES_NAMES, start=1)}
ID_TO_CITY_NAME = {id: name for id, name in enumerate(CITIES_NAMES, start=1)}
