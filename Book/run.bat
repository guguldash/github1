@echo off
start msedge http://localhost:23905/
uvicorn app.main:app --reload --port 23905

