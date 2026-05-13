import json
import os
import glob
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

#Connect to PostgreSQL
engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

#Load match metadata into raw.matches
def load_match(info: dict, match_id: str, conn):
    query = text("""
        INSERT INTO raw.matches (
            match_id, game_id, platform_id, game_mode, game_version,
            queue_id, game_duration_secs, game_creation, game_start,
            game_end, end_of_game_result
        ) VALUES (
            :match_id, :game_id, :platform_id, :game_mode, :game_version,
            :queue_id, :game_duration_secs, :game_creation, :game_start,
            :game_end, :end_of_game_result
        )
        ON CONFLICT (match_id) DO NOTHING;
    """)
    conn.execute(query, {
        "match_id":             match_id,
        "game_id":              info.get("gameId"),
        "platform_id":          info.get("platformId"),
        "game_mode":            info.get("gameMode"),
        "game_version":         info.get("gameVersion"),
        "queue_id":             info.get("queueId"),
        "game_duration_secs":   info.get("gameDuration"),
        "game_creation":        info.get("gameCreation"),
        "game_start":           info.get("gameStartTimestamp"),
        "game_end":             info.get("gameEndTimestamp"),
        "end_of_game_result":   info.get("endOfGameResult"),
    })

#Load player stats into raw.participants
def load_participants(participants: list, match_id: str, conn):
    query = text("""
        INSERT INTO raw.participants (
            match_id, participant_id, puuid, riot_id_game_name, riot_id_tagline,
            team_id, champion_id, champion_name, champ_level,
            kills, deaths, assists, win,
            gold_earned, gold_spent,
            total_damage_dealt_to_champions, total_damage_taken,
            damage_self_mitigated, total_heal, total_heals_on_teammates,
            total_minions_killed, vision_score,
            time_spent_dead_secs, longest_time_living_secs,
            killing_sprees, double_kills, triple_kills, quadra_kills, penta_kills,
            first_blood_kill, first_blood_assist,
            item0, item1, item2, item3, item4, item5, item6,
            summoner1_id, summoner2_id,
            spell1_casts, spell2_casts, spell3_casts, spell4_casts
        ) VALUES (
            :match_id, :participant_id, :puuid, :riot_id_game_name, :riot_id_tagline,
            :team_id, :champion_id, :champion_name, :champ_level,
            :kills, :deaths, :assists, :win,
            :gold_earned, :gold_spent,
            :total_damage_dealt_to_champions, :total_damage_taken,
            :damage_self_mitigated, :total_heal, :total_heals_on_teammates,
            :total_minions_killed, :vision_score,
            :time_spent_dead_secs, :longest_time_living_secs,
            :killing_sprees, :double_kills, :triple_kills, :quadra_kills, :penta_kills,
            :first_blood_kill, :first_blood_assist,
            :item0, :item1, :item2, :item3, :item4, :item5, :item6,
            :summoner1_id, :summoner2_id,
            :spell1_casts, :spell2_casts, :spell3_casts, :spell4_casts
        );
        ON CONFLICT ON CONSTRAINT unique_participant_per_match DO NOTHING;
    """)
    for p in participants:
        conn.execute(query, {
            "match_id":                         match_id,
            "participant_id":                   p.get("participantId"),
            "puuid":                            p.get("puuid"),
            "riot_id_game_name":                p.get("riotIdGameName"),
            "riot_id_tagline":                  p.get("riotIdTagline"),
            "team_id":                          p.get("teamId"),
            "champion_id":                      p.get("championId"),
            "champion_name":                    p.get("championName"),
            "champ_level":                      p.get("champLevel"),
            "kills":                            p.get("kills"),
            "deaths":                           p.get("deaths"),
            "assists":                          p.get("assists"),
            "win":                              p.get("win"),
            "gold_earned":                      p.get("goldEarned"),
            "gold_spent":                       p.get("goldSpent"),
            "total_damage_dealt_to_champions":  p.get("totalDamageDealtToChampions"),
            "total_damage_taken":               p.get("totalDamageTaken"),
            "damage_self_mitigated":            p.get("damageSelfMitigated"),
            "total_heal":                       p.get("totalHeal"),
            "total_heals_on_teammates":         p.get("totalHealsOnTeammates"),
            "total_minions_killed":             p.get("totalMinionsKilled"),
            "vision_score":                     p.get("visionScore"),
            "time_spent_dead_secs":             p.get("totalTimeSpentDead"),
            "longest_time_living_secs":         p.get("longestTimeSpentLiving"),
            "killing_sprees":                   p.get("killingSprees"),
            "double_kills":                     p.get("doubleKills"),
            "triple_kills":                     p.get("tripleKills"),
            "quadra_kills":                     p.get("quadraKills"),
            "penta_kills":                      p.get("pentaKills"),
            "first_blood_kill":                 p.get("firstBloodKill"),
            "first_blood_assist":               p.get("firstBloodAssist"),
            "item0":                            p.get("item0"),
            "item1":                            p.get("item1"),
            "item2":                            p.get("item2"),
            "item3":                            p.get("item3"),
            "item4":                            p.get("item4"),
            "item5":                            p.get("item5"),
            "item6":                            p.get("item6"),
            "summoner1_id":                     p.get("summoner1Id"),
            "summoner2_id":                     p.get("summoner2Id"),
            "spell1_casts":                     p.get("spell1Casts"),
            "spell2_casts":                     p.get("spell2Casts"),
            "spell3_casts":                     p.get("spell3Casts"),
            "spell4_casts":                     p.get("spell4Casts"),
        })

#Load team results into raw.teams
def load_teams(teams: list, match_id: str, conn):
    query = text("""
        INSERT INTO raw.teams (
            match_id, team_id, win,
            champion_kills, tower_kills, inhibitor_kills,
            first_blood, first_tower
        ) VALUES (
            :match_id, :team_id, :win,
            :champion_kills, :tower_kills, :inhibitor_kills,
            :first_blood, :first_tower
        );
        ON CONFLICT ON CONSTRAINT unique_team_per_match DO NOTHING;
    """)
    for t in teams:
        objectives = t.get("objectives", {})
        conn.execute(query, {
            "match_id":         match_id,
            "team_id":          t.get("teamId"),
            "win":              t.get("win"),
            "champion_kills":   objectives.get("champion", {}).get("kills"),
            "tower_kills":      objectives.get("tower", {}).get("kills"),
            "inhibitor_kills":  objectives.get("inhibitor", {}).get("kills"),
            "first_blood":      objectives.get("champion", {}).get("first"),
            "first_tower":      objectives.get("tower", {}).get("first"),
        })

#Main loading pipeline
def load_all_matches():
    json_files = glob.glob("data/raw_json/*.json")
    print(f"Archivos encontrados: {len(json_files)}")

    with engine.begin() as conn:
        for filepath in json_files:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            match_id = data["metadata"]["matchId"]
            info = data["info"]

            print(f"Cargando: {match_id}")
            load_match(info, match_id, conn)
            load_participants(info["participants"], match_id, conn)
            load_teams(info["teams"], match_id, conn)

    print(f"\n✅ Load complete. {len(json_files)} matches inserted into PostgreSQL.")

#Entry point
if __name__ == "__main__":
    load_all_matches()