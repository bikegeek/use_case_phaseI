#!/bin/ksh
#############################################################################
###################################### Computing
#############################################################################
startscript=`date +%s`
#############################################################################
##### Set array variables
set -A model_fcst $model_fcst_list
set -A DATA_IN_model_fcst $DATA_IN_model_fcst_list
set -A model_fcst_dump $model_fcst_dump_list
set -A regions $sfc_regions_list
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
while [ $r -le $nsreg ] ; do
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
       if [ -e "${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf00${model_fcst_dump[$nn]}${date}" ] ; then
          fhr=${fstart}
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
                  echo "-------------> Running Grid Stat ${model_fcst[$nn]} f00 ${date}   ${model_fcst[$nn]} ${fcstdate}f${hr}"
                  echo "-------> Surface"
                  grid_stat ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf${hr}${model_fcst_dump[$nn]}${fcstdate} ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf00${model_fcst_dump[$nn]}${date} ${MET_HOME}/config_files/GridStatConfig_sfc -outdir ${DATA_OUTmodel}/${model_fcst[$nn]}/sfc/${cycle}Z -v ${verbose}
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
          echo "------- Surface"
          stat_analysis -lookin ${DATA_OUTmodel}/${model_fcst[$nn]}/sfc/${cycle}Z -job filter -dump_row ${DATA_OUTmodel}/${model_fcst[$nn]}/sfc/${cycle}Z/parsum_v${vdate}.txt -fcst_valid_beg ${vdate}'_'${vhr}0000 -v ${verbose}
          echo "------------------------------------------------------------"
          echo
          echo
       else
          echo "------------------------------------------------------------"
          echo "-------------> ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf00${model_fcst_dump[$nn]}${date} does not exist"
          echo "------------------------------------------------------------"
          echo
          echo
       fi
       date=`$ndate +24 ${date}`
   done
   #copy file to directory, if given
   if [ -n "$parsum_dir" ] ; then
      echo "Copying files to ${parsum_dir}/sfc/${cycle}Z/${model_fcst[$nn]}"
      if [ -d ${parsum_dir}/sfc/${cycle}Z/${model_fcst[$nn]} ] ; then
         cp ${DATA_OUTmodel}/${model_fcst[$nn]}/sfc/${cycle}Z/parsum_v*.txt ${parsum_dir}/sfc/${cycle}Z/${model_fcst[$nn]}/.
      else
         mkdir ${parsum_dir}/sfc/${cycle}Z/${model_fcst[$nn]}
         cp ${DATA_OUTmodel}/${model_fcst[$nn]}/sfc/${cycle}Z/parsum_v*.txt ${parsum_dir}/sfc/${cycle}Z/${model_fcst[$nn]}/.
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
echo "Compute run time: $runtime_s s; $runtime_m m"
#############################################################################
###################################### Plotting
#############################################################################
################
#${MET_HOME}/scripts/plot_grid2grid_sfc.sh 1>${DATA_OUT}/log/plot_grid2grid_sfc_c${cycle}.out 2>&1 &
################
startscript=`date +%s`
#############################################################################
##### Set array variables
set -A model_fcst $model_fcst_list
set -A DATA_IN_model_fcst $DATA_IN_model_fcst_list
set -A model_fcst_dump $model_fcst_dump_list
set -A regions $sfc_regions_list
#############################################################################
#gather lists of variables
export listvar1=MET_HOME,ndate
export listvar2=model_fcst_list,DATA_IN_model_fcst_list,model_fcst_dump_list,DATA_OUTmain,parsum_dir,start_date,end_date,fstart,fend,fint,grid,regions_list,sfc_regions_list,plot_stats_list,verbose,nexp,nreg,nsreg,cycle,var_name_now,var_level_now,region_now
export listvar3=DATA_OUT,DATA_OUTmodel,DATA_OUTimgs,DATA_OUTlog
export listvar="$listvar1,$listvar2,$listvar3"
##### Submit scripts for surface partial sum statistics
export var_name_list_sfc="TMP RH SPFH HPBL PRES PRMSL TMP UGRD VGRD WEASD TSOIL SOILW CAPE CWAT PWAT HGT TMP TOZNE"
set -A var_name_sfc $var_name_list_sfc
export nvar_sfc=`echo $var_name_list_sfc |wc -w`
export var_level_list_sfc="Z2 Z2 Z2 L0 Z0 L0 Z0 Z10 Z10 Z0 Z10-0 Z10-0 Z0 L0 L0 L0 L0 L0"
set -A var_level_sfc $var_level_list_sfc
#
v=1
while [ $v -le $nvar_sfc ] ; do #submit plotting script by variables
   vv=` expr $v - 1 `
   export var_name_now=${var_name_sfc[$vv]}
   export var_level_now=${var_level_sfc[$vv]}
   r=0
   while [ $r -le $nsreg ] ; do #loop over region
     if [ $r -eq 0 ] ; then
        region_now=FULL
     else
        rr=` expr $r - 1 `
        region_now=${regions[$rr]}
     fi
     export region_now=${region_now}
     echo "----> Submitting SFC: ${var_name_now}${var_level_now} ${region_now}"
     if [ $batch = yes] ; then
          $SUBJOB -e $listvar -a $ACCOUNT  -q "$CUE2RUN" -g $GROUP -p 1/1/N -r 2048/1 -t 6:00:00 -j plot_grid2grid_sfc_fbar_c${cycle}_${var_name_now}${var_level_now}_${region_now} -o ${DATA_OUT}/log/plot_grid2grid_sfc_fbar_c${cycle}_${var_name_now}${var_level_now}_${region_now}.out  ${MET_HOME}/scripts/plot_grid2grid_sfc_fbar.sh
      else
          ${MET_HOME}/scripts/plot_grid2grid_sfc_fbar.sh 1>${DATA_OUT}/log/plot_grid2grid_sfc_fbar_c${cycle}_${var_name_now}${var_level_now}_${region_now}.out 2>&1 &
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
echo "Plot run time: $runtime_s s; $runtime_m m"
