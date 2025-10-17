FROM python:3.9-bookworm

LABEL org.opencontainers.image.authors="william@lees.org.uk"

RUN mkdir /app

COPY app/* /app/

ENV R_BASE_VERSION 4.2.2

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
                r-base=4.2.2.20221110-2 \
                r-base-dev=4.2.2.20221110-2 \
                r-base-core=4.2.2.20221110-2
				
RUN apt-get -y install libcairo2-dev libgtk2.0-dev xvfb xauth xfonts-base libxt-dev libcurl4-openssl-dev libxml2-dev libssl-dev cmake
RUN apt-get -y install libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev libgit2-dev
RUN apt-get -y install r-bioc-biostrings r-bioc-genomicalignments r-bioc-iranges

RUN Rscript /app/install_r_packages && \
    Rscript /app/install_vdjbaseviz && \
    rm -rf /tmp/downloaded_packages/ /tmp/*.rds \
    rm -rf app
