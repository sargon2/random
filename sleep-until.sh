#!/bin/bash

# todo: status updates

endTime=$(date -d "$@" +%s)
startTime=$(date +%s)
timeToWait=$(($endTime- $startTime))
echo -n "Sleeping $timeToWait seconds until "
date -d "@$endTime"
sleep $timeToWait
