#!/bin/ksh
startscript=`date +%s`
#############################################################################
##### Set array variables
set -A model_fcst $model_fcst_list
set -A DATA_IN_model_fcst $DATA_IN_model_fcst_list
set -A model_fcst_dump $model_fcst_dump_list
#set -A gdas_dir $gdas_dir_list
set -A upper_air_regions $upper_air_regions_list
#set -A nam_dir $nam_dir_list
set -A conus_sfc_regions $conus_sfc_regions_list
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
#############################################################################
##### Run MET Point Stat and Stat Analysis
n=1
while [ $n -le $nexp ] ; do #loop over experiments
   nn=` expr $n - 1 `
   export model_fcst_now=${model_fcst[$nn]}
   sdate=${start_date}00
   edate=${end_date}23
   date=${sdate}
   while [ $date -le $edate ] ; do #loop over date range
       #run MET pb2nc to get gdas prepbufr files in format MET can read
       echo "------------------------------------------------------------"
       if [ -e "${prepbufr_dir}/gdas/prepbufr.gdas.${date}" ] ; then
          echo "-------------> Creating gdas prepbufr netcdf file"
          pb2nc ${prepbufr_dir}/gdas/prepbufr.gdas.${date} ${DATA_OUTmodel}/${model_fcst[$nn]}/upper_air/prepbufr.gdas.${date}.nc ${MET_HOME}/config_files/PB2NCConfig_upper_air
          #run MET Point Stat
          fhr=${fstart}
          while [ $fhr -le $fend ] ; do #loop over forecast hours
             if [ $fhr -lt 10 ] ; then
                hr=0${fhr}
             else
                hr=${fhr}
             fi
             fcstdate=`$ndate -${hr} ${date}`
             if [ -e "${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf${hr}${model_fcst_dump[$nn]}${fcstdate}" ] ; then
                  echo "------------------------------------------------------------"
                  echo "-------------> Running Point Stat for global upper-air grid2obs ${model_fcst[$nn]} ${fcstdate}f${hr} valid ${date}"
                  point_stat ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf${hr}${model_fcst_dump[$nn]}${fcstdate} ${DATA_OUTmodel}/${model_fcst[$nn]}/upper_air/prepbufr.gdas.${date}.nc ${MET_HOME}/config_files/PointStatConfig_upper_air -outdir ${DATA_OUTmodel}/${model_fcst[$nn]}/upper_air -v ${verbose}
             else
                  echo "------------------------------------------------------------"
                  echo "-------------> ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf${hr}${model_fcst_dump[$nn]}${fcstdate} does not exist"
             fi
             fhr=` expr $hr + $fint_upper_air`
          done
       else
          echo "------------------------------------------------------------"
          echo "-------------> ${gdas_dir[$nn]}/prepbufr.gdas.${date} does not exist"
       fi
       echo "------------------------------------------------------------"
       echo
       echo
       date=`$ndate +${fint_upper_air} ${date}`
   done
   #filter by initalization hour and valid date using MET Stat Analysis
   for fcycle in $fcycle_list ; do
       export cycle=${fcycle} 
       date=${start_date}${cycle}
       while [ $date -le ${end_date}${cycle} ] ; do #loop over date range
           echo "------------------------------------"
           echo "----------> Running Stat Analysis ${model_fcst[$nn]} valid on ${date} cycle ${cycle}Z"
           vdate=`echo $date |head -c8 `
           stat_analysis -lookin ${DATA_OUTmodel}/${model_fcst[$nn]}/upper_air -job filter -dump_row ${DATA_OUTmodel}/${model_fcst[$nn]}/upper_air/${cycle}Z/grid2obs_v${vdate}.txt -fcst_init_hour ${cycle}0000 -fcst_valid_beg ${vdate}'_'000000 -fcst_valid_end ${vdate}'_'230000 -v ${verbose}
           if [ ! -s ${DATA_OUTmodel}/${model_fcst[$nn]}/upper_air/${cycle}Z/grid2obs_v${vdate}.txt ] ; then
              rm ${DATA_OUTmodel}/${model_fcst[$nn]}/upper_air/${cycle}Z/grid2obs_v${vdate}.txt
           fi
           echo "------------------------------------"
           echo
           date=`$ndate +24 ${date}`
       done
       #copy file to directory, if given
       if [ -n "$grid2obs_dir" ] ; then
          echo "Copying files to ${grid2obs_dir}/upper_air/${cycle}Z/${model_fcst[$nn]}"
          if [ -d ${grid2obs_dir}/upper_air/${cycle}Z/${model_fcst[$nn]} ] ; then
             cp ${DATA_OUTmodel}/${model_fcst[$nn]}/upper_air/${cycle}Z/grid2obs_v*.txt ${grid2obs_dir}/upper_air/${cycle}Z/${model_fcst[$nn]}/.
          else
             mkdir ${grid2obs_dir}/upper_air/${cycle}Z/${model_fcst[$nn]}
             cp ${DATA_OUTmodel}/${model_fcst[$nn]}/upper_air/${cycle}Z/grid2obs_v*.txt ${grid2obs_dir}/upper_air/${cycle}Z/${model_fcst[$nn]}/.
          fi
       fi
   done
   n=` expr $n + 1 `
done
#
endscript=`date +%s`
runtime_s=$((endscript-startscript))
runtime_m=$((runtime_s/60))
echo
echo
echo
echo "Run time: $runtime_s s; $runtime_m m"
