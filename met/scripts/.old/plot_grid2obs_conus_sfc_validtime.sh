#!/bin/ksh
startscript=`date +%s`
#############################################################################
##### Set array variables
set -A model_fcst $model_fcst_list
set -A DATA_IN_model_fcst $DATA_IN_model_fcst_list
set -A model_fcst_dump $model_fcst_dump_list
set -A regions $conus_sfc_regions_list
set -A plot_stats $plot_stats_list
set -A var_level $var_level_list
#############################################################################
export group="conus_sfc"
##### Run MET Stat Analysis to filter upper air point stat files
export nlev=`echo $var_level_list |wc -w`
vl=1
while [ $vl -le $nlev ] ; do #loop over variable level
   vvl=` expr $vl - 1 `
   export var_level_now=${var_level[$vvl]}
   r=0
   while [ $r -le $ncsfcreg ] ; do #loop over region
      if [ $r -eq 0 ] ; then
         region_now=FULL
      else
         rr=` expr $r - 1 `
         region_now=${regions[$rr]}
      fi
      export region_now=${region_now}
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
            export model_fcst_now=${model_fcst[$nn]}
            nn=` expr $n - 1 `
            #if directory of partial sum data provided use this directory, else use output directory
            if [ -n "$grid2obs_dir" ] ; then
               export grid2obs_dir_lookin="${grid2obs_dir}/${group}/${cycle}Z/${model_fcst[$nn]}"
            else
               export grid2obs_dir_lookin="${DATA_OUTmodel}/${model_fcst[$nn]}/${group}/${cycle}Z"
            fi
            #run MET Stat Analysis to filter anomalous upper air point stat files by forecast hour, valid date range,
            #variable name, variable level, and region
            echo "------------------------------------------------------------"
            echo "----------> Filtering Upper Air Point Stat Sum Files"
            echo "----------> Using files from: ${grid2obs_dir_lookin}"
            echo "------------------------------------------------------------"
            #export dump_row_name="${DATA_OUTmodel}/${model_fcst_now}/${group}/${cycle}Z/${region_now}/grid2obs_f${hr}_${var_name_now}${var_level_now}.txt"
            stat_analysis -lookin ${grid2obs_dir_lookin}/grid2obs*.txt -config ${MET_HOME}/config_files/StatAnalysisConfig_grid2obs -v ${verbose}
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
         python ${MET_HOME}/plot/plot_grid2obs_conus_sfc_ts.py
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
      python ${MET_HOME}/plot/plot_grid2obs_conus_sfc_tsmean.py
      echo "------------------------------------"
      echo
      echo 
      echo 
      r=` expr $r + 1 `
   done
   vl=` expr $vl + 1 `
done
#
endscript=`date +%s`
runtime_s=$((endscript-startscript))
runtime_m=$((runtime_s/60))
echo
echo
echo
echo "Run time: $runtime_s s; $runtime_m m"
