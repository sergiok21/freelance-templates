#!/bin/bash


if [[ -f "$FILE" ]]; then
  JSON=$(cat "$FILE")
  redis-cli json.set "$KEY" . "$JSON"
else
  echo "File not found: $FILE"
fi
