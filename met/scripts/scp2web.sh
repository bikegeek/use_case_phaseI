#!/bin/ksh
webpage_dir="/home/people/emc/www/htdocs/gmb/mpr/prnemsgiv_met"
cycle="00"
##########################  GRID2GRID   ####################################
############################################################################
in_dir="/global/save/Mallory.Row/VRFY/met/out/grid2grid/imgs/${cycle}Z"
out_dir="${webpage_dir}/www/grid2grid/${cycle}Z/www/imgs"
###########
stats="ac bias rms msess rsd emd epv pcor"
regions="FULL NHX SHX TRO PNA"
for stat in ${stats} ; do
    for reg in ${regions} ; do
        scp ${in_dir}/${reg}/${stat}* mrow@emcrzdm.ncep.noaa.gov:${out_dir}/${stat}/.
     done
done
###########
#regions="FULL NHX SHX TRO NPO SPO NAO SAO CAM NSA"
#for reg in ${regions} ; do
#     scp ${in_dir}/${reg}/fbar* mrow@emcrzdm.ncep.noaa.gov:${out_dir}/reg/.
#done
##############################################################################


###########################    PRECIP    #####################################
##############################################################################
#in_dir="/global/save/Mallory.Row/VRFY/met/out_precip/precip/imgs/${cycle}Z"
#out_dir="${webpage_dir}/www/precip/www/imgs/precip"
#regions="CONUS"
#for reg in ${regions} ; do
#    scp ${in_dir}/${reg}/* mrow@emcrzdm.ncep.noaa.gov:${out_dir}/.
#done
##############################################################################


###########################   GRID2OBS   #####################################
##############################################################################
#in_dir="/global/save/Mallory.Row/VRFY/met/out_grid2obs/grid2obs/imgs/${cycle}Z"
#out_dir="${webpage_dir}/www/grid2obs/${cycle}Z/www/imgs/g2oair"
###########
#stats="bias rms"
#regions="G236"
#for stat in ${stats} ; do
#    for reg in ${regions} ; do
#        scp ${in_dir}/${reg}/${stat}* mrow@emcrzdm.ncep.noaa.gov:${out_dir}/${stat}/.
#     done
#done
###########
#in_dir="/global/save/Mallory.Row/VRFY/met/out_grid2obs/grid2obs/imgs/${cycle}Z"
#out_dir="${webpage_dir}/www/grid2obs/${cycle}Z/www/imgs/g2osfc"
#stats="bias rms"
#regions="EAST"
#for stat in ${stats} ; do
#    for reg in ${regions} ; do
#        scp ${in_dir}/${reg}/${stat}* mrow@emcrzdm.ncep.noaa.gov:${out_dir}/${stat}/.
#     done
#done
##############################################################################
