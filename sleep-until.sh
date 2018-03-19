#!/bin/bash

endTime=$(date -d "$@" +%s)
while true
do
    startTime=$(date +%s)
    timeToWait=$(($endTime- $startTime))
    if [ "$timeToWait" -le "0" ]
    then
        exit 0
    fi
    echo -n "Sleeping $timeToWait seconds until "
    date -d "@$endTime"
    timeToWait=$((($timeToWait+9) / 10))
    if [ "$timeToWait" -lt "1" ]
    then
        timeToWait=1
    fi
    sleep $timeToWait
done
