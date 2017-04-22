UPSERT INTO routes2 (id_route, airline, id_airline, src_airport, id_src_airport, dst_airport, id_dst_airport, codeshare, stop_val, equipment) VALUES (101,'ZM','19016','AER','2965','KZN','2990','',0,'CR2');
UPSERT INTO routes2 (id_route, airline, id_airline, src_airport, id_src_airport, dst_airport, id_dst_airport, codeshare, stop_val, equipment) VALUES (102,'ZM','19016','AER','2965','KZN','2990','',0,'CR2');
DELETE FROM routes2 WHERE id_route = 100;
UPSERT INTO routes2 (id_route,codeshare) SELECT id_route,'Y' FROM routes2 WHERE  id_route=1;
UPSERT INTO routes2 (id_route,codeshare,stop_val) SELECT id_route,'Y',1 FROM routes2 WHERE  airline='ZM';
UPSERT INTO routes2 (id_route,airline,id_airline) SELECT id_route,'WW','1948' FROM routes2 WHERE  id_route=102;
UPSERT INTO routes2 (id_route, airline, id_airline, src_airport, id_src_airport, dst_airport, id_dst_airport, codeshare, stop_val, equipment) VALUES (104,'QG','19305','DPS','3940','SUB','3928','',0,'CR2');
UPSERT INTO routes2 (id_route, airline, id_airline, src_airport, id_src_airport, dst_airport, id_dst_airport, codeshare, stop_val, equipment) VALUES (105,'QG','19305','SUB','3928','DPS','3940','',0,'CR2');
UPSERT INTO routes2 (id_route,codeshare,stop_val) SELECT id_route,'Y',1 FROM routes2 WHERE  id_route=104;
