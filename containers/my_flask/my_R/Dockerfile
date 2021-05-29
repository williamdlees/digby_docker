FROM python:3

MAINTAINER William Lees william@lees.org.uk

RUN mkdir /app

COPY app/* /app/

ENV R_BASE_VERSION 4.1.0

RUN   apt-get update && \
      apt-get -y install software-properties-common && \
      apt-key adv --keyserver keys.gnupg.net --recv-key 'E19F5F87128899B192B1A2C2AD5F960A256A04AF' && \
      add-apt-repository 'deb http://cloud.r-project.org/bin/linux/debian buster-cran40/' && \
      apt-get update && \
      apt-get -y install libcairo2-dev libgtk2.0-dev xvfb xauth xfonts-base libxt-dev libcurl4-openssl-dev libxml2-dev libssl-dev && \
      apt-get install -y --no-install-recommends \
		r-base \
		r-base-dev \
                r-base-core \
		r-recommended && \    
    Rscript /app/install_r_packages && \
    Rscript /app/install_vdjbaseviz && \
    rm -rf /tmp/downloaded_packages/ /tmp/*.rds && \
    rm -rf /app

