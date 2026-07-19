import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv

BASE_URL = "https://v3.football.api-sports.io/"
load_dotenv()
KEY = os.getenv("FOOTBALL_API_KEY")
HEADERS = {
    "x-apisports-key": KEY
}

TEAMS_MAPPING = {
    "FLAMENGO": {"team_id": 127, "league_id": 71},
    "PALMEIRAS": {"team_id": 121, "league_id": 71},
    "SAO PAULO": {"team_id": 126, "league_id": 71},
    "CORINTHIANS": {"team_id": 131, "league_id": 71},
    "FLUMINENSE": {"team_id": 124, "league_id": 71},
    "BOTAFOGO": {"team_id": 120, "league_id": 71},
    "VASCO": {"team_id": 133, "league_id": 71},
    "ATLETICO MINEIRO": {"team_id": 106, "league_id": 71},
    "CRUZEIRO": {"team_id": 135, "league_id": 71},
    "GREMIO": {"team_id": 130, "league_id": 71},
    "INTERNACIONAL": {"team_id": 119, "league_id": 71},
    "BAHIA": {"team_id": 118, "league_id": 71},
    "FORTALEZA": {"team_id": 154, "league_id": 71},
    "ATHLETICO PR": {"team_id": 134, "league_id": 71},
    "BRAGANTINO": {"team_id": 129, "league_id": 71},
    "CUIABA": {"team_id": 132, "league_id": 71},
    "ATLETICO GO": {"team_id": 137, "league_id": 71},
    "VITORIA": {"team_id": 113, "league_id": 71},
    "CRICIUMA": {"team_id": 125, "league_id": 71},
    "JUVENTUDE": {"team_id": 116, "league_id": 71},
    "MANCHESTER CITY": {"team_id": 47, "league_id": 39},
    "ARSENAL": {"team_id": 42, "league_id": 39},
    "LIVERPOOL": {"team_id": 40, "league_id": 39},
    "CHELSEA": {"team_id": 49, "league_id": 39},
    "MANCHESTER UNITED": {"team_id": 33, "league_id": 39},
    "TOTTENHAM": {"team_id": 47, "league_id": 39},
    "NEWCASTLE": {"team_id": 34, "league_id": 39},
    "ASTON VILLA": {"team_id": 66, "league_id": 39},
    "WEST HAM": {"team_id": 48, "league_id": 39},
    "BRIGHTON": {"team_id": 51, "league_id": 39},
    "WOLVERHAMPTON": {"team_id": 39, "league_id": 39},
    "FULHAM": {"team_id": 36, "league_id": 39},
    "CRYSTAL PALACE": {"team_id": 52, "league_id": 39},
    "BOURNEMOUTH": {"team_id": 35, "league_id": 39},
    "BRENTFORD": {"team_id": 55, "league_id": 39},
    "EVERTON": {"team_id": 45, "league_id": 39},
    "NOTTINGHAM FOREST": {"team_id": 65, "league_id": 39},
    "LEICESTER": {"team_id": 46, "league_id": 39},
    "SOUTHAMPTON": {"team_id": 41, "league_id": 39},
    "IPSWICH": {"team_id": 38, "league_id": 39},
    "REAL MADRID": {"team_id": 541, "league_id": 140},
    "BARCELONA": {"team_id": 529, "league_id": 140},
    "ATLETICO MADRID": {"team_id": 530, "league_id": 140},
    "SEVILLA": {"team_id": 536, "league_id": 140},
    "VALENCIA": {"team_id": 532, "league_id": 140},
    "REAL SOCIEDAD": {"team_id": 548, "league_id": 140},
    "ATHLETIC BILBAO": {"team_id": 531, "league_id": 140},
    "VILLARREAL": {"team_id": 533, "league_id": 140},
    "BETIS": {"team_id": 543, "league_id": 140},
    "GIRONA": {"team_id": 538, "league_id": 140},
    "CELTA VIGO": {"team_id": 539, "league_id": 140},
    "OSASUNA": {"team_id": 542, "league_id": 140},
    "GETAFE": {"team_id": 546, "league_id": 140},
    "RAYO VALLECANO": {"team_id": 547, "league_id": 140},
    "MALLORCA": {"team_id": 724, "league_id": 140},
    "LAS PALMAS": {"team_id": 728, "league_id": 140},
    "ALAVES": {"team_id": 544, "league_id": 140},
    "VALLADOLID": {"team_id": 556, "league_id": 140},
    "LEGANES": {"team_id": 559, "league_id": 140},
    "ESPANYOL": {"team_id": 545, "league_id": 140},
    "JUVENTUS": {"team_id": 496, "league_id": 135},
    "INTER DE MILAO": {"team_id": 505, "league_id": 135},
    "MILAN": {"team_id": 489, "league_id": 135},
    "NAPOLI": {"team_id": 492, "league_id": 135},
    "ROMA": {"team_id": 497, "league_id": 135},
    "LAZIO": {"team_id": 487, "league_id": 135},
    "ATALANTA": {"team_id": 499, "league_id": 135},
    "FIORENTINA": {"team_id": 502, "league_id": 135},
    "TORINO": {"team_id": 503, "league_id": 135},
    "BOLOGNA": {"team_id": 500, "league_id": 135},
    "GENOA": {"team_id": 488, "league_id": 135},
    "MONZA": {"team_id": 1579, "league_id": 135},
    "VERONA": {"team_id": 504, "league_id": 135},
    "CAGLIARI": {"team_id": 490, "league_id": 135},
    "LECCE": {"team_id": 495, "league_id": 135},
    "UDINESE": {"team_id": 494, "league_id": 135},
    "EMPOLI": {"team_id": 493, "league_id": 135},
    "PARMA": {"team_id": 501, "league_id": 135},
    "COMO": {"team_id": 1582, "league_id": 135},
    "VENEZIA": {"team_id": 491, "league_id": 135},
    "BAYERN DE MUNIQUE": {"team_id": 157, "league_id": 78},
    "BORUSSIA DORTMUND": {"team_id": 165, "league_id": 78},
    "BAYER LEVERKUSEN": {"team_id": 168, "league_id": 78},
    "RB LEIPZIG": {"team_id": 173, "league_id": 78},
    "EINTRACHT FRANKFURT": {"team_id": 169, "league_id": 78},
    "WOLFSBURG": {"team_id": 163, "league_id": 78},
    "STUTTGART": {"team_id": 172, "league_id": 78},
    "FREIBURG": {"team_id": 167, "league_id": 78},
    "HOFFENHEIM": {"team_id": 160, "league_id": 78},
    "WERDER BREMEN": {"team_id": 164, "league_id": 78},
    "HEIDENHEIM": {"team_id": 166, "league_id": 78},
    "AUGSBURG": {"team_id": 170, "league_id": 78},
    "GLADBACH": {"team_id": 161, "league_id": 78},
    "UNION BERLIN": {"team_id": 182, "league_id": 78},
    "BOCHUM": {"team_id": 162, "league_id": 78},
    "MAINZ": {"team_id": 171, "league_id": 78},
    "ST PAULI": {"team_id": 179, "league_id": 78},
    "KIEL": {"team_id": 174, "league_id": 78},
    "PSG": {"team_id": 85, "league_id": 61},
    "OLYMPIQUE DE MARSELHA": {"team_id": 81, "league_id": 61},
    "LYON": {"team_id": 80, "league_id": 61},
    "MONACO": {"team_id": 79, "league_id": 61},
    "LILLE": {"team_id": 77, "league_id": 61},
    "NICE": {"team_id": 82, "league_id": 61},
    "LENS": {"team_id": 91, "league_id": 61},
    "RENNES": {"team_id": 93, "league_id": 61},
    "STRASBOURG": {"team_id": 94, "league_id": 61},
    "REIMS": {"team_id": 84, "league_id": 61},
    "TOULOUSE": {"team_id": 92, "league_id": 61},
    "MONTPELLIER": {"team_id": 97, "league_id": 61},
    "NANTES": {"team_id": 83, "league_id": 61},
    "LE HAVRE": {"team_id": 98, "league_id": 61},
    "BREST": {"team_id": 100, "league_id": 61},
    "AUXERRE": {"team_id": 95, "league_id": 61},
    "ANGERS": {"team_id": 96, "league_id": 61},
    "SAINT ETIENNE": {"team_id": 103, "league_id": 61}
}


def search_api_data(team: str, season: int = 2024) -> dict:

    team_data = TEAMS_MAPPING.get(team)
    if not team_data:
        return {"status": "error", "mensage": f"The team '{team}' is not in our sistem."}
    
    team_id = team_data["team_id"]
    league_id = team_data["league_id"]

    cache_directory = "data cache"
    os.makedirs(cache_directory, exist_ok=True)
    date = datetime.now().strftime("%Y-%m-%d")
    archive = f"{cache_directory}/stats_team_{team}_{date}.json"

    if os.path.exists(archive):
        print(f"[INFO] Reading data from local cache for {team}...")
        with open(archive, "r", encoding="utf-8") as file:
            brute_data = json.load(file)
    else:
        print(f"[INFO] Downloading data from API-Football for {team}...")
        endpoint = f"{BASE_URL}teams/statistics"

        params = {
            "team": team_id,
            "league": league_id,
            "season": season
        }

        try:
            response = requests.get(endpoint, headers=HEADERS, params=params)
            response.raise_for_status()
            brute_data = response.json()
            
            with open(archive, "w", encoding="utf-8") as f:
                json.dump(brute_data, f, indent=4)
        except requests.exceptions.RequestException:
            return {"status": "error", "mensage": "Failed to connect to the API"}
        
        try:
            stats = brute_data["response"]
            clean_data = {
                "attack": {
                    "gols_scored_per_game": float(stats["goals"]["for"]["average"]["total"]),
                    "shots_pro": int(stats["shots"]["for"]["total"]),
                    "corners_pro": int(stats["corners"]["for"]["total"]),
                },
                "defense": {
                    "gols_suffered_per_game": float(stats["goals"]["against"]["average"]["total"]),
                    "shots_against": int(stats["shots"]["against"]["total"]),
                    "corners_against": int(stats["corners"]["against"]["total"]),
                }
            }
            return clean_data
        except (KeyError, TypeError):
            return {"status": "error", "mensage": "Data came on a unexpected format."}

