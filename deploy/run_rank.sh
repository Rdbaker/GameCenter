#!/usr/bin/env bash

cd /opt/rank/GameCenter
. /opt/rank/conf.sh
gunicorn manage:application --bind 0.0.0.0:8000 --workers 4
