#!/bin/bash

#export to .json file
mongoexport --host ds054128.mlab.com --port 54128 --username $1 --password $2 --collection testCollection --db handicap --out testCollection.json

#start mongo server
mongod --dbpath /c/tmp/data/db/ &

sleep 20

#
mongoimport --db foot --collection games --file testCollection.json


