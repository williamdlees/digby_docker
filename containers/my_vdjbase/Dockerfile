FROM python:3.7

MAINTAINER William Lees william@lees.org.uk

RUN \
  apt-get update && \
  apt-get -y install vim && \
  apt-get -y install telnet && \
  apt-get -y install git && \
  apt-get install -y ghostscript && \
  git clone https://williamlees@bitbucket.org/yaarilab/vdjbase.git /app && \
  cd /app

COPY app/local_settings.py /app/website/.
COPY app/start.sh /app/.
COPY app/website.wsgi /app/.
COPY app/install_r_packages /app/.
COPY app/install_vdjbaseviz /app/.
COPY app/samples.zip /app/.

RUN pip install -r /app/requirements.txt && \
  chmod +x /app/start.sh

RUN apt-get -y install  \
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
    rm -rf /tmp/downloaded_packages/ /tmp/*.rds 

RUN unzip /app/samples.zip -d /app/uploads

CMD ["/app/start.sh"]
#CMD ["tail -f /app/start.sh"]
