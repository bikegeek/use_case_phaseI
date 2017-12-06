#!/bin/ksh
startscript=`date +%s`
#############################################################################
##### Set array variables
set -A model_fcst $model_fcst_list
set -A DATA_IN_model_fcst $DATA_IN_model_fcst_list
set -A model_fcst_dump $model_fcst_dump_list
set -A file_type $file_type_lists
set -A regions $regions_list
set -A threshold $threshold_list
#############################################################################
##### Use MET Pcp_combine, Grid Stat, and Stat Analysis to generate
##### contingency table counts for various thresholds of precip (mm)
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
#prep thersholds to analyze for intput into MET Grid Stat Config File
t=1
while [ $t -le $nthrs ] ; do
  tt=` expr $t - 1 ` 
  if [ $t -eq 1 ] ; then
     threshold_group=">="${threshold[$tt]}","
  elif [ $t -lt $nthrs ] ; then
     threshold_group[$tt]=">="${threshold[$tt]}","
  else
     threshold_group[$tt]=">="${threshold[$tt]}
  fi
  t=` expr $t + 1 `
done
export threshold_config=${threshold_group[@]}
#############################################################################
#### Run MET Pcp_combine, Grid Stat, and Stat Analysis
n=1
while [ $n -le $nexp ] ; do #loop over experiments
   nn=` expr $n - 1 `
   export model_fcst_now=${model_fcst[$nn]}
   sdate=${start_date}${cycle}
   edate=${end_date}${cycle}
   date=${sdate}
   while [ $date -le $edate ] ; do #loop over date range
      vdate=`echo $date |head -c8 `
      if [ -e "${precip_obs_dir}/${precip_obs_file_prefix}${vdate}${precip_obs_file_suffix}" ] ; then
         #for 00Z cycle
         if [ ${cycle} -eq 00 ] ; then
         #define start of forecast hour range index
         fstart=` expr $fstart_r1 + 12`
         fend=` expr $fend_r2 - 12`
         fhrstart=${fstart}
         while [ $fhrstart -le $fend ] ; do #loop over forecast hour ranges
            fh0=` expr $fhrstart + 0 `
            fh1=` expr $fhrstart + 6 `
            fh2=` expr $fhrstart + 12 `
            fh3=` expr $fhrstart + 18 `
            fh4=` expr $fhrstart + 24 `
            fcstdate=`$ndate -${fh2} ${date}`
            if [ -e "${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh1}${model_fcst_dump[$nn]}${fcstdate}" ] && [ -e "${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh2}${model_fcst_dump[$nn]}${fcstdate}" ] && [ -e "${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh3}${model_fcst_dump[$nn]}${fcstdate}" ] && [ -e "${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh4}${model_fcst_dump[$nn]}${fcstdate}" ] ; then
               #run MET Pcp_combine
               echo "------------------------------------------------------------"
               echo "-------------> Running Pcp_combine c${cycle}Z ${model_fcst[$nn]} v${vdate}12 ${fcstdate} f${fh0}-f${fh1}, f${fh1}-f${fh2}, f${fh2}-f${fh3}, f${fh3}-f${fh4}"
               pcp_combine -add ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh1}${model_fcst_dump[$nn]}${fcstdate} 6 ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh2}${model_fcst_dump[$nn]}${fcstdate} 6 ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh3}${model_fcst_dump[$nn]}${fcstdate} 6 ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh4}${model_fcst_dump[$nn]}${fcstdate} 6 -field "'name="'"'${model_var}'"; level="L0";'"'" -name ${model_var} ${DATA_OUTmodel}/${model_fcst[$nn]}/${cycle}Z/${fcstdate}f${fhrstart}f${fh4}_v${vdate}12.nc -v ${verbose}
               if [ ${model_var} == "PRATE" ] ; then
                     echo "---> PRATE, mm/day to mm"
                     ncatted -a scale_factor,,c,d,3600.0 ${DATA_OUTmodel}/${model_fcst[$nn]}/${cycle}Z/${fcstdate}f${fhrstart}f${fh4}_v${vdate}12.nc
                     ncpdq -U -O ${DATA_OUTmodel}/${model_fcst[$nn]}/${cycle}Z/${fcstdate}f${fhrstart}f${fh4}_v${vdate}12.nc ${DATA_OUTmodel}/${model_fcst[$nn]}/${cycle}Z/${fcstdate}f${fhrstart}f${fh4}_v${vdate}12.nc
               fi
               #run MET Grid Stat
               echo "------------------------------------"
               echo "-------------> Running Grid Stat ${obs_name} v${vdate}12 ${model_fcst[$nn]} c${cycle} ${fcstdate} f${fh0}-f${fh4}"
               grid_stat ${DATA_OUTmodel}/${model_fcst[$nn]}/${cycle}Z/${fcstdate}f${fhrstart}f${fh4}_v${vdate}12.nc ${precip_obs_dir}/${precip_obs_file_prefix}${vdate}${precip_obs_file_suffix} ${MET_HOME}/config_files/GridStatConfig_precip -outdir ${DATA_OUTmodel}/${model_fcst[$nn]}/${cycle}Z -v ${verbose}
               echo "------------------------------------"
               echo "------------------------------------------------------------"
            else
               echo "------------------------------------------------------------"
               echo "-------------> ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh1}${model_fcst_dump[$nn]}${fcstdate} or  ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh2}${model_fcst_dump[$nn]}${fcstdate} or ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh3}${model_fcst_dump[$nn]}${fcstdate} or ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh4}${model_fcst_dump[$nn]}${fcstdate} does not exist "
               echo "------------------------------------------------------------"
            fi
            fhrstart=` expr $fhrstart + 24 `
         done
         #filter by valid date using MET Stat Analysis
         echo "------------------------------------"
         echo "----------> Running Stat Analysis"
         vhr=`echo $date |cut -c9- `
         stat_analysis -lookin ${DATA_OUTmodel}/${model_fcst[$nn]}/${cycle}Z -job filter -dump_row ${DATA_OUTmodel}/${model_fcst[$nn]}/${cycle}Z/precip_v${vdate}.txt -fcst_valid_beg ${vdate}'_'${vhr}0000 -line_type CTC -v ${verbose}
         echo "------------------------------------"
         fi
         #for 12Z cycle
         if [ ${cycle} -eq 12 ] ; then
            #define start of forecast hour range index
            fstart=$fstart_r1
            fend=` expr $fend_r2 - 24`
            fhrstart=${fstart}
            while [ $fhrstart -le $fend ] ; do #loop over forecast hour ranges
               fh0=` expr $fhrstart + 0 `
               fh1=` expr $fhrstart + 6 `
               if [ $fh1 -lt 10 ] ; then
                   fh1=0${fh1}
               fi
               fh2=` expr $fhrstart + 12 `
               fh3=` expr $fhrstart + 18 `
               fh4=` expr $fhrstart + 24 `
               fcstdate=`$ndate -${fh4} ${date}`
               if [ -e "${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh1}${model_fcst_dump[$nn]}${fcstdate}" ] && [ -e "${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh2}${model_fcst_dump[$nn]}${fcstdate}" ] && [ -e "${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh3}${model_fcst_dump[$nn]}${fcstdate}" ] && [ -e "${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh4}${model_fcst_dump[$nn]}${fcstdate}" ] ; then
                  #run MET Pcp_combine
                  echo "------------------------------------------------------------"
                  echo "-------------> Running Pcp_combine c${cycle}Z ${model_fcst[$nn]} v${vdate}12 ${fcstdate} f${fh0}-f${fh1}, f${fh1}-f${fh2}, f${fh2}-f${fh3}, f${fh3}-f${fh4}"
                  pcp_combine -add ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh1}${model_fcst_dump[$nn]}${fcstdate} 6 ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh2}${model_fcst_dump[$nn]}${fcstdate} 6 ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh3}${model_fcst_dump[$nn]}${fcstdate} 6 ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh4}${model_fcst_dump[$nn]}${fcstdate} 6 -field "'name="'"'${model_var}'"; level="L0";'"'" -name ${model_var} ${DATA_OUTmodel}/${model_fcst[$nn]}/${cycle}Z/${fcstdate}f${fhrstart}f${fh4}_v${vdate}12.nc -v ${verbose}
                  if [ ${model_var} == "PRATE" ] ; then
                        echo "---> PRATE, mm/day to mm"
                        ncatted -a scale_factor,,c,d,3600.0 ${DATA_OUTmodel}/${model_fcst[$nn]}/${cycle}Z/${fcstdate}f${fhrstart}f${fh4}_v${vdate}12.nc
                        ncpdq -U -O ${DATA_OUTmodel}/${model_fcst[$nn]}/${cycle}Z/${fcstdate}f${fhrstart}f${fh4}_v${vdate}12.nc ${DATA_OUTmodel}/${model_fcst[$nn]}/${cycle}Z/${fcstdate}f${fhrstart}f${fh4}_v${vdate}12.nc
                  fi
                  #run MET Grid Stat
                  echo "------------------------------------"
                  echo "-------------> Running Grid Stat ${obs_name} v${vdate}12 ${model_fcst[$nn]} c${cycle} ${fcstdate} f${fh0}-f${fh4}"
                  grid_stat ${DATA_OUTmodel}/${model_fcst[$nn]}/${cycle}Z/${fcstdate}f${fhrstart}f${fh4}_v${vdate}12.nc ${precip_obs_dir}/${precip_obs_file_prefix}${vdate}${precip_obs_file_suffix} ${MET_HOME}/config_files/GridStatConfig_precip -outdir ${DATA_OUTmodel}/${model_fcst[$nn]}/${cycle}Z -v ${verbose}
                  echo "------------------------------------"
                  echo "------------------------------------------------------------"
               else
                  echo "------------------------------------------------------------"
                  echo "-------------> ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh1}${model_fcst_dump[$nn]}${fcstdate} or  ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh2}${model_fcst_dump[$nn]}${fcstdate} or ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh3}${model_fcst_dump[$nn]}${fcstdate} or ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/${file_type[$nn]}${fh4}${model_fcst_dump[$nn]}${fcstdate} does not exist "
                  echo "------------------------------------------------------------"
               fi
               fhrstart=` expr $fhrstart + 24 `
            done
            #filter by valid date using MET Stat Analysis
            echo "------------------------------------"
            echo "----------> Running Stat Analysis"
            vhr=`echo $date |cut -c9- `
            stat_analysis -lookin ${DATA_OUTmodel}/${model_fcst[$nn]}/${cycle}Z -job filter -dump_row ${DATA_OUTmodel}/${model_fcst[$nn]}/${cycle}Z/precip_v${vdate}.txt -fcst_valid_beg ${vdate}'_'${vhr}0000 -line_type CTC -v ${verbose}
            echo "------------------------------------"
         fi
      else
        echo "------------------------------------------------------------"
        echo "-------------> ${precip_obs_dir}/${precip_obs_file_prefix}${vdate}${precip_obs_file_suffix} does not exist"
        echo "------------------------------------------------------------"
      fi
      date=`$ndate +24 ${date}`
      echo
   done
   #copy files to directory, if given
   if [ -n "$contable_dir" ] ; then
      if [ -d ${contable_dir}/${cycle}Z/${model_fcst[$nn]} ] ; then
          cp ${DATA_OUTmodel}/${model_fcst[$nn]}/${cycle}Z/precip_v*.txt ${contable_dir}/${cycle}Z/${model_fcst[$nn]}/.
      else
          mkdir ${contable_dir}/${cycle}Z/${model_fcst[$nn]}
          cp ${DATA_OUTmodel}/${model_fcst[$nn]}/${cycle}Z/precip_v*.txt ${contable_dir}/${cycle}Z/${model_fcst[$nn]}/.
      fi
   fi
   echo
   echo
   echo
   n=` expr $n + 1 `
done
echo
echo 
echo
#
endscript=`date +%s`
runtime_s=$((endscript-startscript))
runtime_m=$((runtime_s/60))
echo
echo
echo
echo "Run time: $runtime_s s; $runtime_m m"
