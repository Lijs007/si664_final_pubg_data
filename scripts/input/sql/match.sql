DROP TABLE IF EXISTS temp_match;
CREATE TEMPORARY TABLE temp_match (
  match_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  match_id_in_game VARCHAR(100) NOT NULL, 
  date VARCHAR(45) NOT NULL,
  game_size INTEGER NOT NULL,
  match_mode VARCHAR(45) NOT NULL,
  party_size INTEGER NOT NULL,
  map_name VARCHAR(45) NOT NULL,
  PRIMARY KEY (match_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'C:/Users/ABC/Desktop/664/final_repo/data/match.csv'
INTO TABLE temp_match
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (match_id_in_game, date, game_size, match_mode, party_size, map_name);

CREATE TABLE IF NOT EXISTS `match` (
  match_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  match_id_in_game VARCHAR(100) NOT NULL, 
  date VARCHAR(45) NOT NULL,
  game_size INTEGER NOT NULL,
  match_mode VARCHAR(45) NOT NULL,
  party_size INTEGER NOT NULL,
  map_id INTEGER NOT NULL,
  PRIMARY KEY (match_id),
  FOREIGN KEY (map_id) REFERENCES map(map_id)
  ON DELETE CASCADE ON UPDATE CASCADE 
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `match`
(
  match_id_in_game, 
  date,
  game_size,
  match_mode,
  party_size,
  map_id	
)
SELECT tm.match_id_in_game, tm.date, tm.game_size, tm.match_mode, tm.party_size, m.map_id
FROM temp_match tm
	LEFT JOIN map m
		   ON TRIM(tm.map_name) = TRIM(m.map_name);