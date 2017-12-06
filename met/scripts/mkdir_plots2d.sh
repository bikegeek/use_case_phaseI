#!/bin/ksh
#create output directory
mkdir ${DATA_OUTmain}/plots2d
mkdir ${DATA_OUTmain}/plots2d/model2model
mkdir ${DATA_OUTmain}/plots2d/model2obs
export DATA_OUT_model2model=${DATA_OUTmain}/plots2d/model2model
export DATA_OUT_model2obs=${DATA_OUTmain}/plots2d/model2obs
echo "------------------------------------------------------------"
echo "-------------> 2-D Plots Output Directory"
echo "${DATA_OUT_model2model}"
echo "${DATA_OUT_model2obs}"
export DATA_OUTmodel_model2model="${DATA_OUT_model2model}/model"
export DATA_OUTimgs_model2model="${DATA_OUT_model2model}/imgs"
export DATA_OUTlog_model2model="${DATA_OUT_model2model}/log"
export DATA_OUTmodel_model2obs="${DATA_OUT_model2obs}/model"
export DATA_OUTobs_model2obs="${DATA_OUT_model2obs}/obs"
export DATA_OUTimgs_model2obs="${DATA_OUT_model2obs}/imgs"
export DATA_OUTlog_model2obs="${DATA_OUT_model2obs}/log"
#create branches of output directory
mkdir ${DATA_OUTmodel_model2model}
mkdir ${DATA_OUTimgs_model2model}
mkdir ${DATA_OUTlog_model2model}
mkdir ${DATA_OUTmodel_model2obs}
mkdir ${DATA_OUTobs_model2obs}
mkdir ${DATA_OUTimgs_model2obs}
mkdir ${DATA_OUTlog_model2obs}
#create output directories for models
for model_fcst in $model_fcst_list ; do
  mkdir ${DATA_OUTmodel_model2model}/${model_fcst}
  mkdir ${DATA_OUTmodel_model2obs}/${model_fcst}
  for fcycle in $fcycle_list ; do
     mkdir ${DATA_OUTmodel_model2model}/${model_fcst}/${fcycle}Z
     mkdir ${DATA_OUTmodel_model2obs}/${model_fcst}/${fcycle}Z
#     mkdir ${DATA_OUTobs_model2obs}/${fcycle}Z
     for fday in $fday_list ; do
        mkdir ${DATA_OUTmodel_model2model}/${model_fcst}/${fcycle}Z/${fday}
        mkdir ${DATA_OUTmodel_model2obs}/${model_fcst}/${fcycle}Z/${fday}
#        mkdir ${DATA_OUTobs_model2obs}/${fcycle}Z/${fday}
     done
  done  
done

for fcycle in $fcycle_list ; do
   mkdir ${DATA_OUTobs_model2obs}/${fcycle}Z
   for fday in $fday_list ; do
       mkdir ${DATA_OUTobs_model2obs}/${fcycle}Z/${fday}
   done
done
#create output directories for images
for fcycle in $fcycle_list ; do
  mkdir ${DATA_OUTimgs_model2model}/${fcycle}Z
  mkdir ${DATA_OUTimgs_model2obs}/${fcycle}Z
  for fday in $fday_list ; do
      mkdir ${DATA_OUTimgs_model2model}/${fcycle}Z/${fday}
      mkdir ${DATA_OUTimgs_model2obs}/${fcycle}Z/${fday}
  done
done
