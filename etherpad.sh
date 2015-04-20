#!/bin/bash -ex

git clone http://github.com/ether/etherpad-lite
cd etherpad-lite
npm install sqlite3
cp settings.json.template settings.json
sed -i "/dbType/ s/dirty/sqlite/" settings.json
sed -i "/filename/ s/dirty.db/my-etherpad-db.sqlite/" settings.json
./bin/run.sh
