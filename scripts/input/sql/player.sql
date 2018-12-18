CREATE TABLE IF NOT EXISTS player (
  player_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  player_name VARCHAR(45) NOT NULL,
  player_kills INTEGER,
  player_dbno INTEGER,
  player_assists INTEGER,
  player_dmg INTEGER,
  player_dist_ride INTEGER,
  player_dist_walk INTEGER,
  player_survive_time INTEGER,
  PRIMARY KEY (player_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'C:/Users/ABC/Desktop/664/final_repo/data/player.csv'
INTO TABLE player
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (player_name, player_kills, player_dbno, player_assists, player_dmg, player_dist_ride, player_dist_walk, player_survive_time);