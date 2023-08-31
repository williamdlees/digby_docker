FROM python:3.9.6-bullseye

MAINTAINER William Lees william@lees.org.uk

RUN mkdir /app

COPY app/* /app/

ENV R_BASE_VERSION 4.1.0

RUN apt-get update && \
      apt-get -y install software-properties-common && \
      apt-get install -y --no-install-recommends \
		r-base \
		r-base-dev \
		r-base-core \
		r-recommended && \    
      apt-get -y install libcairo2-dev libgtk2.0-dev xvfb xauth xfonts-base libxt-dev libcurl4-openssl-dev libxml2-dev libssl-dev cmake && \
	  apt-get -y install libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev && \
    Rscript /app/install_r_packages && \
    Rscript /app/install_vdjbaseviz && \
    rm -rf /tmp/downloaded_packages/ /tmp/*.rds && \
    rm -rf /app

