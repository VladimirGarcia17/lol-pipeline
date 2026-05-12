import requests
import json
import time
import os
from dotenv import load_dotenv

#Cargar variables del rchivo .env
load_dotenv()
API_KEY = os.getenv("RIOT_API_KEY")
print(f"API KEY cargada: {API_KEY[:10] if API_KEY else 'NINGUNA'}")

#Header que se envían en cada petición a la API
HEADERS = {"X-Riot-Token": API_KEY}

#Obtener el PUUID de un jugador por su nombre
def get_puuid(game_name: str, tag_line: str, region: str = "americas") -> str:
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status() #Lanza error si la petición falla
    data = response.json()
    print(f"Jugador encontrado: {data['gameName']}#{data['tagLine']} | PUUID: {data['puuid'][:20]}...")
    return data["puuid"]

#Obtener lista de IDs de partidas recientes
def get_match_ids(puuid: str, count: int = 20, continent: str = "americas") -> list:
    url = f"https://{continent}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    params = {"count": count, "queue": 450}
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    match_ids = response.json()
    print(f"Partidas encontradas: {len(match_ids)}")
    return match_ids

#Obtener datos completos de una partida
def get_match_data(match_id: str, continent: str = "americas") -> dict:
    url = f"https://{continent}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

#Guardar JSON en disco
def save_json(data: dict, filename: str):
    os.makedirs("data/raw_json", exist_ok=True)
    filepath = f"data/raw_json/{filename}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Guardado: {filepath}")
    
#Pipeline principal
def extract_matches_for_player(game_name: str, tag_line: str, match_count: int = 20):
    print(f"\n=== Extrayendo partidas de: {game_name}#{tag_line} ===")
    
    #Obtener PUUID
    puuid = get_puuid(game_name, tag_line)
    time.sleep(1.5) #Pausa para respetar rate limit
    
    #Obtener IDs de partidas
    match_ids = get_match_ids(puuid, count=match_count)
    time.sleep(1.5)
    
    #Extraer y guardar cad partida
    for i, match_id  in enumerate(match_ids):
        print(f"Extrayendo partida {i+1}/{len(match_ids)}: {match_id}")
        match_data = get_match_data(match_id)
        save_json(match_data, match_id)
        time.sleep(1.5) #Pausa entre peticiones para no superar rate limit
        
    print(f"\n Extracción completa. {len(match_ids)} partidas guardadas en data/raw_json/")

#Ejecución
if __name__ == "__main__":
    extract_matches_for_player("Doblado", "WeebR", match_count=20)    