#!/bin/bash
service cron start

sleep 1

exec uvicorn src.main:app --host 0.0.0.0 --port 8000
