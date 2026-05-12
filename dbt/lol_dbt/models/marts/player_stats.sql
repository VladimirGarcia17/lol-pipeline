WITH participants AS (
    SELECT * FROM {{ ref('stg_participants') }}
)

SELECT
    riot_id_game_name,
    riot_id_tagline,
    COUNT(*)                                                AS total_games,
    SUM(CASE WHEN win THEN 1 ELSE 0 END)                   AS total_wins,
    ROUND(AVG(CASE WHEN win THEN 1.0 ELSE 0.0 END), 3)     AS win_rate,
    ROUND(AVG(kda), 2)                                      AS avg_kda,
    ROUND(AVG(kills), 2)                                    AS avg_kills,
    ROUND(AVG(deaths), 2)                                   AS avg_deaths,
    ROUND(AVG(assists), 2)                                  AS avg_assists,
    ROUND(AVG(total_damage_dealt_to_champions), 0)          AS avg_damage,
    ROUND(AVG(gold_earned), 0)                              AS avg_gold,
    SUM(penta_kills)                                        AS total_penta_kills,
    COUNT(DISTINCT champion_name)                           AS unique_champions_played
FROM participants
WHERE riot_id_game_name IS NOT NULL
GROUP BY riot_id_game_name, riot_id_tagline
ORDER BY total_games DESC