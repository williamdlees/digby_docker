#!/bin/sh

cd /app
cp -r assets/* /assets/.
rm -rf /scratch/*
mkdir /scratch/graphs /scratch/graphs/alleles_appearance_graph /scratch/graphs/freq_distributions /scratch/graphs/genesXalleles /scratch/graphs/heterozygous_graph && \
mkdir /scratch/graphs/merge_genotype /scratch/graphs/genotypes /scratch/graphs/html_genotypes /scratch/tables /scratch/tables/merge_genotypes

echo "staring gunicorn"
exec gunicorn --workers=9 -b :5001 --access-logfile - --error-logfile - website.wsgi
