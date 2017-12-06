#!/bin/ksh
startscript=`date +%s`
#############################################################################
##### Set array variables
set -A model_fcst $model_fcst_list
set -A DATA_IN_model_fcst $DATA_IN_model_fcst_list
set -A model_fcst_dump $model_fcst_dump_list
set -A upper_air_regions $upper_air_regions_list
set -A conus_sfc_regions $conus_sfc_regions_list
set -A plot_stats $plot_stats_list
#############################################################################
###################################### Computing
#############################################################################
##### Use MET Point Stat and Stat Analysis to generate partial sums
#prep upper-air regions to analyze for input into MET Point Stat Config File
r=1
while [ $r -le $nuareg ] ; do
  rr=` expr $r - 1 `
  if [ $rr -eq 0 ]; then
     upper_air_regions_path='"'"${MET_HOME}/poly/${upper_air_regions[$rr]}.poly"'"'
  else
     upper_air_regions_path[$rr]=' "'"${MET_HOME}/poly/${upper_air_regions[$rr]}.poly"'"'
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
       #run MET pb2nc to get gdas prepbufr files in format MET can read
       echo "------------------------------------------------------------"
             echo "-------------> Creating gdas prepbufr netcdf file"
       if [ -e "${prepbufr_dir}/gdas/prepbufr.gdas.${date}" ] ; then
          pb2nc ${prepbufr_dir}/gdas/prepbufr.gdas.${date} ${DATA_OUTmodel}/${model_fcst[$nn]}/upper_air/${cycle}Z/prepbufr.gdas.${date}.nc ${MET_HOME}/config_files/PB2NCConfig_upper_air
       else
          echo "------------------------------------------------------------"
          echo "-------------> ${gdas_dir[$nn]}/prepbufr.gdas.${date}  does not exist"
       fi
       #run MET pb2nc to get ndas/gdas prepbufr files in format MET can read
       if [ $date -le 2017031923 ]; then
          #use ndas files
          dir="ndas"
          if [  $(((cycle/6)*6)) -eq $cycle ] ; then
             xdate=$date
             suffix="tm00"
             prefix="nam"
          else
             xdate=$($ndate +3 $date )
             suffix=tm03
             prefix="ndas"
          fi
       else
          dir="nam"
          #use nam files
          if [  $(((cycle/6)*6)) -eq $cycle ] ; then
             xdate=$date
             suffix=tm00
             prefix="nam"
          else
             xdate=$($ndate +3 $date )
             suffix=tm03
             prefix="nam"
          fi
       fi
       vyyyymmdd=`echo $xdate |head -c8 `
       vcc=`echo $xdate |cut -c9-10 `
       if [ -e "${prepbufr_dir}/${dir}/${dir}.${vyyyymmdd}/${prefix}.t${vcc}z.prepbufr.${suffix}" ] ; then
             echo "------------------------------------------------------------"
             echo "-------------> Creating ${prefix} prepbufr netcdf file"
             pb2nc ${prepbufr_dir}/${dir}/${dir}.${vyyyymmdd}/${prefix}.t${vcc}z.prepbufr.${suffix} ${DATA_OUTmodel}/${model_fcst[$nn]}/conus_sfc/${cycle}Z/prepbufr.${prefix}.${vyyyymmdd}.t${vcc}z.${suffix}.nc ${MET_HOME}/config_files/PB2NCConfig_conus_sfc
          else
             echo "------------------------------------------------------------"
             echo "-------------> ${prepbufr_dir}/${dir}/${dir}.${vyyyymmdd}/${prefix}.t${vcc}z.prepbufr.${suffix}  does not exist" 
          fi
       fhr=${fstart}
       while [ $fhr -le $fend ] ; do #loop over forecast hours
          if [ $fhr -lt 10 ] ; then
             hr=0${fhr}
          else
             hr=${fhr}
          fi
          #run MET Point Stat
          fcstdate=`$ndate -${hr} ${date}`
          if [ -e "${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf${hr}${model_fcst_dump[$nn]}${fcstdate}" ] ; then
               echo "------------------------------------------------------------"
               echo "-------------> Running Point Stat for global upper-air grid2obs ${model_fcst[$nn]} ${fcstdate}f${hr} valid ${date}"
               point_stat ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf${hr}${model_fcst_dump[$nn]}${fcstdate} ${DATA_OUTmodel}/${model_fcst[$nn]}/upper_air/${cycle}Z/prepbufr.gdas.${date}.nc ${MET_HOME}/config_files/PointStatConfig_upper_air -outdir ${DATA_OUTmodel}/${model_fcst[$nn]}/upper_air/${cycle}Z -v ${verbose}
               echo "------------------------------------------------------------"
               echo "-------------> Running Point Stat for CONUS surface grid2obs ${model_fcst[$nn]} ${fcstdate}f${hr} valid ${date}"
               point_stat ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf${hr}${model_fcst_dump[$nn]}${fcstdate} ${DATA_OUTmodel}/${model_fcst[$nn]}/conus_sfc/${cycle}Z/prepbufr.${prefix}.${vyyyymmdd}.t${vcc}z.${suffix}.nc ${MET_HOME}/config_files/PointStatConfig_conus_sfc -outdir ${DATA_OUTmodel}/${model_fcst[$nn]}/conus_sfc/${cycle}Z -v ${verbose}
          else
               echo "------------------------------------------------------------"
               echo "-------------> ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf${hr}${model_fcst_dump[$nn]}${fcstdate} does not exist"
          fi
          fhr=` expr $hr + $fint`
       done
       #filter by valid date using MET Stat Analysis
       echo "----------> Running Stat Analysis ${model_fcst[$nn]} v${date}"
       vdate=`echo $date |head -c8 `
       vhr=`echo $date |cut -c9- `
       stat_analysis -lookin ${DATA_OUTmodel}/${model_fcst[$nn]}/upper_air/${cycle}Z -job filter -dump_row ${DATA_OUTmodel}/${model_fcst[$nn]}/upper_air/${cycle}Z/grid2obs_v${vdate}.txt -fcst_valid_beg ${vdate}'_'${vhr}0000 -v ${verbose}
       stat_analysis -lookin ${DATA_OUTmodel}/${model_fcst[$nn]}/conus_sfc/${cycle}Z -job filter -dump_row ${DATA_OUTmodel}/${model_fcst[$nn]}/conus_sfc/${cycle}Z/grid2obs_v${vdate}.txt -fcst_valid_beg ${vdate}'_'${vhr}0000 -v ${verbose}
       echo "------------------------------------------------------------"
       echo
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
      echo "Copying files to ${grid2obs_dir}/conus_sfc/${cycle}Z/${model_fcst[$nn]}"
      if [ -d ${grid2obs_dir}/conus_sfc/${cycle}Z/${model_fcst[$nn]} ] ; then
         cp ${DATA_OUTmodel}/${model_fcst[$nn]}/conus_sfc/${cycle}Z/grid2obs_v*.txt ${grid2obs_dir}/conus_sfc/${cycle}Z/${model_fcst[$nn]}/.
      else
         mkdir ${grid2obs_dir}/conus_sfc/${cycle}Z/${model_fcst[$nn]}
         cp ${DATA_OUTmodel}/${model_fcst[$nn]}/conus_sfc/${cycle}Z/grid2obs_v*.txt ${grid2obs_dir}/conus_sfc/${cycle}Z/${model_fcst[$nn]}/.
      fi

   fi
   n=` expr $n + 1 `
done
#############################################################################
###################################### Plotting
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
