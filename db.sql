BEGIN TRANSACTION;
DROP TABLE IF EXISTS data_login;
DROP TABLE IF EXISTS data_user;
DROP TABLE IF EXISTS data_mobile;
DROP TABLE IF EXISTS data_app;
DROP TABLE IF EXISTS data_code;
DROP TABLE IF EXISTS data_access;
DROP TRIGGER IF EXISTS data_code_cleaner_update;
DROP TRIGGER IF EXISTS data_code_cleaner_insert;

CREATE TABLE data_login (login TEXT UNIQUE, password TEXT);
INSERT INTO "data_login" VALUES('olyakosyura','qwerty');
INSERT INTO "data_login" VALUES('barnybrown','0000');
INSERT INTO "data_login" VALUES('Nick','qazxsw');
INSERT INTO "data_login" VALUES('Marina','1234567890');
INSERT INTO "data_login" VALUES('happy','1');

CREATE TABLE data_user (id INTEGER PRIMARY KEY, login TEXT UNIQUE, firstname TEXT, email TEXT, mobile TEXT);
INSERT INTO "data_user" VALUES(1,'olyakosyura','Olga','olyakosyura.15@mail.ru','1,4,6');
INSERT INTO "data_user" VALUES(2,'barnybrown','Nick','barnybrown@mail.ru','5');
INSERT INTO "data_user" VALUES(3,'Nick','Nick','nick@yandex.ru','1,4');
INSERT INTO "data_user" VALUES(4,'Marina','Marina','Marina@gmail.com','1,2,3');
INSERT INTO "data_user" VALUES(5,'happy','Olya','kosyura@mail.ru','3,4,5');

CREATE TABLE data_mobile (id INTEGER PRIMARY KEY, firm TEXT, model TEXT, color TEXT, cost REAL, description TEXT, users text);
INSERT INTO "data_mobile" VALUES(1,'Nokia','3310','Blue',1950.0,'��������������� ������� ������� ����� Nokia. ������� � ��������� �������� 2000 ����, ����� �� ����� ������ 3210. Nokia 3310 - ���� �� ����� ������� ������� � �������: ���� ������� ����� 126 ��������� ���������','1,3,4');
INSERT INTO "data_mobile" VALUES(2,'Apple','Iphone 6','Gold',65990.0,'�������� , ���������� �� iOS 8, �������������� 9 �������� 2014 ����. ��������� ������ ���� ����������� ��������� �� ��������� � ����������� ��������. ������� - ����� 7 ��, ��� ����� ������� ������.','4');
INSERT INTO "data_mobile" VALUES(3,'Samsung','Galaxy S5','White',19990.0,'�������� ������ ��������� ������� Galaxy S, �������������� ��������� Samsung Electronics 25 ������� 2014 ���� �� MWC � ���������. �������� � ������� 11 ������ 2014 ���� � 125 �������.','4,5');
INSERT INTO "data_mobile" VALUES(4,'LG','Optimus G','Blue',17990.0,'The LG Optimus G is a smartphone designed and manufactured by LG Electronics. It was announced on September 19, 2012;On January 18, 2013, LG announced that the device reached 1 million in sales four months after its release in Korea, Japan, Canada, and the U.S. The LG Optimus G is also closely related to the Nexus 4 with similar specifications and a similar design.','1,3,5');
INSERT INTO "data_mobile" VALUES(5,'LG','Nexus 4','White',16850.0,'�������� �������� Google, ���������� ��� ����������� ������������ ������� Android. ���������� ��������� ���������� LG Electronics � Google Inc. �������� �������������� ���������� ��������� � ������� ���������� Google Nexus.�������� ��� ����������� 29 ������� 2012 ���� ������ � ��������� Nexus 10 � ������������ �������� Android 4.2 Jelly Bean. ������� ���������� ���������� 13 ������ 2012 ����.','2,5');
INSERT INTO "data_mobile" VALUES(6,'LG','Nexus 5','Black',23490.0,'����������� �������� �� ������� Google Nexus 2013 ����, ���������� ��� ����������� ������������ ������� Android.���������� ���� ����������� ����������� �������� �������� LG Electronics � Google Inc. ������ ��������, ���������� �� ������������ ������� Android ������ 4.4 KitKat. ����������� ����� ��������� 31 ������� 2013 ����','1');

CREATE TABLE data_app (client_id TEXT PRIMARY KEY, client_secret TEXT, login TEXT);
INSERT INTO "data_app" VALUES ('12345','123456789','olyakosyura');

CREATE TABLE data_code (login TEXT, client_id TEXT, code TEXT, expiration_time INTEGER, redirect_uri TEXT, PRIMARY KEY(login, client_id));
CREATE TABLE data_access (client_id TEXT, access_token TEXT UNIQUE, refresh_token TEXT UNIQUE, expiration_time INTEGER);

CREATE TRIGGER data_code_cleaner_update UPDATE ON data_code
BEGIN
	DELETE FROM data_code WHERE strftime('%s', 'now') >= expiration_time;
END;

CREATE TRIGGER data_code_cleaner_insert INSERT ON data_code
BEGIN
	DELETE FROM data_code WHERE strftime('%s', 'now') >= expiration_time;
END;

COMMIT;