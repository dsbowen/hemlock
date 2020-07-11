web: gunicorn -k eventlet app:app
worker: rq worker -u $REDIS_URL hemlock-task-queue