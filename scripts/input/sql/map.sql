CREATE TABLE IF NOT EXISTS map (
  map_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  map_name VARCHAR(45) NOT NULL UNIQUE,
  PRIMARY KEY (map_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'C:/Users/ABC/Desktop/664/final_repo/data/map.csv'
INTO TABLE map
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (map_name);