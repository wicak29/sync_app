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


Table Airport :
UPDATE airport2 SET timezone='9', dst='A' WHERE airport_id=1;