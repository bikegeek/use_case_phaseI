#!/bin/ksh
startscript=`date +%s`
#############################################################################
##### Set array variables
set -A model_fcst $model_fcst_list
set -A DATA_IN_model_fcst $DATA_IN_model_fcst_list
set -A model_fcst_dump $model_fcst_dump_list
set -A regions $regions_list
#############################################################################
##### Use MET Grid Stat and Stat Analysis to generate partial sums
##### model analysis as truth
#format desired grid ID for correct use in MET Grid Stat config file
GG=`echo $grid |cut -c2- `
if [ $GG -lt 10 ] ; then
   GGG=G00$GG
fi
if ([ $GG -ge 10 ] && [ $GG -lt 100 ]) ; then
   GGG=G0$GG
fi
if [ $GG -ge 100 ] ; then
   GGG=G$GG
fi
export GGG=${GGG}
#prep regions to analyze for input into MET Grid Stat Config File
r=1
while [ $r -le $nreg ] ; do
  rr=` expr $r - 1 `
  if [ $rr -eq 0 ]; then
     regions_path='"'"${MET_HOME}/poly/${regions[$rr]}.nc"'"'
  else
     regions_path[$rr]=' "'"${MET_HOME}/poly/${regions[$rr]}.nc"'"'
  fi
  r=` expr $r + 1 `
done
export regions_config=$( printf "%s," "${regions_path[@]}" | cut -d "," -f 1-${#regions_path[@]} )
#############################################################################
##### Run MET Grid Stat and Stat Analysis
n=1
while [ $n -le $nexp ] ; do #loop over experiments
   nn=` expr $n - 1 `
   export model_fcst_now=${model_fcst[$nn]}
   sdate=${start_date}${cycle}
   edate=${end_date}${cycle}
   date=${sdate}
   while [ $date -le $edate ] ; do #loop over date range
       vm=`echo $date |cut -c5-6 `
       export vm=${vm}
       vd=`echo $date |cut -c7-8 `
       export vd=${vd}
       fhr=${fstart}
       if [ -e "${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbanl${model_fcst_dump[$nn]}${date}" ] ; then
          while [ $fhr -le $fend ] ; do #loop over forecast hours
             if [ $fhr -lt 10 ] ; then
                hr=0${fhr}
             else
                hr=${fhr}
             fi
             #run MET Grid Stat
             fcstdate=`$ndate -${hr} ${date}`
             if [ -e "${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf${hr}${model_fcst_dump[$nn]}${fcstdate}" ] ; then
                  echo "------------------------------------------------------------"
                  echo "-------------> Running Grid Stat ${model_fcst[$nn]}_anl ${date}   ${model_fcst[$nn]} ${fcstdate}f${hr}"
                  echo "-------> Anomaly"
                  grid_stat ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf${hr}${model_fcst_dump[$nn]}${fcstdate} ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbanl${model_fcst_dump[$nn]}${date} ${MET_HOME}/config_files/GridStatConfig_anom -outdir ${DATA_OUTmodel}/${model_fcst[$nn]}/anom/${cycle}Z -v ${verbose}
                  grid_stat ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf${hr}${model_fcst_dump[$nn]}${fcstdate} ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbanl${model_fcst_dump[$nn]}${date} ${MET_HOME}/config_files/GridStatConfig_anom_height -outdir ${DATA_OUTmodel}/${model_fcst[$nn]}/anom/${cycle}Z -v ${verbose}
             else
                  echo "------------------------------------------------------------"
                  echo "-------------> ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf${hr}${model_fcst_dump[$nn]}${fcstdate} does not exist"
             fi
             fhr=` expr $hr + $fint`
          done
          #filter by valid date using MET Stat Analysis
          echo "------------------------------------"
          echo "----------> Running Stat Analysis ${model_fcst[$nn]} v${date}"
          vdate=`echo $date |head -c8 `
          vhr=`echo $date |cut -c9- `
          echo "-------> Anomaly"
          stat_analysis -lookin ${DATA_OUTmodel}/${model_fcst[$nn]}/anom/${cycle}Z -job filter -dump_row ${DATA_OUTmodel}/${model_fcst[$nn]}/anom/${cycle}Z/parsum_v${vdate}.txt -fcst_valid_beg ${vdate}'_'${vhr}0000 -v ${verbose}
          echo "------------------------------------"
          echo "------------------------------------------------------------"
          echo
          echo
       else
         echo "------------------------------------------------------------"
         echo "-------------> ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbanl${model_fcst_dump[$nn]}${date} does not exist"
         echo "------------------------------------------------------------"
         echo
         echo
       fi
       date=`$ndate +24 ${date}`
   done
   #copy file to directory, if given
   if [ -n "$parsum_dir" ] ; then
      echo "Copying files to ${parsum_dir}/anom/${cycle}Z/${model_fcst[$nn]}"
      if [ -d ${parsum_dir}/anom/${cycle}Z/${model_fcst[$nn]} ] ; then
         cp ${DATA_OUTmodel}/${model_fcst[$nn]}/anom/${cycle}Z/parsum_v*.txt ${parsum_dir}/anom/${cycle}Z/${model_fcst[$nn]}/.
      else
         mkdir ${parsum_dir}/anom/${cycle}Z/${model_fcst[$nn]}
         cp ${DATA_OUTmodel}/${model_fcst[$nn]}/anom/${cycle}Z/parsum_v*.txt ${parsum_dir}/anom/${cycle}Z/${model_fcst[$nn]}/.
      fi
   fi
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
