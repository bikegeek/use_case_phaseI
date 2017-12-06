#!/bin/ksh
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
echo "Run time: $runtime_s s; $runtime_m m"
