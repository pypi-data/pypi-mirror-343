#!/bin/bash
# scripts/run_api.sh

uvicorn									\
	app.api.main:app						\
	--host 0.0.0.0							\
	--port 8000							\
	--reload
