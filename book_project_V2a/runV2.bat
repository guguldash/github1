@echo on
start msedge http://localhost:8002/
uvicorn V2.app.main:app --reload --port 8002

REM gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
