CREATE TABLE IF NOT EXISTS routes2 (
	id_route INTEGER NOT NULL,
        detail.airline VARCHAR DEFAULT NULL,
        detail.id_airline VARCHAR DEFAULT NULL,
        f.src_airport VARCHAR DEFAULT NULL,
        f.id_src_airport VARCHAR DEFAULT NULL,
	f.dst_airport VARCHAR DEFAULT NULL,
	f.id_dst_airport VARCHAR DEFAULT NULL,
	data.codeshare VARCHAR DEFAULT NULL,
	data.stop_val INTEGER DEFAULT NULL,
	log.equipment VARCHAR DEFAULT NULL,
	log.log_date VARCHAR DEFAULT NULL
	CONSTRAINT pk PRIMARY KEY (id_route)
);
