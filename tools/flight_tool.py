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
        if alias in text:
            return code

    return None

def f_airport_country_matchs(airport:dict,country_code:str) -> bool:

    airport_country = str(airport.get("country", "")).upper().strip()

    if airport_country == country_code:
        return True

    try:
        country = pycountry.countries.get(alpha_2=country_code)
        if country and airport_country.lower() == country.name.lower():
            return True

    except Exception:
        pass

    return False


def f_get_best_airport_for_country(country_code:str):
    """
    Generates the best airport from each country
    """
    preferred_airport = COUNTRY_MAIN_AIRPORT.get(country_code)

    if preferred_airport in AIRPORTS:
        return preferred_airport

    candidates = []

    for iata, airport in AIRPORTS.items():
        if not iata:
            continue

        if f_airport_country_matchs(airport,country_code):
            name = str(airport.get("name","")).lower()
            city = str(airport.get("city","")).lower()

            score = 0

            if "international" in name:
                score = score + 50
            if "intl" in name:
                score = score + 40
            if "capital" in name:
                score = score + 20
            if city:
                score = score + 5

            candidates.append((score,iata))

    if not candidates:
        return None

    candidates.sort(reverse=True)
    return candidates[0][1]