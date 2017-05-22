Table Routes :
-------------------------------------------------------
INSERT INTO routes2 (id_route, airline, id_airline, src_airport, id_src_airport, dst_airport, id_dst_airport, codeshare, stop_val, equipment) VALUES (101,'ZM','19016','AER','2965','KZN','2990','',0,'CR2');
INSERT INTO routes2 (id_route, airline, id_airline, src_airport, id_src_airport, dst_airport, id_dst_airport, codeshare, stop_val, equipment) VALUES (102,'ZM','19016','AER','2965','KZN','2990','',0,'CR2');
DELETE FROM routes2 WHERE id_route = 100;
UPDATE routes2 SET codeshare='Y' WHERE id_route=1;
UPDATE routes2 SET codeshare='Y', stop_val=1 WHERE airline='ZM';
UPDATE routes2 SET airline='WW', id_airline='1948' WHERE id_route=102;
INSERT INTO routes2 (id_route, airline, id_airline, src_airport, id_src_airport, dst_airport, id_dst_airport, codeshare, stop_val, equipment) VALUES (103,'QG','19305','CGK','3275','SUB','3928','',0,'320');
INSERT INTO routes2 (id_route, airline, id_airline, src_airport, id_src_airport, dst_airport, id_dst_airport, codeshare, stop_val, equipment) VALUES (104,'QG','19305','DPS','3940','SUB','3928','',0,'CR2');
INSERT INTO routes2 (id_route, airline, id_airline, src_airport, id_src_airport, dst_airport, id_dst_airport, codeshare, stop_val, equipment) VALUES (105,'QG','19305','SUB','3928','DPS','3940','',0,'CR2');
UPDATE routes2 SET codeshare='Y', stop_val=1 WHERE id_route=104;

Table Airline :
-------------------------------------------------------
UPDATE airline2 SET iata='PR', callsign='PRIVATE', country='Unknown' WHERE id_airline=1;
INSERT INTO airline2 (id_airline, name, alias, iata, icao, callsign, country, active_stat) VALUES (21318,'Garuda Indonesia','\N','GA','GIA','INDONESIA','Indonesia','Y');


Table Airport : select * from airport2 order by airport_id desc;
--------------------------------------------------------
UPDATE airport2 SET timezone='9', dst='A' WHERE airport_id=1;
INSERT INTO airport2 (airport_Id, name_airport, city, country, iata, icao, latitude, longitude, altitude, timezone, dst, tz_db, type_airport, source) VALUES (12059,'Goroka Airport','Goroka','Papua New Guinea','GKA','AYGA','-6.081689834590001','145.391998291','5282','10','U','Pacific/Port_Moresby','airport','OurAirports');


kueri select : 
--------------------------------------------
SELECT a.*,b.country  FROM routes2 a JOIN airline2 b on a.id_airline = b.id_airline where a.id_route=410;
SELECT id_airline, count(id_route) FROM routes2 GROUP BY id_airline;
SELECT a.id_airline,b.name, count(a.id_route) FROM routes2 a JOIN airline2 b on a.id_airline = b.id_airline GROUP BY a.id_airline;
SELECT id_airline, count(id_route) FROM routes2 GROUP BY id_airline HAVING COUNT(*) > 100;
SELECT DISTINCT id_airline from routes2;