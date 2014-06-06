#!/bin/sh

mkdir -p data
cd data

wget -O 'kplr000757450-2009166043257_llc.fits' 'http://exoplanetarchive.ipac.caltech.edu:80/data/ETSS//Kepler/000/301/03/kplr000757450-2009166043257_llc.fits' -a raw_13205.log
wget -O kplr010874614-2009131105131_llc.fits http://exoplanetarchive.ipac.caltech.edu/data/ETSS/Kepler/000/294/95/kplr010874614-2009131105131_llc.fits -a wget_etss_15480.log
