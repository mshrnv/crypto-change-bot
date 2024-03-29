"""Config file"""
from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# MONGO_HOST = getenv("MONGO_HOST")
# MONGO_PORT = int(getenv("MONGO_PORT"))
REDIS_HOST = getenv("REDIS_HOST")
REDIS_PORT = int(getenv("REDIS_PORT"))
REDIS_DB = int(getenv("REDIS_DB"))

MEXC_ACCESS_KEY = getenv("MEXC_ACCESS_KEY")
MEXC_SECRET_KEY = getenv("MEXC_SECRET_KEY")
