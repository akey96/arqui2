
use dht11;

DROP TABLE IF EXISTS `data`;

CREATE TABLE `data` (
      id  int NOT NULL AUTO_INCREMENT,
      date datetime NOT NULL DEFAULT  ,
      temperature int,
      humidity int,
      PRIMARY KEY(`id`)
);

INSERT INTO data(temperature, humidity) VALUES (20, 30), (33, 45);

SELECT * from data;