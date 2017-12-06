#!/bin/ksh
startscript=`date +%s`
#############################################################################
##### Set array variables
set -A model_fcst $model_fcst_list
set -A DATA_IN_model_fcst $DATA_IN_model_fcst_list
set -A model_fcst_dump $model_fcst_dump_list
##### Set list of variables to calculate
export var_name_list="TCDC TCDC TCDC TCDC DSWRF USWRF USWRF DLWRF ULWRF ULWRF PWAT APCP ALBDO TMP CWAT"
export var_level_list="L0 L0 L0 L0 Z0 Z0 L0 Z0 Z0 L0 L0 Z0 Z0 Z2 L0"
export var_GRIBlvltyp_list="200 214 224 234 01 01 08 01 01 08 200 01 01 105 200"
export var_GRIB1ptv_list="2 2 2 2 2 2 2 2 2 2 2 2 2 2 2"
export var_obs_list="cldt cldl cldm cldt sw_sfc_down sw_sfc_up sw_toa_up lw_sfc_down lw_sfc_up lw_toa_up tpw precip alb tmp2m clwp"
export nvar=`echo $var_name_list |wc -w`
set -A var_name $var_name_list
set -A var_level $var_level_list
set -A var_GRIBlvltyp $var_GRIBlvltyp_list
set -A var_GRIB1ptv $var_GRIB1ptv_list
set -A var_obs $var_obs_list
#############################################################################
##### Use MET Series Analysis to generate differences from model #1 as comparsion
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
#format forecast hours
if [ ${fday} == anl ]; then
 export fhr4="anl"
 export fhr3="anl"
 export fhr2="anl"
 export fhr1="anl"
 export fhr_list=$(eval echo \${fhr_list$fday:-"$fhr1 $fhr2 $fhr3 $fhr4"})
elif [ ${fday} == d00 ]; then
 export fhr4="00"
 export fhr3="00"
 export fhr2="00"
 export fhr1="00"
 export fhr_list=$(eval echo \${fhr_list$fday:-"f$fhr1 f$fhr2 f$fhr3 f$fhr4"})
else
 day=`echo $fday |cut -c2- `
 fhr4=` expr ${day} \* 24 `
 fhr3=` expr $fhr4 - 6  `
 fhr2=` expr $fhr4 - 12  `
 fhr1=` expr $fhr4 - 18 `
 if [ $fhr1 -lt 10 ]; then fhr1=0$fhr1 ; fi
 export fhr_list=$(eval echo \${fhr_list$fday:-"f$fhr1 f$fhr2 f$fhr3 f$fhr4"})
fi
#create text files containing model files to be including in Series Analysis
n=1
while [ $n -le $nexp ] ; do #loop over experiments
   nn=` expr $n - 1 `
   export model_fcst_now=${model_fcst[$nn]}
   sdate=${start_date}${cycle}
   edate=${end_date}${cycle}
   date=${sdate}
   while [ $date -le $edate ] ; do #loop over date range
      for fhr in ${fhr_list} ; do #loop over forecast hours
          echo ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgb${fhr}${model_fcst_dump[$nn]}${date} >> ${DATA_OUTmodel_model2obs}/${model_fcst[$nn]}/${cycle}Z/${fday}/${model_fcst[$nn]}_${fday}files.txt
      done
      date=`$ndate +24 ${date}`
   done
   n=` expr $n + 1 `
done
#create text files containing observation files to be including in Series Analysis
sdate=${start_date}${cycle}
edate=${end_date}${cycle}
date=${sdate}
while [ $date -le $edate ] ; do #loop over date range
   v=1
   while [ $v -le $nvar ] ; do #loop over variables
      vv=` expr $v - 1 `
      export var_name_now="${var_name[$vv]}"
      export var_level_now="${var_level[$vv]}"
      export var_GRIBlvltyp_now="${var_GRIBlvltyp[$vv]}"
      #patition for data source
      if [ ${var_name_now} = TMP ]; then
         data_source="ghcn_cams"
      elif [ ${var_name_now} = APCP ]; then
         data_source="gpcp"
      else
         data_source="ceres"
      fi
      for fhr in ${fhr_list} ; do #loop over forecast hours
          if [ ${fhr} = anl ]; then
             hr=0
          else
             hr=`echo $fhr |cut -c2- `
          fi
          validdate=`$ndate +${hr} ${date}`
          vyyyy=`echo $validdate |cut -c1-4 `
          vmm=`echo $validdate |cut -c5-6 `
          #partition between using monthly mean files or climatology
          if [ ${climo} = no ]; then
             time_frq="mm"
             file_suffix=${vyyyy}${vmm}
          else
             time_frq="climo"
             file_suffix=${vmm}
          fi
          echo ${obs_dir}/${data_source}_${time_frq}/${data_source}_${time_frq}_${file_suffix}.nc >> ${DATA_OUTobs_model2obs}/${cycle}Z/${fday}/${var_name_now}_${var_GRIBlvltyp_now}${var_level_now}_${fday}files.txt
      done
      v=` expr $v + 1 `
   done
   date=`$ndate +24 ${date}`
done
#run Series Analysis
n=1
while [ $n -le $nexp ] ; do #loop over experiments
   nn=` expr $n - 1 `
   export model_fcst_now="${model_fcst[$nn]}"
   v=1
   while [ $v -le $nvar ] ; do #loop over variables
        vv=` expr $v - 1 `
        export var_name_now="${var_name[$vv]}"
        export var_level_now="${var_level[$vv]}"
        export var_GRIBlvltyp_now="${var_GRIBlvltyp[$vv]}"
        export var_GRIB1ptv_now="${var_GRIB1ptv[$vv]}"
        export var_obs_now="${var_obs[$vv]}"
        #name for observations in SeriesAnalysis Config
        if [ ${climo} = no ]; then
           if [ ${var_name_now} = TMP ]; then
              export obs="ghcn_cams_mm"
           elif [ ${var_name_now} = APCP ]; then
              export obs="gpcp_mm"
           else
              export obs="ceres_mm"
           fi
        else
           if [ ${var_name_now} = TMP ]; then
              export obs="ghcn_cams_climo"
           elif [ ${var_name_now} = APCP ]; then
              export obs="gpcp_climo"
           else
              export obs="ceres_climo"
           fi
        fi
        echo "------------------------------------------------------------"
        echo "-------------> Running Series Analysis ${var_name_now} ${obs} ${model_fcst[$nn]} ${sdate}-${edate} ${fday}"
        series_analysis -fcst ${DATA_OUTmodel_model2obs}/${model_fcst[$nn]}/${cycle}Z/${fday}/${model_fcst[$nn]}_${fday}files.txt -obs ${DATA_OUTobs_model2obs}/${cycle}Z/${fday}/${var_name_now}_${var_GRIBlvltyp_now}${var_level_now}_${fday}files.txt -paired -config ${MET_HOME}/config_files/SeriesAnalysisConfig_model2obs -out ${DATA_OUTmodel_model2obs}/${model_fcst[$nn]}/${cycle}Z/${fday}/seriesanalysis_${var_name_now}_${var_GRIBlvltyp_now}${var_level_now}.nc -v ${verbose}
        v=` expr $v + 1 `
   done
   n=` expr $n + 1 `
   echo "------------------------------------------------------------"
   echo
   echo
   echo
done
#############################################################################
##### Plot
export modellist=${model_fcst[@]}
v=1
while [ $v -le $nvar ] ; do #loop over variables
  vv=` expr $v - 1 `
  export var_name_now="${var_name[$vv]}"
  export var_level_now="${var_level[$vv]}"
  export var_GRIBlvltyp_now="${var_GRIBlvltyp[$vv]}"
  export var_GRIB1ptv_now="${var_GRIB1ptv[$vv]}"
  #patition for data source
  if [ ${var_name_now} = TMP ]; then
     export data_source="GHCN_CAMS"
  elif [ ${var_name_now} = APCP ]; then
     export data_source="GPCP"
  else
     export data_source="CERES"
  fi
  echo "------------------------------------------------------------"
  echo "-------------> Plotting ${var_name_now} ${var_GRIBlvltyp_now}${var_level_now} ${sdate}-${edate} ${fday}"
  python ${MET_HOME}/plot/plot_plots2d_model2obs.py
  echo "------------------------------------------------------------"
  echo
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
