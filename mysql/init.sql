-- Host: localhost    Database: icecreamshopdb
-- ------------------------------------------------------

CREATE DATABASE IF NOT EXISTS icecreamshopdb ;

CREATE USER 'admin'@'%' identified by 'mySqlPass**123';
GRANT ALL PRIVILEGES on *.* to 'admin'@'%';