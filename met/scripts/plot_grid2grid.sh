#!/bin/ksh
startscript=`date +%s`
#############################################################################
##### Set array variables
set -A model_fcst $model_fcst_list
set -A DATA_IN_model_fcst $DATA_IN_model_fcst_list
set -A model_fcst_dump $model_fcst_dump_list
set -A regions $regions_list
set -A plot_stats $plot_stats_list
#############################################################################
#gather lists of variables
export listvar1=MET_HOME,ndate
export listvar2=model_fcst_list,DATA_IN_model_fcst_list,model_fcst_dump_list,DATA_OUTmain,parsum_dir,start_date,end_date,fstart,fend,fint,grid,regions_list,sfc_regions_list,plot_stats_list,verbose,nexp,nreg,nsreg,cycle,var_name_now,var_level_list,region_now
export listvar3=DATA_OUT,DATA_OUTmodel,DATA_OUTimgs,DATA_OUTlog
export listvar="$listvar1,$listvar2,$listvar3"
##### Submit scripts for partial sum statistics
export var_name_list_pres="HGT TMP O3MR UGRD VGRD UGRD_VGRD"
set -A var_name_pres $var_name_list_pres 
export nvar_pres=`echo $var_name_list_pres |wc -w`
#
v=1
while [ $v -le $nvar_pres ] ; do #submit plotting script by variables...
   vv=` expr $v - 1 `
   export var_name_now=${var_name_pres[$vv]}
   if [ ${var_name_now} = O3MR ]; then
      export var_level_list="P100 P70 P50 P30 P20 P10"
   else
      export var_level_list="P1000 P850 P700 P500 P200 P100 P50 P20 P10"
   fi
   r=0
   while [ $r -le $nreg ] ; do #...and by regions
      if [ $r -eq 0 ] ; then
         region_now=FULL
      else
         rr=` expr $r - 1 `
         region_now=${regions[$rr]}
      fi
      export region_now=${region_now}
      echo "----> Submitting PRES: ${var_name_now} ${region_now}"
      if [ $batch = yes ] ; then
          $SUBJOB -e $listvar -a $ACCOUNT  -q "$CUE2RUN" -g $GROUP -p 1/1/N -r 2048/1 -t 6:00:00 -j plot_grid2grid_pres_c${cycle}_${var_name_now}_${region_now} -o ${DATA_OUT}/log/plot_grid2grid_pres_c${cycle}_${var_name_now}_${region_now}.out  ${MET_HOME}/scripts/plot_grid2grid_pres.sh
      else
          ${MET_HOME}/scripts/plot_grid2grid_pres.sh 1>${DATA_OUT}/log/plot_grid2grid_pres_c${cycle}_${var_name_now}_${region_now}.out 2>&1 &
      fi
      r=` expr $r + 1 `
   done 
   v=` expr $v + 1 `
done
echo
echo
echo
##### Submit scripts for anomalous partial sums statistics
export var_name_list_anom="HGT TMP PRMSL UGRD VGRD UGRD_VGRD"
set -A var_name_anom $var_name_list_anom 
export nvar_anom=`echo $var_name_list_anom |wc -w`
v=1
while [ $v -le $nvar_anom ] ; do #submit plotting script by variables...
   vv=` expr $v - 1 `
   export var_name_now=${var_name_anom[$vv]}
   if [ ${var_name_now} = PRMSL ]; then
      export var_level_list="Z0"
   elif [ ${var_name_now} = HGT ]; then
      export var_level_list="P1000 P700 P500 P250"
   else
      export var_level_list="P850 P500 P250"
   fi
   r=0
   while [ $r -le $nreg ] ; do #...and by regions
      if [ $r -eq 0 ] ; then
         region_now=FULL
      else
         rr=` expr $r - 1 `
         region_now=${regions[$rr]}
      fi
      export region_now=${region_now}
      echo "----> Submitting ANOM: ${var_name_now} ${region_now}"
      if [ $batch = yes ] ; then
          $SUBJOB -e $listvar -a $ACCOUNT  -q "$CUE2RUN" -g $GROUP -p 1/1/N -r 2048/1 -t 6:00:00 -j plot_grid2grid_anom_c${cycle}_${var_name_now}_${region_now} -o ${DATA_OUT}/log/plot_grid2grid_anom_c${cycle}_${var_name_now}_${region_now}.out  ${MET_HOME}/scripts/plot_grid2grid_anom.sh
      else
          ${MET_HOME}/scripts/plot_grid2grid_anom.sh 1>${DATA_OUT}/log/plot_grid2grid_anom_c${cycle}_${var_name_now}_${region_now}.out 2>&1 &
      fi
      r=` expr $r + 1 `
   done 
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
