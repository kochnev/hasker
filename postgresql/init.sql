create user hasker_admin with password '123456789';
alter role hasker_admin set client_encoding to 'utf8';
alter role hasker_admin set default_transaction_isolation to 'read committed';
alter role hasker_admin set timezone to 'UTC';

create database hasker owner hasker_admin
