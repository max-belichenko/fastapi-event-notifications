#!/bin/bash

source venv/bin/activate
uvicorn notify_app.web_service:app --reload
