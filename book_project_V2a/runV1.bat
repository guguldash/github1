@echo on
start msedge http://localhost:8001/
uvicorn V1.app.main:app --reload --port 8001

REM gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
