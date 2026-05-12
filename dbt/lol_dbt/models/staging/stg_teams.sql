WITH source AS (
    SELECT * FROM raw.teams
)

SELECT
    id,
    match_id,
    team_id,
    CASE team_id
        WHEN 100 THEN 'Blue'
        WHEN 200 THEN 'Red'
    END                 AS team_side,
    win,
    champion_kills,
    tower_kills,
    inhibitor_kills,
    first_blood,
    first_tower,
    ingested_at
FROM source