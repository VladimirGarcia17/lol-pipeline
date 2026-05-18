WITH matches AS (
    SELECT * FROM {{ ref('stg_matches') }}
),

teams AS (
    SELECT * FROM {{ ref('stg_teams') }}
),

winner AS (
    SELECT DISTINCT ON (match_id)
        match_id,
        team_side AS winning_side
    FROM teams
    WHERE win = TRUE
)

SELECT
    m.match_id,
    m.game_mode,
    m.game_duration_mins,
    m.game_start_ts,
    m.game_version,
    w.winning_side,
    t_blue.champion_kills     AS blue_kills,
    t_red.champion_kills      AS red_kills,
    t_blue.tower_kills        AS blue_towers,
    t_red.tower_kills         AS red_towers
FROM matches m
LEFT JOIN winner w       ON m.match_id = w.match_id
LEFT JOIN teams t_blue   ON m.match_id = t_blue.match_id AND t_blue.team_id = 100
LEFT JOIN teams t_red    ON m.match_id = t_red.match_id  AND t_red.team_id = 200
ORDER BY m.game_start_ts DESC