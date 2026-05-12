-- Crear schema raw
CREATE SCHEMA IF NOT EXISTS raw;

-- Tabla de partidas
CREATE TABLE IF NOT EXISTS raw.matches (
    match_id            VARCHAR(20) PRIMARY KEY,
    game_id             BIGINT,
    platform_id         VARCHAR(10),
    game_mode           VARCHAR(20),
    game_version        VARCHAR(30),
    queue_id            INT,
    game_duration_secs  INT,
    game_creation       BIGINT,
    game_start          BIGINT,
    game_end            BIGINT,
    end_of_game_result  VARCHAR(30),
    ingested_at         TIMESTAMP DEFAULT NOW()	
);

-- Tabla de participantes
CREATE TABLE IF NOT EXISTS raw.participants (
    id                              SERIAL PRIMARY KEY,
    match_id                        VARCHAR(20) REFERENCES raw.matches(match_id),
    participant_id                  INT,
    puuid                           VARCHAR(100),
    riot_id_game_name               VARCHAR(50),
    riot_id_tagline                 VARCHAR(20),
    team_id                         INT,
    champion_id                     INT,
    champion_name                   VARCHAR(50),
    champ_level                     INT,
    kills                           INT,
    deaths                          INT,
    assists                         INT,
    win                             BOOLEAN,
    gold_earned                     INT,
    gold_spent                      INT,
    total_damage_dealt_to_champions INT,
    total_damage_taken              INT,
    damage_self_mitigated           INT,
    total_heal                      INT,
    total_heals_on_teammates        INT,
    total_minions_killed            INT,
    vision_score                    INT,
    time_spent_dead_secs            INT,
    longest_time_living_secs        INT,
    killing_sprees                  INT,
    double_kills                    INT,
    triple_kills                    INT,
    quadra_kills                    INT,
    penta_kills                     INT,
    first_blood_kill                BOOLEAN,
    first_blood_assist              BOOLEAN,
    item0                           INT,
    item1                           INT,
    item2                           INT,
    item3                           INT,
    item4                           INT,
    item5                           INT,
    item6                           INT,
    summoner1_id                    INT,
    summoner2_id                    INT,
    spell1_casts                    INT,
    spell2_casts                    INT,
    spell3_casts                    INT,
    spell4_casts                    INT,
    ingested_at                     TIMESTAMP DEFAULT NOW()
);

-- Tabla de equipos
CREATE TABLE IF NOT EXISTS raw.teams (
    id                      SERIAL PRIMARY KEY,
    match_id                VARCHAR(20) REFERENCES raw.matches(match_id),
    team_id                 INT,
    win                     BOOLEAN,
    champion_kills          INT,
    tower_kills             INT,
    inhibitor_kills         INT,
    first_blood             BOOLEAN,
    first_tower             BOOLEAN,
    ingested_at             TIMESTAMP DEFAULT NOW()
);