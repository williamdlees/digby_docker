FROM python:3

MAINTAINER William Lees william@lees.org.uk

VOLUME /config

RUN mkdir /app

COPY app/* /app/

RUN   apt-get update && \
      apt-get -y install  \
      r-base \
      r-base-dev \
      r-recommended \
      r-cran-cairo \
      r-cran-optparse \
      r-cran-ggplot2 \
      r-cran-magrittr \
      r-cran-dplyr \
      r-cran-rcolorbrewer \
      r-cran-scales \
      r-cran-tigger \
      r-cran-stringr \
      r-cran-tidyr \
      r-cran-plotly \
      r-cran-plyr \
      r-cran-purrr \
      r-cran-readxl \
      r-cran-reshape2 \
      r-cran-alakazam \
      r-cran-seqinr \
      r-cran-gtools \
      r-cran-data.table \
      r-cran-dendextend \
      r-cran-gplots \
      r-cran-fastmatch \
      r-cran-xml2 \
      r-cran-devtools \
      r-cran-cairodevice && \
    Rscript /app/install_r_packages && \
    Rscript /app/install_vdjbaseviz && \
    rm -rf /tmp/downloaded_packages/ /tmp/*.rds && \
    rm -rf /app

