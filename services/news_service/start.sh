#!/bin/bash
service cron start
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 