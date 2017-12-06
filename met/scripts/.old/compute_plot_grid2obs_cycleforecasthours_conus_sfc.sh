#!/bin/ksh
startscript=`date +%s`
#############################################################################
##### Set array variables
set -A model_fcst $model_fcst_list
set -A DATA_IN_model_fcst $DATA_IN_model_fcst_list
set -A model_fcst_dump $model_fcst_dump_list
set -A conus_sfc_regions $conus_sfc_regions_list
#############################################################################
###################################### Computing
#############################################################################
#format desired conus_sfc_grid ID for correct use in MET Point Stat config file
conus_sfc_GG=`echo $conus_sfc_grid |cut -c2- `
if [ $conus_sfc_GG -lt 10 ] ; then
   conus_sfc_GGG=G00$conus_sfc_GG
fi
if ([ $conus_sfc_GG -ge 10 ] && [ $conus_sfc_GG -lt 100 ]) ; then
   conus_sfc_GGG=G0$conus_sfc_GG
fi
if [ $conus_sfc_GG -ge 100 ] ; then
   conus_sfc_GGG=G$conus_sfc_GG
fi
export conus_sfc_GGG=${conus_sfc_GGG}
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
          #run MET Grid Stat
          validdate=`$ndate +${hr} ${date}`
          vhr=`echo $validdate |cut -c9-10 `
          if [ $validdate -le 2017031923 ]; then
             #use ndas files
             dir="ndas"
             if [  $(((cycle/6)*6)) -eq $cycle ] ; then
                xdate=$validdate
                suffix="tm00"
                prefix="nam"
             else
                xdate=$($ndate +3 $validdate )
                suffix=tm03
                prefix="ndas"
             fi
          else
             dir="nam"
             #use nam files
             if [  $(((vhr/6)*6)) -eq $vhr ] ; then
                xdate=$validdate
                suffix=tm00
                prefix="nam"
             else
                xdate=$($ndate +3 $validdate )
                suffix=tm03
                prefix="nam"
             fi
          fi
          vyyyymmdd=`echo $xdate |head -c8 `
          vcc=`echo $xdate |cut -c9-10 `
          #run MET PB2nc to get prepbufr files in format MET can read
          if [ ! -e "${DATA_OUTmodel}/${model_fcst[$nn]}/conus_sfc/${cycle}Z/prepbufr.${prefix}.${vyyyymmdd}.t${vcc}z.${suffix}.nc" ] ; then
             if [ -e "${prepbufr_dir}/${dir}/${dir}.${vyyyymmdd}/${prefix}.t${vcc}z.prepbufr.${suffix}" ] ; then
                echo "------------------------------------------------------------"
                echo "-------------> Creating prepbufr netcdf file valid ${validdate}"
                pb2nc ${prepbufr_dir}/${dir}/${dir}.${vyyyymmdd}/${prefix}.t${vcc}z.prepbufr.${suffix} ${DATA_OUTmodel}/${model_fcst[$nn]}/conus_sfc/${cycle}Z/prepbufr.${prefix}.${vyyyymmdd}.t${vcc}z.${suffix}.nc ${MET_HOME}/config_files/PB2NCConfig_conus_sfc
             else
                echo "------------------------------------------------------------"
                echo "-------------> ${prepbufr_dir}/${dir}/${dir}.${vyyyymmdd}/${prefix}.t${vcc}z.prepbufr.${suffix}  does not exist"
             fi
          fi
          if [ -e "${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf${hr}${model_fcst_dump[$nn]}${date}" ] ; then
             echo "------------------------------------------------------------"
             echo "-------------> Running Point Stat ${model_fcst[$nn]} ${date}f${hr} valid ${validdate}"
             point_stat ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf${hr}${model_fcst_dump[$nn]}${date} ${DATA_OUTmodel}/${model_fcst[$nn]}/conus_sfc/${cycle}Z/prepbufr.${prefix}.${vyyyymmdd}.t${vcc}z.${suffix}.nc ${MET_HOME}/config_files/PointStatConfig_conus_sfc -outdir ${DATA_OUTmodel}/${model_fcst[$nn]}/conus_sfc/${cycle}Z -v ${verbose}
          else
               echo "------------------------------------------------------------"
               echo "-------------> ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf${hr}${model_fcst_dump[$nn]}${date} does not exist"
          fi
          fhr=` expr $hr + $fint_conus_sfc`
          echo
       done
       #filter by valid date using MET Stat Analysis
       echo "----------> Running Stat Analysis ${model_fcst[$nn]} i${date}"
       idate=`echo $date |head -c8 `
       stat_analysis -lookin ${DATA_OUTmodel}/${model_fcst[$nn]}/conus_sfc/${cycle}Z -job filter -dump_row ${DATA_OUTmodel}/${model_fcst[$nn]}/conus_sfc/${cycle}Z/grid2obs_i${date}.txt -fcst_init_beg ${idate}'_'${cycle}0000 -v ${verbose}
       echo "------------------------------------------------------------"
       echo
       echo
       date=`$ndate +24 ${date}`
   done
   #copy file to directory, if given
   if [ -n "$grid2obs_dir" ] ; then
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
##### Submit scripts for partial sums CONUS surface statistics
export var_name_list_conus_sfc="TMP RH DPT PRMSL"
set -A var_name_conus_sfc $var_name_list_conus_sfc 
export nvar_conus_sfc=`echo $var_name_list_conus_sfc |wc -w`
v=1
while [ $v -le $nvar_conus_sfc ] ; do #submit plotting script by variable
   vv=` expr $v - 1 `
   export var_name_now=${var_name_conus_sfc[$vv]}
   if [ ${var_name_now} = PRMSL ]; then
      export var_level_list="Z0"
   #elif [ ${var_name_now} = UGRD_VGRD ]; then
   #   export var_level_list="Z10"
   else
      export var_level_list="Z2"
   fi
   ${MET_HOME}/scripts/plot_grid2obs_cycleforecasthours_conus_sfc.sh 1>${DATA_OUT}/log/plot_grid2obs_conus_sfc_c${cycle}_${var_name_now}.out 2>&1 &
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
