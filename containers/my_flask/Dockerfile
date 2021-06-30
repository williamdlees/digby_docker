FROM my_r

MAINTAINER William Lees william@lees.org.uk

RUN \ 
  rm -rf /app && \
  apt-get update && \
  apt-get -y install vim && \
  apt-get -y install telnet && \
  apt-get -y install git && \
  apt-get -y install dos2unix && \
  apt-get -y install samtools && \
  apt-get -y install ghostscript && \
  apt-get -y install rabbitmq-server && \
  apt-get -y install redis-server && \
  apt-get -y install mariadb-client && \
  git clone https://github.com/williamdlees/digby_backend.git /app && \
  ln -s /config/migrations /app/migrations && \
  ln -s /config/exports /app/exports && \
  cd /app/static/gff && \
  dos2unix *.fasta && \
  for foo in *.fasta; do samtools faidx $foo; done && \
  chmod +x make_bam && \
  ./make_bam
COPY app/* /app/
COPY app/cronjobs /etc/crontabs/root

RUN \
  pip install "celery[redis]" && \
  pip install -r /app/requirements.txt && \
  pip install gevent && \
  chmod +x /app/start.sh && \
  chmod +x /app/do_backup.sh && \
  chmod +x /app/rotate.sh && \
  Rscript /app/install_vdjbaseviz && \
  cd / && \
  mkdir /app/static/output && \
  mkdir /app/static/study_data/VDJbase && \
  mkdir /app/static/study_data/VDJbase/samples && \
  mkdir /app/static/study_data/VDJbase/samples/Human && \
  mkdir /app/static/study_data/VDJbase/samples/Human/Human_IGH && \
  unzip /app/new_pipeline_samples.zip -d /app/static/study_data/VDJbase/samples/Human/IGH && \
  mkdir /app/static/study_data/VDJbase/samples/Human/Human_TRB && \
  unzip /app/TRB_samples.zip -d /app/static/study_data/VDJbase/samples/Human/TRB && \
  mkdir /app/static/study_data/VDJbase/db && \
  mkdir /app/static/study_data/VDJbase/db/Human && \
  mkdir /app/static/study_data/VDJbase/db/Human/IGH && \
  cp /app/new_pipeline_db.sqlite3 /app/static/study_data/VDJbase/db/Human/IGH/db.sqlite3 && \
  cp /app/new_pipeline_db_description.txt /app/static/study_data/VDJbase/db/Human/IGH/db_description.txt && \
  mkdir /app/static/study_data/VDJbase/db/Human/TRB && \
  cp /app/TRB_db.sqlite3 /app/static/study_data/VDJbase/db/Human/TRB/db.sqlite3 && \
  cp /app/TRB_db_description.txt /app/static/study_data/VDJbase/db/Human/TRB/db_description.txt && \
  mv /app/static/study_data /app/static/init_study_data && \
  ln -s /study_data /app/static/study_data && \
  mkdir -p /backup/backup.daily && \
  mkdir -p /backup/backup.weekly && \
  mkdir -p /backup/backup.monthly && \
  crontab /app/cronjobs
 
CMD ["/app/start.sh"]
