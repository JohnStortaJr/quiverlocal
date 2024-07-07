#!/usr/bin/bash

FILENAME=localtest01.json

DOMAIN_NAME=$(jq -r '.domain_name' $FILENAME)
DB_NAME=$(jq -r '.db_name' $FILENAME)
DOMAIN_CONF=$(jq -r '.domain_conf' $FILENAME)

echo "Domain: $DOMAIN_NAME"
echo "Database: $DB_NAME"
echo "Config: $DOMAIN_CONF"
#echo "Names: $names"

NEWDOMAIN=localtest04
NEWDBNAME=localtest04_db
tmp=$(mktemp)
#jq --arg n $NEWDOMAIN '.domain_name = $n' $FILENAME > $tmp && mv $tmp $FILENAME
jq --arg n $NEWDOMAIN --arg p $NEWDBNAME '.domain_name = $n | .db_name = $p' $FILENAME > $tmp && mv $tmp $FILENAME

#jq '.domain_name = "hardcodedvalue"' $FILENAME > "$tmp" && mv "$tmp" $FILENAME

DOMAIN_NAME=$(jq -r '.domain_name' $FILENAME)
DB_NAME=$(jq -r '.db_name' $FILENAME)
DOMAIN_CONF=$(jq -r '.domain_conf' $FILENAME)

echo "Domain: $DOMAIN_NAME"
echo "Database: $DB_NAME"
echo "Config: $DOMAIN_CONF"
#echo "Names: $names"

