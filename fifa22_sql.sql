DROP TABLE IF EXISTS players;

CREATE TABLE players (
    short_name VARCHAR(100),
    long_name VARCHAR(150),
    player_positions VARCHAR(50),
    overall INT,
    potential INT,
    value_eur FLOAT,
    wage_eur FLOAT,
    age INT,
    height_cm INT,
    weight_kg INT,
    club_name VARCHAR(100),
    league_name VARCHAR(100),
    nationality_name VARCHAR(100),
    preferred_foot VARCHAR(10),
    weak_foot INT,
    skill_moves INT,
    pace FLOAT,
    shooting FLOAT,
    passing FLOAT,
    dribbling FLOAT,
    defending FLOAT,
    physic FLOAT,
    international_reputation FLOAT,
    release_clause_eur FLOAT
);

COPY players FROM 'C:\Users\Saksham\Desktop\players_clean.csv' 
DELIMITER ',' 
CSV HEADER 
ENCODING 'UTF8';

SELECT COUNT(*) FROM players;

-- Q1: Top 10 highest valued players
SELECT short_name, club_name, overall, value_eur
FROM players
ORDER BY value_eur DESC
LIMIT 10;

-- Q2: Konsi league mein average player value sabse zyada hai?
SELECT league_name, ROUND(AVG(value_eur)::NUMERIC, 2) AS avg_value
FROM players
GROUP BY league_name
ORDER BY avg_value DESC
LIMIT 10;

-- Q3: Konsa position sabse zyada earn karta hai?
SELECT SPLIT_PART(player_positions, ',', 1) AS main_position, 
       ROUND(AVG(wage_eur)::NUMERIC, 2) AS avg_wage
FROM players
GROUP BY main_position
ORDER BY avg_wage DESC
LIMIT 10;

-- Q4: Young undervalued players (age < 23, potential >= 85)
SELECT short_name, age, overall, potential, value_eur
FROM players
WHERE age < 23 AND potential >= 85
ORDER BY value_eur ASC
LIMIT 10;

-- Q5: Konsi nationality ke players ki average value sabse zyada hai?
SELECT nationality_name, ROUND(AVG(value_eur)::NUMERIC, 2) AS avg_value
FROM players
GROUP BY nationality_name
ORDER BY avg_value DESC
LIMIT 10;
