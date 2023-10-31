FROM python:3.9-bullseye

MAINTAINER William Lees william@lees.org.uk

RUN mkdir /app

COPY app/* /app/

ENV R_BASE_VERSION 4.1.0

RUN gpg --keyserver keyserver.ubuntu.com --recv-key '95C0FAF38DB3CCAD0C080A7BDC78B2DDEABC47B7' && \
    gpg --armor --export '95C0FAF38DB3CCAD0C080A7BDC78B2DDEABC47B7' | gpg --dearmor | tee /usr/share/keyrings/cran.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/cran.gpg] https://cloud.r-project.org/bin/linux/debian bullseye-cran40/" | tee /etc/apt/sources.list.d/cran.list && \
    apt-get update && \
    apt-get -y install software-properties-common && \
    apt-get install -y --no-install-recommends \
                r-base \
                r-base-dev \
                r-base-core \
                r-recommended \
                r-cran-devtools

RUN apt-get -y install libcairo2-dev libgtk2.0-dev xvfb xauth xfonts-base libxt-dev libcurl4-openssl-dev libxml2-dev libssl-dev cmake
RUN apt-get -y install libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev
RUN apt-get -y install r-bioc-biostrings r-bioc-genomicalignments r-bioc-iranges

RUN Rscript /app/install_r_packages && \
    Rscript /app/install_vdjbaseviz && \
    rm -rf /tmp/downloaded_packages/ /tmp/*.rds && \
    rm -rf /app
