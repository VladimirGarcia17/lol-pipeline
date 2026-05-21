import requests
import json
import time
import os
from dotenv import load_dotenv

#Load variables from .env
load_dotenv()
API_KEY = os.getenv("RIOT_API_KEY")
print(f"API KEY cargada: {API_KEY[:10] if API_KEY else 'NINGUNA'}")

#Headers sent with every API request
HEADERS = {"X-Riot-Token": API_KEY}

#Get player PUUID by Riot ID
def get_puuid(game_name: str, tag_line: str, region: str = "americas") -> str:
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status() #Raise error if request fails
    data = response.json()
    print(f"Player found: {data['gameName']}#{data['tagLine']} | PUUID: {data['puuid'][:20]}...")
    return data["puuid"]

#Get list of recent match IDs
def get_match_ids(puuid: str, count: int = 20, continent: str = "americas", queue: int = None) -> list:
    url = f"https://{continent}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    params = {"count": count}
    if queue is not None:
        params["queue"] = queue
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    match_ids = response.json()
    print(f"Matches found: {len(match_ids)}")
    return match_ids

#Get full data for a single match
def get_match_data(match_id: str, continent: str = "americas") -> dict:
    url = f"https://{continent}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

#Save match data as JSON file
def save_json(data: dict, filename: str):
    os.makedirs("data/raw_json", exist_ok=True)
    filepath = f"data/raw_json/{filename}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved: {filepath}")
    
#Main extraction pipeline
def extract_matches_for_player(game_name: str, tag_line: str, match_count: int = 20):
    print(f"\n=== Extracting matches for: {game_name}#{tag_line} ===")
    
    #Step 1: get PUUID
    puuid = get_puuid(game_name, tag_line)
    time.sleep(1.5) #Pause to respect rate limit
    
    #Step 2: get matchs IDs
    
    #Extract ARAM matches (queue 450)
    aram_ids = get_match_ids(puuid, count=match_count, queue=450)
    time.sleep(1.5)
    
    #Extract Classic/Ranked matches (queue 420)
    classic_ids = get_match_ids(puuid, count=match_count, queue=420)
    time.sleep(1.5)
    
    #Step 3: combine and deduplicate
    all_match_ids = list(set(aram_ids + classic_ids))
    print(f"\nTotal unique matches to extract: {len(all_match_ids)}")
    
    #Step 4: extract and save each match
    for i, match_id  in enumerate(all_match_ids):
        print(f"Extracting match {i+1}/{len(all_match_ids)}: {match_id}")
        match_data = get_match_data(match_id)
        save_json(match_data, match_id)
        time.sleep(1.5) #Pause between requests to avoid rate limit
        
    print(f"\n Extraction complete. {len(all_match_ids)} matches saved to data/raw_json/")

#Entry point
if __name__ == "__main__":
    extract_matches_for_player("Doblado", "WeebR", match_count=20)    