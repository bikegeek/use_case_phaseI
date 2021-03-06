#!/bin/ksh
startscript=`date +%s`
#############################################################################
##### Set array variables
set -A model_fcst $model_fcst_list
set -A DATA_IN_model_fcst $DATA_IN_model_fcst_list
set -A model_fcst_dump $model_fcst_dump_list
set -A upper_air_regions $upper_air_regions_list
set -A conus_sfc_regions $conus_sfc_regions_list
#############################################################################
###################################### Computing
#############################################################################
##### Use MET Point Stat and Stat Analysis to generate partial sums
#format desired upper_air_grid ID for correct use in MET Point Stat config file
upper_air_GG=`echo $upper_air_grid |cut -c2- `
if [ $upper_air_GG -lt 10 ] ; then
   upper_air_GGG=G00$upper_air_GG
fi
if ([ $upper_air_GG -ge 10 ] && [ $upper_air_GG -lt 100 ]) ; then
   upper_air_GGG=G0$upper_air_GG
fi
if [ $upper_air_GG -ge 100 ] ; then
   upper_air_GGG=G$upper_air_GG
fi
export upper_air_GGG=${upper_air_GGG}
#prep upper-air regions to analyze for input into MET Point Stat Config File
r=1
while [ $r -le $nuareg ] ; do
  rr=` expr $r - 1 `
  if [ $rr -eq 0 ]; then
     upper_air_regions_path='"'"${MET_HOME}/poly/${upper_air_regions[$rr]}.nc"'"'
  else
     upper_air_regions_path[$rr]=' "'"${MET_HOME}/poly/${upper_air_regions[$rr]}.nc"'"'
  fi
  r=` expr $r + 1 `
done
export upper_air_regions_config=$( printf "%s," "${upper_air_regions_path[@]}" | cut -d "," -f 1-${#upper_air_regions_path[@]} )
#prep CONUS regions to analyze for input into MET Point Stat Config File
r=1
while [ $r -le $ncsfcreg ] ; do
  rr=` expr $r - 1 `
  if [ $rr -eq 0 ]; then
     conus_sfc_regions_path='"'"${MET_HOME}/poly/${conus_sfc_regions[$rr]}.poly"'"'
  else
     conus_sfc_regions_path[$rr]=' "'"${MET_HOME}/poly/${conus_sfc_regions[$rr]}.poly"'"'
  fi
  r=` expr $r + 1 `
done
export conus_sfc_regions_config=$( printf "%s," "${conus_sfc_regions_path[@]}" | cut -d "," -f 1-${#conus_sfc_regions_path[@]} )
#############################################################################
##### Run MET Point Stat and Stat Analysis
n=1
while [ $n -le $nexp ] ; do #loop over experiments
   nn=` expr $n - 1 `
   export model_fcst_now=${model_fcst[$nn]}
   sdate=${start_date}${cycle}
   edate=${end_date}${cycle}
   date=${sdate}
   while [ $date -le $edate ] ; do #loop over date range
     fhr=${fstart}
       while [ $fhr -le $fend ] ; do #loop over forecast hours
          if [ $fhr -lt 10 ] ; then
             hr=0${fhr}
          else
             hr=${fhr}
          fi
          #run MET Point Stat
          validdate=`$ndate +${hr} ${date}`    
          #run MET pb2nc to get gdas prepbufr files in format MET can read
          if [ ! -e "${DATA_OUTmodel}/${model_fcst[$nn]}/upper_air/${cycle}Z/prepbufr.gdas.${validdate}.nc" ] ; then
             echo "------------------------------------------------------------"
             echo "-------------> Creating gdas prepbufr netcdf file valid ${validdate}"
             if [ -e "${prepbufr_dir}/gdas/prepbufr.gdas.${validdate}" ] ; then
                pb2nc ${prepbufr_dir}/gdas/prepbufr.gdas.${validdate} ${DATA_OUTmodel}/${model_fcst[$nn]}/upper_air/${cycle}Z/prepbufr.gdas.${validdate}.nc ${MET_HOME}/config_files/PB2NCConfig_upper_air
             else
                echo "------------------------------------------------------------"
                echo "-------------> ${gdas_dir[$nn]}/prepbufr.gdas.${validdate}  does not exist"
             fi
          fi
          #run MET Point Stat
          if [ -e "${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf${hr}${model_fcst_dump[$nn]}${date}" ] ; then
               echo "------------------------------------------------------------"
               echo "-------------> Running Point Stat for global upper-air grid2obs ${model_fcst[$nn]} ${date}f${hr} valid ${validdate}"
               point_stat ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf${hr}${model_fcst_dump[$nn]}${date} ${DATA_OUTmodel}/${model_fcst[$nn]}/upper_air/${cycle}Z/prepbufr.gdas.${validdate}.nc ${MET_HOME}/config_files/PointStatConfig_upper_air -outdir ${DATA_OUTmodel}/${model_fcst[$nn]}/upper_air/${cycle}Z -v ${verbose}
          else
               echo "------------------------------------------------------------"
               echo "-------------> ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf${hr}${model_fcst_dump[$nn]}${date} does not exist"
          fi
          fhr=` expr $hr + $fint_upper_air`
          echo
       done
       #filter by initalization date using MET Stat Analysis
       echo "----------> Running Stat Analysis ${model_fcst[$nn]} run at ${date}"
       idate=`echo $date |head -c8 `
       stat_analysis -lookin ${DATA_OUTmodel}/${model_fcst[$nn]}/upper_air/${cycle}Z -job filter -dump_row ${DATA_OUTmodel}/${model_fcst[$nn]}/upper_air/${cycle}Z/grid2obs_i${date}.txt -fcst_init_beg ${idate}'_'${cycle}0000 -v ${verbose}
       echo "------------------------------------------------------------"
       echo
       echo
       date=`$ndate +24 ${date}`
   done
   #copy file to directory, if given
   if [ -n "$grid2obs_dir" ] ; then
      echo "Copying files to ${grid2obs_dir}/upper_air/${cycle}Z/${model_fcst[$nn]}"
      if [ -d ${grid2obs_dir}/upper_air/${cycle}Z/${model_fcst[$nn]} ] ; then
         cp ${DATA_OUTmodel}/${model_fcst[$nn]}/upper_air/${cycle}Z/grid2obs_i*.txt ${grid2obs_dir}/upper_air/${cycle}Z/${model_fcst[$nn]}/.
      else
         mkdir ${grid2obs_dir}/upper_air/${cycle}Z/${model_fcst[$nn]}
         cp ${DATA_OUTmodel}/${model_fcst[$nn]}/upper_air/${cycle}Z/grid2obs_i*.txt ${grid2obs_dir}/upper_air/${cycle}Z/${model_fcst[$nn]}/.
      fi
   fi
   n=` expr $n + 1 `
done
#############################################################################
###################################### Plotting
#############################################################################
export var_name_list_upper_air="TMP RH"
set -A var_name_upper_air $var_name_list_upper_air 
export nvar_upper_air=`echo $var_name_list_upper_air |wc -w`
#
v=1
while [ $v -le $nvar_upper_air ] ; do #submit plotting script by variables
   vv=` expr $v - 1 `
   export var_name_now=${var_name_upper_air[$vv]}
   export var_level_list="P1000 P925 P850 P700 P500 P400 P300 P250 P200 P150 P100 P50"
   ${MET_HOME}/scripts/plot_grid2obs_cycleforecasthours_upper_air.sh 1>${DATA_OUT}/log/plot_grid2obs_upper_air_c${cycle}_${var_name_now}.out 2>&1 &
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
