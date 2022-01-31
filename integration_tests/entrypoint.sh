#!/bin/bash

function wait_for_service () {
  host=$1
  port=$2
  timeout=${3:-60}
  seconds=0
  while [ "$seconds" -lt "$timeout" ] && ! nc -z -w1 $host $port
  do
    seconds=$((seconds+1))
    sleep 1
  done

  if [ "$seconds" -ge "$timeout" ]; then
    exit 1
  fi
}

echo Waiting for rabbitmq...
wait_for_service rabbitmq 5672

echo Starting bus services...
flask run --host 0.0.0.0
