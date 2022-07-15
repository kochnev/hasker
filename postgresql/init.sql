
create user :db_user with password ':db_password';
alter user :db_user createdb;
alter user :db_user set client_encoding to 'utf8';
alter user :db_user set default_transaction_isolation to 'read committed';
alter user :db_user set timezone to 'UTC';

create database :db_name owner :db_user ;