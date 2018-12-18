CREATE TEMPORARY TABLE temp_team (
  team_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  match_id_in_game VARCHAR(100) NOT NULL, 
  team_id_in_match INTEGER NOT NULL,
  team_placement INTEGER,
  PRIMARY KEY (team_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'C:/Users/ABC/Desktop/664/final_repo/data/team.csv'
INTO TABLE temp_team
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (match_id_in_game, team_id_in_match, team_placement);

CREATE TABLE IF NOT EXISTS team (
  team_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  match_id INTEGER NOT NULL, 
  team_id_in_match INTEGER NOT NULL,
  team_placement INTEGER,
  PRIMARY KEY (team_id),
  FOREIGN KEY (match_id) REFERENCES `match`(match_id)
  ON DELETE CASCADE ON UPDATE CASCADE 
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO team
(
  match_id,
  team_id_in_match,
  team_placement
)
SELECT m.match_id, tt.team_id_in_match, tt.team_placement
FROM temp_team tt
	LEFT JOIN `match` m
		   ON TRIM(tt.match_id_in_game) = TRIM(m.match_id_in_game);