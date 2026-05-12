WITH participants AS (
    SELECT * FROM {{ ref('stg_participants') }}
),

matches AS (
    SELECT * FROM {{ ref('stg_matches') }}
)

SELECT
    p.champion_name,
    COUNT(*)                                                AS total_games,
    SUM(CASE WHEN p.win THEN 1 ELSE 0 END)                 AS total_wins,
    ROUND(AVG(CASE WHEN p.win THEN 1.0 ELSE 0.0 END), 3)   AS win_rate,
    ROUND(AVG(p.kda), 2)                                    AS avg_kda,
    ROUND(AVG(p.kills), 2)                                  AS avg_kills,
    ROUND(AVG(p.deaths), 2)                                 AS avg_deaths,
    ROUND(AVG(p.assists), 2)                                AS avg_assists,
    ROUND(AVG(p.total_damage_dealt_to_champions), 0)        AS avg_damage,
    ROUND(AVG(p.gold_earned), 0)                            AS avg_gold,
    SUM(p.penta_kills)                                      AS total_penta_kills
FROM participants p
JOIN matches m ON p.match_id = m.match_id
GROUP BY p.champion_name
ORDER BY total_games DESC