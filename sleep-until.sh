#!/bin/bash
DATE=date

if [[ "$OSTYPE" == "darwin"* ]]; then
    DATE=gdate
fi

endTime=$($DATE -d "$@" +%s)
while true
do
    startTime=$($DATE +%s)
    timeToWait=$(($endTime- $startTime))
    if [ "$timeToWait" -le "0" ]
    then
        exit 0
    fi
    echo -n "Sleeping $timeToWait seconds until "
    $DATE -d "@$endTime"
    timeToWait=$((($timeToWait+9) / 10))
    if [ "$timeToWait" -lt "1" ]
    then
        timeToWait=1
    fi
    sleep $timeToWait
done
