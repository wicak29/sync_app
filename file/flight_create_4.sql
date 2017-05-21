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

CREATE TABLE IF NOT EXISTS airport2 (
    airport_id INTEGER NOT NULL,
    d.name_airport VARCHAR DEFAULT NULL,
    d.city VARCHAR DEFAULT NULL,
    d.country VARCHAR DEFAULT NULL,
    kode.iata VARCHAR DEFAULT NULL,
    kode.icao VARCHAR DEFAULT NULL,
    pos.latitude VARCHAR DEFAULT NULL,
    pos.longitude VARCHAR DEFAULT NULL,
    pos.altitude VARCHAR DEFAULT NULL,
    time.timezone VARCHAR DEFAULT NULL,
    time.dst VARCHAR DEFAULT NULL,
    time.tz_db VARCHAR DEFAULT NULL,
    tipe.type_airport VARCHAR DEFAULT NULL,
    tipe.source VARCHAR
	CONSTRAINT pk PRIMARY KEY (airport_id)
);

CREATE TABLE IF NOT EXISTS airline2 (
        id_airline INTEGER NOT NULL,
        d.name VARCHAR DEFAULT NULL,
        d.alias VARCHAR DEFAULT NULL,
        kode.iata VARCHAR DEFAULT NULL,
        kode.icao VARCHAR DEFAULT NULL,
        pos.callsign VARCHAR DEFAULT NULL,
        pos.country VARCHAR DEFAULT NULL,
        pos.active_stat VARCHAR DEFAULT NULL
        CONSTRAINT pk PRIMARY KEY (id_airline)
);

CREATE TABLE IF NOT EXISTS routes3 (
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

CREATE TABLE IF NOT EXISTS airport3 (
    airport_id INTEGER NOT NULL,
    d.name_airport VARCHAR DEFAULT NULL,
    d.city VARCHAR DEFAULT NULL,
    d.country VARCHAR DEFAULT NULL,
    kode.iata VARCHAR DEFAULT NULL,
    kode.icao VARCHAR DEFAULT NULL,
    pos.latitude VARCHAR DEFAULT NULL,
    pos.longitude VARCHAR DEFAULT NULL,
    pos.altitude VARCHAR DEFAULT NULL,
    time.timezone VARCHAR DEFAULT NULL,
    time.dst VARCHAR DEFAULT NULL,
    time.tz_db VARCHAR DEFAULT NULL,
    tipe.type_airport VARCHAR DEFAULT NULL,
    tipe.source VARCHAR
    CONSTRAINT pk PRIMARY KEY (airport_id)
);

CREATE TABLE IF NOT EXISTS airline3 (
        id_airline INTEGER NOT NULL,
        d.name VARCHAR DEFAULT NULL,
        d.alias VARCHAR DEFAULT NULL,
        kode.iata VARCHAR DEFAULT NULL,
        kode.icao VARCHAR DEFAULT NULL,
        pos.callsign VARCHAR DEFAULT NULL,
        pos.country VARCHAR DEFAULT NULL,
        pos.active_stat VARCHAR DEFAULT NULL
        CONSTRAINT pk PRIMARY KEY (id_airline)
);

CREATE TABLE IF NOT EXISTS routes4 (
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

CREATE TABLE IF NOT EXISTS airport4 (
    airport_id INTEGER NOT NULL,
    d.name_airport VARCHAR DEFAULT NULL,
    d.city VARCHAR DEFAULT NULL,
    d.country VARCHAR DEFAULT NULL,
    kode.iata VARCHAR DEFAULT NULL,
    kode.icao VARCHAR DEFAULT NULL,
    pos.latitude VARCHAR DEFAULT NULL,
    pos.longitude VARCHAR DEFAULT NULL,
    pos.altitude VARCHAR DEFAULT NULL,
    time.timezone VARCHAR DEFAULT NULL,
    time.dst VARCHAR DEFAULT NULL,
    time.tz_db VARCHAR DEFAULT NULL,
    tipe.type_airport VARCHAR DEFAULT NULL,
    tipe.source VARCHAR
    CONSTRAINT pk PRIMARY KEY (airport_id)
);

CREATE TABLE IF NOT EXISTS airline4 (
        id_airline INTEGER NOT NULL,
        d.name VARCHAR DEFAULT NULL,
        d.alias VARCHAR DEFAULT NULL,
        kode.iata VARCHAR DEFAULT NULL,
        kode.icao VARCHAR DEFAULT NULL,
        pos.callsign VARCHAR DEFAULT NULL,
        pos.country VARCHAR DEFAULT NULL,
        pos.active_stat VARCHAR DEFAULT NULL
        CONSTRAINT pk PRIMARY KEY (id_airline)
);