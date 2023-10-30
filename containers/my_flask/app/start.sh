#!/bin/sh

#while true; do sleep 60; done

# Allow other containers to stabilise
sleep 20

cp /config/secret.cfg /app/secret.cfg
cp /config/do_backup.sh /app/do_backup.sh
chmod +x /app/do_backup.sh

cd /app

echo "configuring study data"
if [ ! -f /config/study_data_conf.csv ]; then
  cp /app/sample_study_data_conf.csv /config/study_data_conf.csv 
fi

python /app/dataSeparationVdjbase.py


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
celery -A app:celery worker -c $CELERY_WORKERS -l INFO --logfile /config/log/celery.log&
echo "starting gunicorn"
export PYTHONUNBUFFERED=1
exec gunicorn -b :5000 --timeout 300 --limit-request-line 0 --worker-class gthread --keep-alive 5 --workers=$GUNICORN_WORKERS --graceful-timeout 900 --access-logfile /config/log/access.log --error-logfile /config/log/error.log --capture-output --log-level debug app:app 

while true; do sleep 60; done