DROP TABLE IF EXISTS `MVoTs`;

CREATE TABLE `MVoTs` (
  `mvot_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `anon_id` VARCHAR(255),
  `registration_date` TIMESTAMP,
  `last_timestamp` TIMESTAMP,
  `sdtt` FLOAT,
  `RFC` FLOAT,
  `TSLC` FLOAT,
  `tx_time` FLOAT,
  `comm_freq` FLOAT,
  `certainty` FLOAT,
  `avg_tx_time` FLOAT,
  `trust_score` FLOAT,
  `distrust_score` FLOAT,
  `total_msgs` INTEGER,
  `other_count` INTEGER,
  `alerts_count` INTEGER,
  `timeout_count` INTEGER,
  `count_expected_msgs` INTEGER,
  `count_unexpected_msgs` INTEGER
);
