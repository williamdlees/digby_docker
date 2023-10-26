FROM my_r

MAINTAINER William Lees william@lees.org.uk

ARG backend_repo_url="https://github.com/williamdlees/digby_backend.git"
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
  apt-get -y install cron

# ensure we don't use the cache if the repo has changed
ADD "https://api.github.com/repos/williamdlees/digby_backend/commits?per_page=1" latest_commit


RUN \
  git clone "$backend_repo_url" /app && \
  ln -s /config/migrations /app/migrations && \
  ln -s /config/exports /app/exports && \
  cd /app/static/gff && \
  dos2unix *.fasta && \
  for foo in *.fasta; do samtools faidx $foo; done && \
  chmod +x make_bam && \
  ./make_bam && \
  pip install "celery[redis]" && \
  pip install -r /app/requirements.txt && \
  pip install gevent

COPY app/* /app/
COPY app/cronjobs /etc/crontabs/root

RUN \
  Rscript /app/install_vdjbaseviz && \
  chmod +x /app/start.sh && \
  chmod +x /app/rotate.sh && \
  ln -s /study_data /app/static/study_data && \
  mkdir -p /backup/backup.daily && \
  mkdir -p /backup/backup.weekly && \
  mkdir -p /backup/backup.monthly && \
  crontab /app/cronjobs

CMD ["/app/start.sh"]