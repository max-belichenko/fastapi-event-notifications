#!/bin/bash

source venv/bin/activate
dramatiq notify_app.workers
