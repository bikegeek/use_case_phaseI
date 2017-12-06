#!/bin/ksh
#create output directory
mkdir ${DATA_OUTmain}/grid2grid
export DATA_OUT=${DATA_OUTmain}/grid2grid
echo "------------------------------------------------------------"
echo "-------------> Grid-to-Grid Output Directory"
echo "${DATA_OUT}"
export DATA_OUTmodel="${DATA_OUT}/model"
export DATA_OUTimgs="${DATA_OUT}/imgs"
export DATA_OUTlog="${DATA_OUT}/log"
#create branches of output directory
mkdir ${DATA_OUTmodel}
mkdir ${DATA_OUTimgs}
mkdir ${DATA_OUTlog}
#create output directories for models
for model_fcst in $model_fcst_list ; do
  mkdir ${DATA_OUTmodel}/${model_fcst}
  mkdir ${DATA_OUTmodel}/${model_fcst}/pres
  mkdir ${DATA_OUTmodel}/${model_fcst}/anom
  mkdir ${DATA_OUTmodel}/${model_fcst}/sfc
  for fcycle in $fcycle_list ; do
     mkdir ${DATA_OUTmodel}/${model_fcst}/pres/${fcycle}Z
     mkdir ${DATA_OUTmodel}/${model_fcst}/anom/${fcycle}Z
     mkdir ${DATA_OUTmodel}/${model_fcst}/sfc/${fcycle}Z
     mkdir ${DATA_OUTmodel}/${model_fcst}/pres/${fcycle}Z/FULL
     mkdir ${DATA_OUTmodel}/${model_fcst}/anom/${fcycle}Z/FULL
     mkdir ${DATA_OUTmodel}/${model_fcst}/sfc/${fcycle}Z/FULL
     for reg in ${regions_list} ; do
        mkdir ${DATA_OUTmodel}/${model_fcst}/pres/${fcycle}Z/${reg}
        mkdir ${DATA_OUTmodel}/${model_fcst}/anom/${fcycle}Z/${reg}
     done 
     for sreg in ${sfc_regions_list} ; do
        mkdir ${DATA_OUTmodel}/${model_fcst}/sfc/${fcycle}Z/${sreg}
     done 
  done  
done
#create output directories for images
for fcycle in $fcycle_list ; do
  mkdir ${DATA_OUTimgs}/${fcycle}Z
  mkdir ${DATA_OUTimgs}/${fcycle}Z/FULL
  for reg in ${regions_list} ; do
     mkdir ${DATA_OUTimgs}/${fcycle}Z/${reg}
  done
  for sreg in ${sfc_regions_list} ; do
     if [ ! -d ${DATA_OUTimgs}/${fcycle}Z/${sreg} ] ; then
        mkdir ${DATA_OUTimgs}/${fcycle}Z/${sreg}
     fi
  done
done
