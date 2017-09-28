#!/bin/bash

startTime=$(date +%s)
endTime=$(date -d "$@" +%s)
timeToWait=$(($endTime- $startTime))
echo "Sleeping $timeToWait seconds until:"
date -d "@$endTime"
sleep $timeToWait
