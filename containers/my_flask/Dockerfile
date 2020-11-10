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
  git clone https://github.com/williamdlees/digby_backend.git /app && \
  ln -s /config/migrations /app/migrations && \
  ln -s /config/exports /app/exports && \
  cd /app/static/gff && \
  dos2unix *.fasta && \
  for foo in *.fasta; do samtools faidx $foo; done && \
  chmod +x make_bam && \
  ./make_bam
COPY app/* /app/

RUN \
  pip install "celery[redis]" && \
  pip install -r /app/requirements.txt && \
  pip install gevent && \
  chmod +x /app/start.sh && \
  cd / && \
  mkdir /app/static/output && \
  mkdir /app/static/study_data/VDJbase/samples && \
  mkdir /app/static/study_data/VDJbase/samples/Human && \
  mkdir /app/static/study_data/VDJbase/samples/Human/Human_IGH && \
  unzip /app/samples.zip -d /app/static/study_data/VDJbase/samples/Human/Human_IGH && \
  mkdir /app/static/study_data/VDJbase/samples/Human/New_Pipeline_IGH && \
  unzip /app/new_pipeline_samples.zip -d /app/static/study_data/VDJbase/samples/Human/New_Pipeline_IGH && \
  mv /app/static/study_data /app/static/init_study_data && \
  ln -s /study_data /app/static/study_data
 
CMD ["/app/start.sh"]
