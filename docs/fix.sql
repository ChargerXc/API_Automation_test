CREATE TABLE el_sys_depart_bak AS SELECT * FROM el_sys_depart;
TRUNCATE TABLE el_sys_depart;
INSERT INTO el_sys_depart SELECT * FROM el_sys_depart_bak;
DROP TABLE el_sys_depart_bak;