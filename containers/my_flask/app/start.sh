#!/bin/sh

#while true; do sleep 60; done

# Allow other containers to stabilise
sleep 20

cd /app

if [ -f /study_data/.gitkeep ]; then
  echo "initialising study_data"
  rm /study_data/.gitkeep
  cp -r static/init_study_data/* /study_data/.
fi

#while true; do sleep 60; done


echo "migrating database"
if [ ! -f migrations/README ]; then
  rm migrations/.gitkeep
  rm exports/.gitkeep
  flask db init
fi
flask db migrate
flask db upgrade

echo "starting cron"
service cron start
echo "starting RabbitMQ"
service rabbitmq-server restart 
echo "starting redis"
service redis-server restart
echo "starting celery workers"
celery -A app:celery worker -l INFO --logfile /config/log/celery.log&
echo "starting gunicorn"
export PYTHONUNBUFFERED=1
exec gunicorn -b :5000 --timeout 300 --limit-request-line 0 --worker-class gthread --keep-alive 5 --workers=10 --graceful-timeout 900 --access-logfile /config/log/access.log --error-logfile /config/log/error.log --capture-output --log-level debug app:app 

while true; do sleep 60; done

