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

CREATE TEMPORARY TABLE temp_player_in_team (
  player_in_team_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  match_id_in_game VARCHAR(100) NOT NULL, 
  team_id_in_match INTEGER NOT NULL,
  player_name VARCHAR(45),
  PRIMARY KEY (player_in_team_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'C:/Users/ABC/Desktop/664/final_repo/data/player_in_team.csv'
INTO TABLE temp_player_in_team
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (match_id_in_game, team_id_in_match, player_name);

CREATE TABLE IF NOT EXISTS player_in_team (
  player_in_team_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  team_id INTEGER NOT NULL,
  player_id INTEGER,
  PRIMARY KEY (player_in_team_id),
  FOREIGN KEY (team_id) REFERENCES team(team_id)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (player_id) REFERENCES player(player_id)
  ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO player_in_team
(
  player_in_team_id,
  team_id,
  player_id
)
SELECT tpt.player_in_team_id, t.team_id, p.player_id
FROM temp_player_in_team tpt
  LEFT JOIN player p
       ON TRIM(tpt.player_name) = TRIM(p.player_name)
  LEFT JOIN temp_team tt
       ON TRIM(tpt.match_id_in_game) = TRIM(tt.match_id_in_game) AND TRIM(tpt.team_id_in_match) = TRIM(tt.team_id_in_match)
  LEFT JOIN team t
       ON tt.team_id = t.team_id;