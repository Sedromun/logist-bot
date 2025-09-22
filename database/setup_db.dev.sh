#!/bin/bash

psql -U postgres <<-EOSQL
    CREATE DATABASE "pallets";
EOSQL

psql -U postgres -d "pallets" <<-EOSQL
    CREATE SCHEMA IF NOT EXISTS "users";
EOSQL

