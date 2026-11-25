import os
import re
import certifi
import airportsdata
import pycountry
from dotenv import load_dotenv
import requests

from utils.airport_mappings import (
    AIRPORTS,
    COUNTRY_ALIASES,
    COUNTRY_MAIN_AIRPORT,
    CITY_MAIN_AIRPORT
)

load_dotenv()

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

api_key = os.getenv("AVAIATIONSTACK_API_KEY")

DEFAULT_ORIGIN_IATA = os.getenv("DEFAULT_ORIGIN_IATA","CCU")

BASE_URL = "https://api.aviationstack.com/v1/floghts"