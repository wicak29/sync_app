CREATE TABLE IF NOT EXISTS daerah3 (
        iddaerah INTEGER NOT NULL,
        d.kode VARCHAR DEFAULT NULL,
        d.nama VARCHAR DEFAULT NULL,
        det.date_change DATE
     CONSTRAINT pk PRIMARY KEY (iddaerah)
);

