CREATE TABLE IF NOT EXISTS member (
	id INTEGER NOT NULL,
	name VARCHAR(50) NOT NULL DEFAULT NULL,
	salary DOUBLE NULL DEFAULT NULL,
	email VARCHAR(50) NULL DEFAULT NULL,
	CONSTRAINT pk PRIMARY KEY (id, name));
