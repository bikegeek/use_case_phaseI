#!/bin/ksh
#create output directory
mkdir ${DATA_OUTmain}/precip
export DATA_OUT=${DATA_OUTmain}/precip
echo "------------------------------------------------------------"
echo "-------------> Precip Output Directory"
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
  for fcycle in $fcycle_list ; do
     mkdir ${DATA_OUTmodel}/${model_fcst}/${fcycle}Z
     mkdir ${DATA_OUTmodel}/${model_fcst}/${fcycle}Z/FULL
     for reg in $regions_list ; do
        mkdir ${DATA_OUTmodel}/${model_fcst}/${fcycle}Z/${reg}
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
done
