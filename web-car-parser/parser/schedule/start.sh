#!/bin/bash

docker-compose up -d parser >> log/start.log 2>&1

echo -e "Start script started at: $(date)\n=================" >> log/start.log
