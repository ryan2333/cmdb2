CREATE DATABASE IF NOT EXISTS cmdb default character set utf8 COLLATE utf8_general_ci;

use cmdb;
DROP TABLE IF EXISTS users;
CREATE TABLE users(
	id int not null primary key auto_increment,
	username varchar(20),
	password varchar(32),
	email varchar(32),
	user_type int default 1,
	status int default 0
)engine=innodb default charset=utf8;


DROP TABLE IF EXISTS oses;
CREATE TABLE oses(
	id int not null primary key auto_increment,
	osname varchar(20),
	status int
)engine=innodb default charset=utf8;


DROP TABLE IF EXISTS idcs;
CREATE TABLE idcs(
	id int not null primary key auto_increment,
	idcName varchar(64),
	pods varchar(64),
	bankwidth int,
	t_contact varchar(16),
	t_phone varchar(16),
	kf_contact varchar(16),
	kf_phone varchar(16),
	start_date date,
	end_date date,
	address varchar(255),
	status int
)engine=innodb default charset=utf8;

DROP TABLE IF EXISTS physics_host;
CREATE TABLE physics_host(
	id int not null primary key auto_increment,
	sn varchar(64),
	ip varchar(24),
	vendor varchar(32),
	model varchar(32),
	os int,
	cpuModel varchar(24),
	mem varchar(32),
	PurchaseDate date,
	warranty int,
	bIdc int,
	bPod int,
	bPu int,
	status int
)engine=innodb default charset=utf8;

DROP TABLE IF EXISTS vms;
CREATE TABLE vms(
	id int not null primary key auto_increment,
	vmid varchar(64),
	application varchar(32),
	ip varchar(24),
	os int,
	cpuThread int,
	mem int,
	disk int,
	bHost int,
	status int
)engine=innodb default charset=utf8;