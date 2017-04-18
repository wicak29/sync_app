CREATE TABLE IF NOT EXISTS member3 (
	id_member INTEGER NOT NULL,
	user.name VARCHAR DEFAULT NULL,
	user.salary INTEGER DEFAULT NULL,
	detail.date_change DATE NULL,
	detail.email VARCHAR,
	detail.address VARCHAR
     CONSTRAINT pk PRIMARY KEY (id_member)
);
