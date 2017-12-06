#!/bin/ksh
startscript=`date +%s`
#############################################################################
##### Set array variables
set -A model_fcst $model_fcst_list
set -A DATA_IN_model_fcst $DATA_IN_model_fcst_list
set -A model_fcst_dump $model_fcst_dump_list
set -A regions $regions_list
set -A plot_stats $plot_stats_list
set -A var_level $var_level_list
#############################################################################
export group="pres"
##### Run MET Stat Analysis to filter pressure level partial sum files
export nlev=`echo $var_level_list |wc -w`
vl=1
while [ $vl -le $nlev ] ; do #loop over variable level
   vvl=` expr $vl - 1 `
   export var_level_now=${var_level[$vvl]}
   fhr=${fstart}
   while [ $fhr -le $fend ] ; do #loop over forecast hour
      if [ $fhr -lt 10 ] ; then
         hr=0${fhr}
      else
         hr=${fhr}
      fi
      export hr=${hr}
      n=1
      while [ $n -le $nexp ] ; do #loop over experiment
         nn=` expr $n - 1 `
         export model_fcst_now=${model_fcst[$nn]}
         #if directory of partial sum data provided use this directory, else use output directory
         if [ -n "$parsum_dir" ] ; then
            export parsum_dir_lookin="${parsum_dir}/${group}/${cycle}Z/${model_fcst[$nn]}"
         else
            export parsum_dir_lookin="${DATA_OUTmodel}/${model_fcst[$nn]}/${group}/${cycle}Z"
         fi
         #run MET Stat Analysis to filter anomalous partial sum files by forecast hour, valid date range,
         #variable name, variable level, and region
         echo "------------------------------------------------------------"
         echo "----------> Filtering Partial Sum Files"
         echo "----------> Using files from: ${parsum_dir_lookin}"
         echo "------------------------------------------------------------"
         stat_analysis -lookin ${parsum_dir_lookin}/parsum*.txt -config ${MET_HOME}/config_files/StatAnalysisConfig_grid2grid -v ${verbose}
         n=` expr $n + 1 `
      done
#############################################################################
# Time Series Plots
#############################################################################
      #### Submit python statistic computing and plotting script
      echo "------------------------------------"
      echo "----------> Plotting time series ${region_now} ${start_date} ${end_date} f${hr} c${cycle} ${var_name_now} ${var_level[$vvl]}"     
      export modellist=${model_fcst[@]}
      export fcsthr=${hr}
      export DATA_OUTimgs_now=${DATA_OUTimgs}/${cycle}Z/${region_now}
      export varname=${var_name_now}
      export varlevel=${var_level[$vvl]}
      export reg=${region_now}
      export nstats=`echo $plot_stats_list |wc -w`
      export stats=${plot_stats[@]}
      python ${MET_HOME}/plot/plot_grid2grid_pres_ts.py
      echo "------------------------------------"
      fhr=` expr $hr + $fint`
   done
   echo "------------------------------------"
   echo "----------> Plotting forecast hour mean time series ${region_now} ${start_date} ${end_date} c${cycle} ${var_name_now} ${var_level[$vvl]}"     
   export modellist=${model_fcst[@]}
   export DATA_OUTimgs_now=${DATA_OUTimgs}/${cycle}Z/${region_now}
   export varname=${var_name_now}
   export varlevel=${var_level[$vvl]}
   export reg=${region_now}
   export nstats=`echo $plot_stats_list |wc -w`
   export stats=${plot_stats[@]}
   python ${MET_HOME}/plot/plot_grid2grid_pres_tsmean.py
   echo "------------------------------------"
   echo
   echo 
   echo 
   vl=` expr $vl + 1 `
done
#############################################################################
# 2D Plots
#############################################################################
fhr=${fstart}
while [ $fhr -le $fend ] ; do #loop over forecast hour
   if [ $fhr -lt 10 ] ; then
      hr=0${fhr}
   else
      hr=${fhr}
   fi
   #### Submit python statistic computing and plotting script
   echo "------------------------------------"
   echo "----------> Plotting date-pressure ${region_now} ${start_date} ${end_date} f${hr} c${cycle} ${var_name_now}"     
   export modellist=${model_fcst[@]}
   export fcsthr=${hr}
   export DATA_OUTimgs_now=${DATA_OUTimgs}/${cycle}Z/${region_now}
   export varname=${var_name_now}
   export varlevellist=${var_level[@]}
   export nlev=`echo $var_level_list |wc -w`
   export reg=${region_now}
   export nstats=`echo $plot_stats_list |wc -w`
   export stats=${plot_stats[@]}
   python ${MET_HOME}/plot/plot_grid2grid_pres_tp.py
   echo 
   echo
   fhr=` expr $hr + $fint`
done
#### Submit python statistic computing and plotting script
echo "----------> Plotting forecast hour mean-pressure ${region_now} ${start_date} ${end_date} c${cycle} ${var_name_now}"     
export modellist=${model_fcst[@]}
export DATA_OUTimgs_now=${DATA_OUTimgs}/${cycle}Z/${region_now}
export varname=${var_name_now}
export varlevellist=${var_level[@]}
export nlev=`echo $var_level_list |wc -w`
export reg=${region_now}
export nstats=`echo $plot_stats_list |wc -w`
export stats=${plot_stats[@]}
python ${MET_HOME}/plot/plot_grid2grid_pres_tpmean.py
echo "------------------------------------"
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
