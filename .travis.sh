#!/bin/bash
POSTGRES=$(docker run -d -P mdillon/postgis)
RANDOM_PORT=$(docker inspect $POSTGRES | \
	jq '.[0].NetworkSettings.Ports."5432/tcp"[0].HostPort' -r)

echo "Postgres $POSTGRES running on $RANDOM_PORT"
sed -i "s/5432/$RANDOM_PORT/g" base/travis.py

