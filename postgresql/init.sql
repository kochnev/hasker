
create user :db_user with password ':db_password';
alter role :db_user set client_encoding to 'utf8';
alter role :db_user set default_transaction_isolation to 'read committed';
alter role :db_user set timezone to 'UTC';

create database :db_name owner :db_user
