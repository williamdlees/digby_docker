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
  cd / && \
  mkdir /app/static/output && \
  mkdir /app/static/study_data && \
  mkdir /app/static/study_data/VDJbase && \
  mkdir /app/static/study_data/VDJbase/samples && \
  mkdir /app/static/study_data/VDJbase/samples/Human && \
  mkdir /app/static/study_data/VDJbase/db && \
  mkdir /app/static/study_data/VDJbase/db/Human && \
  mkdir /app/static/study_data/VDJbase/samples/Human/IGH && \
  unzip /app/Human_IGH_samples.zip -d /app/static/study_data/VDJbase/samples/Human/IGH && \
  mkdir /app/static/study_data/VDJbase/db/Human/IGH && \
  cp /app/Human_IGH_db.sqlite3 /app/static/study_data/VDJbase/db/Human/IGH/db.sqlite3 && \
  cp /app/Human_IGH_db_description.txt /app/static/study_data/VDJbase/db/Human/IGH/db_description.txt && \
  mkdir /app/static/study_data/VDJbase/samples/Human/IGK && \
  unzip /app/Human_IGK_samples.zip -d /app/static/study_data/VDJbase/samples/Human/IGK && \
  mkdir /app/static/study_data/VDJbase/db/Human/IGK && \
  cp /app/Human_IGK_db.sqlite3 /app/static/study_data/VDJbase/db/Human/IGK/db.sqlite3 && \
  cp /app/Human_IGK_db_description.txt /app/static/study_data/VDJbase/db/Human/IGK/db_description.txt && \
  mkdir /app/static/study_data/VDJbase/samples/Human/IGL && \
  unzip /app/Human_IGL_samples.zip -d /app/static/study_data/VDJbase/samples/Human/IGL && \
  mkdir /app/static/study_data/VDJbase/db/Human/IGL && \
  cp /app/Human_IGL_db.sqlite3 /app/static/study_data/VDJbase/db/Human/IGL/db.sqlite3 && \
  cp /app/Human_IGL_db_description.txt /app/static/study_data/VDJbase/db/Human/IGL/db_description.txt && \
  mkdir /app/static/study_data/VDJbase/samples/Human/TRB && \
  unzip /app/Human_TRB_samples.zip -d /app/static/study_data/VDJbase/samples/Human/TRB && \
  mkdir /app/static/study_data/VDJbase/db/Human/TRB && \
  cp /app/Human_TRB_db.sqlite3 /app/static/study_data/VDJbase/db/Human/TRB/db.sqlite3 && \
  cp /app/Human_TRB_db_description.txt /app/static/study_data/VDJbase/db/Human/TRB/db_description.txt && \
  mkdir "/app/static/study_data/VDJbase/samples/Rhesus Macaque" && \
  mkdir "/app/static/study_data/VDJbase/samples/Rhesus Macaque/IGH" && \
  unzip /app/Rhesus_Macaque_IGH_samples.zip -d "/app/static/study_data/VDJbase/samples/Rhesus Macaque/IGH" && \
  mkdir "/app/static/study_data/VDJbase/db/Rhesus Macaque" && \
  mkdir "/app/static/study_data/VDJbase/db/Rhesus Macaque/IGH" && \
  cp /app/Rhesus_Macaque_IGH_db.sqlite3 "/app/static/study_data/VDJbase/db/Rhesus Macaque/IGH/db.sqlite3" && \
  cp /app/Rhesus_Macaque_IGH_db_description.txt "/app/static/study_data/VDJbase/db/Rhesus Macaque/IGH/db_description.txt" && \
  mkdir "/app/static/study_data/VDJbase/samples/Crab-eating Macaque" && \
  mkdir "/app/static/study_data/VDJbase/samples/Crab-eating Macaque/IGH" && \
  unzip /app/Crab-eating_Macaque_IGH_samples.zip -d "/app/static/study_data/VDJbase/samples/Crab-eating Macaque/IGH" && \
  mkdir "/app/static/study_data/VDJbase/db/Crab-eating Macaque" && \
  mkdir "/app/static/study_data/VDJbase/db/Crab-eating Macaque/IGH" && \
  cp /app/Crab-eating_Macaque_IGH_db.sqlite3 "/app/static/study_data/VDJbase/db/Crab-eating Macaque/IGH/db.sqlite3" && \
  cp /app/Crab-eating_Macaque_IGH_db_description.txt "/app/static/study_data/VDJbase/db/Crab-eating Macaque/IGH/db_description.txt" && \
  mkdir "/app/static/study_data/Genomic" && \
  mkdir "/app/static/study_data/Genomic/samples" && \
  mkdir "/app/static/study_data/Genomic/samples/Rhesus_Macaque" && \
  mkdir "/app/static/study_data/Genomic/samples/Rhesus_Macaque/IGH" && \
  unzip /app/Rhesus_Macaque_IGH_genomic_samples.zip -d "/app/static/study_data/Genomic/samples/Rhesus_Macaque/IGH" && \
  mkdir "/app/static/study_data/Genomic/db" && \
  mkdir "/app/static/study_data/Genomic/db/Rhesus Macaque" && \
  mkdir "/app/static/study_data/Genomic/db/Rhesus Macaque/IGH" && \
  cp /app/Rhesus_Macaque_IGH_genomic_db.sqlite3 "/app/static/study_data/Genomic/db/Rhesus Macaque/IGH/db.sqlite3" && \
  cp /app/Rhesus_Macaque_IGH_genomic_db_description.txt "/app/static/study_data/Genomic/db/Rhesus Macaque/IGH/db_description.txt" && \
  mkdir "/app/static/study_data/Genomic/samples/Human" && \
  mkdir "/app/static/study_data/Genomic/samples/Human/IGL" && \
  unzip /app/Human_IGL_genomic_samples.zip -d "/app/static/study_data/Genomic/samples/Human/IGL" && \
  mkdir "/app/static/study_data/Genomic/db/Human" && \
  mkdir "/app/static/study_data/Genomic/db/Human/IGL" && \
  cp /app/Human_IGL_genomic_db.sqlite3 "/app/static/study_data/Genomic/db/Human/IGL/db.sqlite3" && \
  cp /app/Human_IGL_genomic_db_description.txt "/app/static/study_data/Genomic/db/Human/IGL/db_description.txt" && \
  mkdir "/app/static/study_data/Genomic/samples/Human/IGH" && \
  unzip /app/Human_IGH_genomic_samples.zip -d "/app/static/study_data/Genomic/samples/Human/IGH" && \
  mkdir "/app/static/study_data/Genomic/db/Human/IGH" && \
  cp /app/Human_IGH_genomic_db.sqlite3 "/app/static/study_data/Genomic/db/Human/IGH/db.sqlite3" && \
  cp /app/Human_IGH_genomic_db_description.txt "/app/static/study_data/Genomic/db/Human/IGH/db_description.txt" && \
  mv /app/static/study_data /app/static/init_study_data && \
  ln -s /study_data /app/static/study_data && \
  mkdir -p /backup/backup.daily && \
  mkdir -p /backup/backup.weekly && \
  mkdir -p /backup/backup.monthly && \
  crontab /app/cronjobs
 
CMD ["/app/start.sh"]
