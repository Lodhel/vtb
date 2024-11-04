#!/bin/sh

start() {
    docker-compose up -d --build
}

stop() {
    docker-compose -f docker-compose.yml down
}

if [ -n "$1" ]; then
    case "$1" in
    start) start ;;
    stop) stop ;;
    restart) stop ; start ;;
    load_cbr_data) docker exec vtb24_fast_api_mvp_1 sh load_cbr_data.sh ;;
    *) echo "$1 is not an option." ;;
    esac
else
    echo "No parameters found."
fi
