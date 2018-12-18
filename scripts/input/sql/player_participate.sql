CREATE TEMPORARY TABLE temp_player_participate (
  player_participate_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  match_id_in_game VARCHAR(100) NOT NULL, 
  player_name VARCHAR(45),
  PRIMARY KEY (player_participate_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'C:/Users/ABC/Desktop/664/final_repo/data/player_participate.csv'
INTO TABLE temp_player_participate
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (match_id_in_game, player_name);

CREATE TABLE IF NOT EXISTS player_participate (
  player_participate_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  match_id INTEGER NOT NULL, 
  player_id INTEGER,
  PRIMARY KEY (player_participate_id),
  FOREIGN KEY (match_id) REFERENCES `match`(match_id)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (player_id) REFERENCES player(player_id)
  ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO player_participate
(
  match_id,
  player_id
)
SELECT m.match_id, p.player_id
FROM temp_player_participate tpp
  LEFT JOIN player p
       ON TRIM(tpp.player_name) = TRIM(p.player_name)
  LEFT JOIN `match` m
       ON TRIM(tpp.match_id_in_game) = TRIM(m.match_id_in_game);