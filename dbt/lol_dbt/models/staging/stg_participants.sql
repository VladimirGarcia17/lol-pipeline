WITH source AS (
    SELECT * FROM raw.participants
)

SELECT
    id,
    match_id,
    participant_id,
    puuid,
    riot_id_game_name,
    riot_id_tagline,
    team_id,
    champion_id,
    champion_name,
    champ_level,
    kills,
    deaths,
    assists,
    CASE
        WHEN deaths = 0 THEN kills + assists
        ELSE ROUND((kills + assists)::NUMERIC / deaths, 2)
    END                                          AS kda,
    win,
    gold_earned,
    gold_spent,
    total_damage_dealt_to_champions,
    total_damage_taken,
    damage_self_mitigated,
    total_heal,
    total_heals_on_teammates,
    total_minions_killed,
    vision_score,
    time_spent_dead_secs,
    longest_time_living_secs,
    killing_sprees,
    double_kills,
    triple_kills,
    quadra_kills,
    penta_kills,
    first_blood_kill,
    first_blood_assist,
    item0, item1, item2, item3, item4, item5, item6,
    summoner1_id,
    summoner2_id,
    ingested_at
FROM source