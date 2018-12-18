CREATE TEMPORARY TABLE temp_death (
  death_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  weapon_name VARCHAR(45),
  killer_name VARCHAR(45), 
  killer_placement VARCHAR(45),
  match_id_in_game VARCHAR(100) NOT NULL,
  game_time INTEGER NOT NULL,
  victim_name VARCHAR(45),
  victim_placement VARCHAR(45),
  PRIMARY KEY (death_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'C:/Users/ABC/Desktop/664/final_repo/data/death_edit.csv'
INTO TABLE temp_death
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (weapon_name, killer_name, killer_placement, match_id_in_game, game_time, victim_name, victim_placement)

SET killer_placement = IF(killer_placement = '', NULL, TRIM(killer_placement)),
killer_placement = IF(killer_placement = '\r', NULL, TRIM(killer_placement)),
victim_placement = IF(victim_placement = '', NULL, TRIM(victim_placement)),
victim_placement = IF(victim_placement = '\r', NULL, TRIM(victim_placement));

CREATE TABLE IF NOT EXISTS death (
  death_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  weapon_id INTEGER,
  killer_id INTEGER, 
  killer_placement VARCHAR(45),
  match_id INTEGER NOT NULL,
  game_time INTEGER NOT NULL,
  victim_id INTEGER,
  victim_placement VARCHAR(45),
  PRIMARY KEY (death_id),
  FOREIGN KEY (weapon_id) REFERENCES weapon(weapon_id)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (killer_id) REFERENCES player(player_id)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (match_id) REFERENCES `match`(match_id)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (victim_id) REFERENCES player(player_id)
  ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO death
(
  weapon_id,
  killer_id, 
  killer_placement,
  match_id,
  game_time,
  victim_id,
  victim_placement
)
SELECT w.weapon_id, k.player_id, td.killer_placement, mt.match_id, td.game_time, v.player_id, td.victim_placement
FROM temp_death td
	LEFT JOIN weapon w
		   ON TRIM(td.weapon_name) = TRIM(w.weapon_name)
  LEFT JOIN player k
       ON TRIM(td.killer_name) = TRIM(k.player_name)
  LEFT JOIN `match` mt
       ON TRIM(td.match_id_in_game) = TRIM(mt.match_id_in_game)
  LEFT JOIN player v
       ON TRIM(td.victim_name) = TRIM(v.player_name);  