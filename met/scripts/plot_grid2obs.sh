#!/bin/ksh
startscript=`date +%s`
#############################################################################
##### Set array variables
set -A model_fcst $model_fcst_list
set -A DATA_IN_model_fcst $DATA_IN_model_fcst_list
set -A model_fcst_dump $model_fcst_dump_list
set -A upper_air_regions $upper_air_regions_list
set -A conus_sfc_regions $conus_sfc_regions_list
set -A regions $regions_list
set -A plot_stats $plot_stats_list
#############################################################################
#gather lists of variables
export listvar1=MET_HOME,ndate
export listvar2=model_fcst_list,DATA_IN_model_fcst_list,model_fcst_dump_list,DATA_OUTmain,grid2obs_dir,start_date,end_date,fstart,fend,fint_upper_air,fint_conus_sfc,upper_air_grid,conus_sfc_grid,prepbufr_dir,upper_air_regions_list,conus_sfc_regions_list,plot_stats_list,verbose,nexp,nuareg,ncsfcreg,cycle,var_name_now,var_level_list,region_now
export listvar3=DATA_OUT,DATA_OUTmodel,DATA_OUTimgs,DATA_OUTlog
export listvar="$listvar1,$listvar2,$listvar3"
##### Submit scripts for partial sum upper-air statistics
export var_name_list_upper_air="TMP HGT RH UGRD VGRD"
set -A var_name_upper_air $var_name_list_upper_air 
export nvar_upper_air=`echo $var_name_list_upper_air |wc -w`
#
v=1
while [ $v -le $nvar_upper_air ] ; do #submit plotting script by variables
   vv=` expr $v - 1 `
   export var_name_now=${var_name_upper_air[$vv]}
   export var_level_list="P1000 P925 P850 P700 P500 P400 P300 P250 P200 P150 P100 P50"
   r=0
   while [ $r -le $nuareg ] ; do #loop over region
      if [ $r -eq 0 ] ; then
         region_now=FULL
      else
         rr=` expr $r - 1 `
         region_now=${upper_air_regions[$rr]}
      fi
      export region_now=${region_now}
      echo "----> Submitting UPPER AIR: ${var_name_now} ${region_now}"
      if [ $batch = yes ] ; then
          $SUBJOB -e $listvar -a $ACCOUNT  -q "$CUE2RUN" -g $GROUP -p 1/1/N -r 2048/1 -t 6:00:00 -j plot_grid2obs_upper_air_c${cycle}_${var_name_now}_${region_now} -o ${DATA_OUT}/log/plot_grid2obs_upper_air_c${cycle}_${var_name_now}_${region_now}.out  ${MET_HOME}/scripts/plot_grid2obs_upper_air.sh
      else
          echo "SPACE"
          #${MET_HOME}/scripts/plot_grid2obs_upper_air.sh 1>${DATA_OUT}/log/plot_grid2obs_upper_air_c${cycle}_${var_name_now}_${region_now}.out 2>&1 &
      fi
      r=` expr $r + 1 `
   done
   v=` expr $v + 1 `
done
echo
echo
echo
#gather lists of variables
export listvar1=MET_HOME,ndate
export listvar2=model_fcst_list,DATA_IN_model_fcst_list,model_fcst_dump_list,DATA_OUTmain,grid2obs_dir,start_date,end_date,fstart,fend,fint_upper_air,fint_conus_sfc,upper_air_grid,conus_sfc_grid,prepbufr_dir,upper_air_regions_list,conus_sfc_regions_list,plot_stats_list,verbose,nexp,nuareg,ncsfcreg,cycle,var_name_now,var_level_now,region_now
export listvar3=DATA_OUT,DATA_OUTmodel,DATA_OUTimgs,DATA_OUTlog
export listvar="$listvar1,$listvar2,$listvar3"
##### Submit scripts for partial sums CONUS surface statistics
export var_name_list_conus_sfc="TMP RH DPT PRMSL UGRD VGRD TCDC"
set -A var_name_conus_sfc $var_name_list_conus_sfc 
export nvar_conus_sfc=`echo $var_name_list_conus_sfc |wc -w`
v=1
while [ $v -le $nvar_conus_sfc ] ; do #submit plotting script by variable
   vv=` expr $v - 1 `
   export var_name_now=${var_name_conus_sfc[$vv]}
   if [ ${var_name_now} = PRMSL ]; then
      export var_level_now="Z0"
   elif [ ${var_name_now} = UGRD -o ${var_name_now} = VGRD ]; then
      export var_level_now="Z10"
   elif [ ${var_name_now} = TCDC ] ; then
      export var_level_now="L0"
   else
      export var_level_now="Z2"
   fi
   r=0
   while [ $r -le $ncsfcreg ] ; do #loop over region
      if [ $r -eq 0 ] ; then
         region_now=FULL
      else
         rr=` expr $r - 1 `
         region_now=${conus_sfc_regions[$rr]}
      fi
      export region_now=${region_now}
      echo "----> Submitting CONUS SURFACE: ${var_name_now} ${var_level_now} ${region_now}"
      if [ $batch = yes ] ; then
          $SUBJOB -e $listvar -a $ACCOUNT  -q "$CUE2RUN" -g $GROUP -p 1/1/N -r 2048/1 -t 6:00:00 -j plot_grid2obs_conus_sfc_c${cycle}_${var_name_now}${var_level_now}_${region_now} -o ${DATA_OUT}/log/plot_grid2obs_conus_sfc_c${cycle}_${var_name_now}${var_level_now}_${region_now}.out  ${MET_HOME}/scripts/plot_grid2obs_conus_sfc.sh
      else
          ${MET_HOME}/scripts/plot_grid2obs_conus_sfc.sh 1>${DATA_OUT}/log/plot_grid2obs_conus_sfc_c${cycle}_${var_name_now}${var_level_now}_${region_now}.out 2>&1 &
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
