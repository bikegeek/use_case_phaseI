#!/bin/ksh
startscript=`date +%s`
#############################################################################
##### Set array varibles 
set -A model_fcst $model_fcst_list
set -A DATA_IN_model_fcst $DATA_IN_model_fcst_list
set -A model_fcst_dump $model_fcst_dump_list
set -A regions $regions_list
set -A threshold $threshold_list
set -A plot_stats $plot_stats_list
#############################################################################
#### Run MET Stat Analysis to filter partial sum files
t=1
while [ $t -le $nthrs ] ; do #loop over threshold
  tt=` expr $t - 1 `
  export threshold_now=${threshold[$tt]}
  r=0
  while [ $r -le $nreg ] ; do #loop over region
    if [ $r -eq 0 ] ; then
       region_now=FULL
    else
       rr=` expr $r - 1 `
       region_now=${regions[$rr]}
    fi
    export region_now=${region_now}
    #for 00Z cycle
    if [ ${cycle} -eq 00 ] ; then
       fstart=` expr $fstart_r1 + 36`
       fend=` expr $fend_r2 + 12`
    fi
    #for 12Z cycle
    if [ ${cycle} -eq 12 ] ; then
       fstart=` expr $fstart_r1 + 24`
       fend=` expr $fend_r2 + 0`
    fi
    fhr=${fstart}
    while [ $fhr -le $fend ] ; do #loop over forecast hour
       if [ $fhr -lt 10 ] ; then
           hr=0${fhr}
       else
           hr=${fhr}
       fi
       export hr=${hr}
       n=1
       while [ $n -le $nexp ] ; do #loop over experiments
           nn=` expr $n - 1 `
           export model_fcst_now=${model_fcst[$nn]}
           #if directory of partial sum data provided use this directory, else use output directory
           if [ -n "$contable_dir" ] ; then
              export contable_dir_lookin="${contable_dir}/${cycle}Z/${model_fcst[$nn]}"
           else
              export contable_dir_lookin="${DATA_OUTmodel}/${model_fcst[$nn]}/${cycle}Z"
           fi
           #run MET Stat Analysis to filter partial sum files by forecast hour, valid date range
           #threshold, and region
           echo "------------------------------------------------------------"
           echo "----------> Filtering Partial Sum Files"
           echo "----------> Using files from: ${contable_dir_lookin}"
           echo "------------------------------------------------------------"
           stat_analysis -lookin ${contable_dir_lookin}/precip*.txt -config ${MET_HOME}/config_files/StatAnalysisConfig_precip -v ${verbose}
           n=` expr $n + 1 `
       done
#############################################################################
# Time Series Plots
#############################################################################
       #### Submit python statistic computing and plotting script
       echo "------------------------------------"
       echo "----------> Plotting threshold time series by forecast hour  ${region_now} ${start_date} ${end_date} f${hr} c${cycle} ${model_var} ${threshold[$tt]}"     
       export modellist=${model_fcst[@]}
       export fcsthr=${hr}
       export DATA_OUTimgs_now=${DATA_OUTimgs}/${cycle}Z/${region_now}
       export varname=${model_var}
       export reg=${region_now}
       export thrs=${threshold[$tt]}
       export nstats=`echo $plot_stats_list |wc -w`
       export stats=${plot_stats[@]}
       python ${MET_HOME}/plot/plot_precip_ts.py
       echo "------------------------------------"
       echo
       echo
       echo
       fhr=` expr $hr + 24`
    done
    r=` expr $r + 1 `
    echo
  done
  t=` expr $t + 1 `
  echo 
  echo 
  echo
done
#
r=0
while [ $r -le $nreg ] ; do #loop over region
   if [ $r -eq 0 ] ; then
      region_now=FULL
   else
      rr=` expr $r - 1 `
      region_now=${regions[$rr]}
   fi
   #for 00Z cycle
   if [ ${cycle} -eq 00 ] ; then
      fstart=` expr $fstart_r1 + 36`
      fend=` expr $fend_r2 + 12`
   fi
   #for 12Z cycle
   if [ ${cycle} -eq 12 ] ; then
      fstart=` expr $fstart_r1 + 24`
      fend=` expr $fend_r2 + 0`
   fi
   fhr=${fstart}
   while [ $fhr -le $fend ] ; do #loop over forecast hour
      if [ $fhr -lt 10 ] ; then
         hr=0${fhr}
      else
         hr=${fhr}
      fi
      #### Submit python statistic computing and plotting script
      echo "------------------------------------"
      echo "----------> Plotting threshold mean by forecast hour ${region_now} ${start_date} ${end_date} f${hr} c${cycle} ${model_var}"     
      export modellist=${model_fcst[@]}
      export fcsthr=${hr}
      export DATA_OUTimgs_now=${DATA_OUTimgs}/${cycle}Z/${region_now}
      export varname=${model_var}
      export reg=${region_now}
      export nstats=`echo $plot_stats_list |wc -w`
      export stats=${plot_stats[@]}
      python ${MET_HOME}/plot/plot_precip_tsmean.py
      echo "------------------------------------"
      fhr=` expr $hr + 24`
   done 
   r=` expr $r + 1 `
   echo
   echo
   echo
done
#############################################################################
# 2D Plots
#############################################################################
r=0
while [ $r -le $nreg ] ; do #loop over region
   if [ $r -eq 0 ] ; then
      region_now=FULL
   else
      rr=` expr $r - 1 `
      region_now=${regions[$rr]}
   fi
   #for 00Z cycle
   if [ ${cycle} -eq 00 ] ; then
      fstart=` expr $fstart_r1 + 36`
      fend=` expr $fend_r2 + 12`
   fi
   #for 12Z cycle
   if [ ${cycle} -eq 12 ] ; then
      fstart=` expr $fstart_r1 + 24`
      fend=` expr $fend_r2 + 0`
   fi
   #### Submit python statistic computing and plotting script
   echo "------------------------------------"
   echo "----------> Plotting threshold-forecast hour mean by forecast hour ${region_now} ${start_date} ${end_date} f${hr} c${cycle} ${model_var}"     
   export modellist=${model_fcst[@]}
   export fstart=${fstart}
   export fend=${fend}
   export DATA_OUTimgs_now=${DATA_OUTimgs}/${cycle}Z/${region_now}
   export varname=${model_var}
   export reg=${region_now}
   export thrs_levels=${threshold[@]}
   export nstats=`echo $plot_stats_list |wc -w`
   export stats=${plot_stats[@]}
   python ${MET_HOME}/plot/plot_precip_2dmean.py
   echo "------------------------------------"
   r=` expr $r + 1 `
   echo
   echo
   echo
done
#
endscript=`date +%s`
runtime_s=$((endscript-startscript))
runtime_m=$((runtime_s/60))
echo
echo
echo
echo "Run time: $runtime_s s; $runtime_m m"
