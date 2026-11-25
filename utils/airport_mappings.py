"""Worldwide airport lookup mappings with explicit preferred-airport overrides."""
import re
import airportsdata
import pycountry


def normalize(value):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", value.lower())).strip()


AIRPORTS = airportsdata.load("IATA")
COUNTRY_ALIASES = {}
for country in pycountry.countries:
    for field in ("name", "official_name", "common_name"):
        value = getattr(country, field, None)
        if value:
            COUNTRY_ALIASES[normalize(value)] = country.alpha_2

COUNTRY_MAIN_AIRPORT = {}
CITY_MAIN_AIRPORT = {}
_country_scores = {}
_city_scores = {}

for iata, airport in sorted(AIRPORTS.items()):
    country = str(airport.get("country", "")).upper().strip()
    city = normalize(str(airport.get("city") or ""))
    name = str(airport.get("name") or "").lower()
    score = 50 if "international" in name else 40 if "intl" in name else 0
    score += 5 if city else 0
    if country and score > _country_scores.get(country, -1):
        COUNTRY_MAIN_AIRPORT[country] = iata
        _country_scores[country] = score
    if city and score > _city_scores.get(city, -1):
        CITY_MAIN_AIRPORT[city] = iata
        _city_scores[city] = score

# Preserve the original explicit preferences.

COUNTRY_ALIASES.update({
    "usa": "US",
    "u.s.a": "US",
    "u.s.": "US",
    "america": "US",
    "united states": "US",
    "uk": "GB",
    "u.k.": "GB",
    "britain": "GB",
    "england": "GB",
    "uae": "AE",
    "dubai": "AE",
    "south korea": "KR",
    "korea": "KR",
    "russia": "RU",
    "vietnam": "VN",
    "bangladesh": "BD",
    "india": "IN",
    "japan": "JP",
    "china": "CN",
    "singapore": "SG",
    "malaysia": "MY",
    "thailand": "TH",
    "indonesia": "ID",
    "nepal": "NP",
    "qatar": "QA",
    "saudi arabia": "SA",
    "turkey": "TR",
    "canada": "CA",
    "australia": "AU",
    "germany": "DE",
    "france": "FR",
    "italy": "IT",
    "spain": "ES",
})

COUNTRY_MAIN_AIRPORT.update({
    "BD": "DAC",
    "IN": "DEL",
    "JP": "NRT",
    "US": "JFK",
    "GB": "LHR",
    "AE": "DXB",
    "SG": "SIN",
    "MY": "KUL",
    "TH": "BKK",
    "ID": "CGK",
    "CN": "PEK",
    "KR": "ICN",
    "NP": "KTM",
    "QA": "DOH",
    "SA": "JED",
    "TR": "IST",
    "CA": "YYZ",
    "AU": "SYD",
    "DE": "FRA",
    "FR": "CDG",
    "IT": "FCO",
    "ES": "MAD",
})

CITY_MAIN_AIRPORT.update({
    "dhaka": "DAC",
    "delhi": "DEL",
    "new delhi": "DEL",
    "mumbai": "BOM",
    "kolkata": "CCU",
    "chennai": "MAA",
    "bangalore": "BLR",
    "bengaluru": "BLR",
    "tokyo": "NRT",
    "osaka": "KIX",
    "kyoto": "KIX",
    "new york": "JFK",
    "london": "LHR",
    "dubai": "DXB",
    "singapore": "SIN",
    "kuala lumpur": "KUL",
    "bangkok": "BKK",
    "doha": "DOH",
    "istanbul": "IST",
    "toronto": "YYZ",
    "sydney": "SYD",
    "paris": "CDG",
    "rome": "FCO",
    "madrid": "MAD",
    "frankfurt": "FRA",
})

# Include normalized spellings used by flight_tool.clean_text.
COUNTRY_ALIASES.update({normalize(k): v for k, v in COUNTRY_ALIASES.items()})
