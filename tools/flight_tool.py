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

BASE_URL = "https://api.aviationstack.com/v1/flights"

def f_clean_text(text:str) -> str:
    """
    To clean up text from response
    """
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]"," ",text)
    text = re.sub(r"\s+"," ",text)
    stop_words = [
        "flight", "flights", "ticket", "tickets", "trip", "travel",
        "plan", "complete", "days", "day", "including", "hotel",
        "hotels", "sightseeing", "under", "budget", "info", "information"
    ]
    words = [w for w in text.split() if w not in stop_words]
    output = " ".join(words).strip()
    return output


def f_country_name_to_countrycode(text:str):
    """
    This function coverts country name to country code
    """
    text=f_clean_text(text)

    if text in COUNTRY_ALIASES:
        return COUNTRY_ALIASES[text]

    try:
        country = pycountry.countries.lookup(text)
        return country.alpha_2
    except LookupError:
        pass

    for country in pycountry.countries:
        country_name = country.name.lower()
        if country_name in text:
            return country.alpha_2


    for alias,code in COUNTRY_ALIASES.items():
        