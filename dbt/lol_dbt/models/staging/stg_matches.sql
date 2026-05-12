WITH source AS (
    SELECT * FROM raw.matches
)

SELECT
    match_id,
    game_id,
    platform_id,
    game_mode,
    game_version,
    queue_id,
    game_duration_secs,
    ROUND(game_duration_secs / 60.0, 2)         AS game_duration_mins,
    TO_TIMESTAMP(game_start / 1000)              AS game_start_ts,
    TO_TIMESTAMP(game_end / 1000)                AS game_end_ts,
    end_of_game_result,
    ingested_at
FROM source