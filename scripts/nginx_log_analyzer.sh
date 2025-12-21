#!/usr/bin/env bash

LOG_FILE=$1

if [ -z "$LOG_FILE" ]; then
  echo "Usage: nginx_log_analyzer.sh access.log"
  exit 1
fi

echo "Top slow requests:"
awk '{print $NF}' "$LOG_FILE" | sort -n | tail -20

echo "Request count:"
wc -l "$LOG_FILE"
