INSERT INTO `daerah` (`iddaerah`, `kode`, `nama`, `date_change`) VALUES
	(1, 'SBY', 'Surabaya', '2017-04-08 16:47:11'),
	(2, 'JKT', 'Jakarta', '2017-04-08 16:47:09'),
	(3, 'BDG', 'Bandung', '2017-04-08 16:47:10'),
	(4, 'DPS', 'Denpasar', '2017-04-08 16:47:10'),
	(5, 'JKT', 'Jakarta', '2017-04-09 16:47:10'),
	(6, 'YGJ', 'Jogja', '2017-04-09 16:47:10'),
	(7, 'CGK', 'Cengkareng', '2017-04-09 14:57:30'),
	(8, 'BUD', 'Ubud', '2017-04-09 14:57:30'),
	(9, 'SGJ', 'Singaraja', '2017-04-09 14:57:30');

INSERT INTO daerah3 VALUES (10, 'MED', 'MEDAN', '2017-04-15 15:24:14');
INSERT INTO daerah3 VALUES (11, 'PAD', 'Padang', '2017-04-15 15:24:15');

DELETE FROM daerah3 WHERE iddaerah = 1;
DELETE FROM daerah3 WHERE iddaerah = 3;


