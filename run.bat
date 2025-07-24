@echo off
cd app
uvicorn main:app --reload --host localhost --port 8000