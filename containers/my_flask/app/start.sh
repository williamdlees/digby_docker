#!/bin/sh

#while true; do sleep 60; done

cd /app
echo "starting RabbitMQ"
service rabbitmq-server restart 
echo "starting redis"
service redis-server restart
echo "starting celery workers"
celery -A app:celery worker -l INFO --logfile /config/log/celery.log&
echo "starting gunicorn"
export PYTHONUNBUFFERED=1
exec gunicorn -b :5000 --timeout 300 --limit-request-line 0 --worker-class gthread --keep-alive 5 --workers=10 --graceful-timeout 900 --access-logfile /config/log/access.log --error-logfile /config/log/error.log --capture-output --log-level debug app:app 
