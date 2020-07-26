web: gunicorn -k eventlet -w 1 app:app
worker: rq worker -u $REDIS_URL hemlock-task-queue