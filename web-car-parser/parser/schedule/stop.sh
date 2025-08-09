#!/bin/bash

docker-compose stop parser >> log/stop.log 2>&1

echo -e "Stop script started at: $(date)\n=================" >> log/stop.log
