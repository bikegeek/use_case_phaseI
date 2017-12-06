#!/bin/ksh
startscript=`date +%s`
#############################################################################
##### Set array variables
set -A model_fcst $model_fcst_list
set -A DATA_IN_model_fcst $DATA_IN_model_fcst_list
set -A model_fcst_dump $model_fcst_dump_list
set -A plot_stats $plot_stats_list
#############################################################################
##### Submit scripts for partial sum upper-air statistics
export var_name_list_upper_air="TMP RH UGRD_VGRD"
set -A var_name_upper_air $var_name_list_upper_air 
export nvar_upper_air=`echo $var_name_list_upper_air |wc -w`
#
v=1
while [ $v -le $nvar_upper_air ] ; do #submit plotting script by variables
   vv=` expr $v - 1 `
   export var_name_now=${var_name_upper_air[$vv]}
   export var_level_list="P850 P500 P200 P50 P10"
   #${MET_HOME}/scripts/plot_grid2obs_upper_air.sh 1>${DATA_OUT}/log/plot_grid2obs_upper_air_c${cycle}_${var_name_now}.out 2>&1 & 
   v=` expr $v + 1 `
done
##### Submit scripts for partial sums CONUS surface statistics
export var_name_list_conus_sfc="TMP RH DPT UGRD_VGRD TCDC PRMSL"
set -A var_name_conus_sfc $var_name_list_conus_sfc 
export nvar_conus_sfc=`echo $var_name_list_conus_sfc |wc -w`
v=1
while [ $v -le $nvar_conus_sfc ] ; do #submit plotting script by variable
   vv=` expr $v - 1 `
   export var_name_now=${var_name_conus_sfc[$vv]}
   if [ ${var_name_now} = PRMSL -o ${var_name_now} = TCDC ]; then
      export var_level_list="Z0"
   elif [ ${var_name_now} = UGRD_VGRD ]; then
      export var_level_list="Z10"
   else
      export var_level_list="Z2"
   fi
   ${MET_HOME}/scripts/plot_grid2obs_conus_sfc.sh 1>${DATA_OUT}/log/plot_grid2obs_conus_sfc_c${cycle}_${var_name_now}.out 2>&1 &
   v=` expr $v + 1 `
done
#
endscript=`date +%s`
runtime_s=$((endscript-startscript))
runtime_m=$((runtime_s/60))
echo
echo
echo
echo "Run time: $runtime_s s; $runtime_m m"
