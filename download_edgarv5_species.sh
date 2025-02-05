#!/bin/bash

base_url="https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/EDGAR/datasets/v2_FT2015_AP/monthly/"
declare -a pollutants=("BC" "CO" "NH3" "NMVOC" "NOx" "OC" "PM2.5" "PM10" "SO2")

for pollutant in "${pollutants[@]}"; do
  sectors=$(wget -q -O - ${base_url}${pollutant}/ | grep -oP '(?<=href=")[^"]*(?=/")')
  for sector in $sectors; do
    wget -r -np -nH --cut-dirs=7 -A "*_emi_nc.zip" ${base_url}${pollutant}/${sector}/ -P ./edgar_emi_nc_files
  done
done

