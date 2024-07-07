#!/usr/bin/bash

FILENAME=localtest01.json

DOMAIN_NAME=$(jq -r '.domain_name' $FILENAME)
DB_NAME=$(jq -r '.db_name' $FILENAME)
DOMAIN_CONF=$(jq -r '.domain_conf' $FILENAME)

echo "Domain: $DOMAIN_NAME"
echo "Database: $DB_NAME"
echo "Config: $DOMAIN_CONF"
#echo "Names: $names"
