#!/bin/ksh
startscript=`date +%s`
#############################################################################
##### Set array variables
set -A model_fcst $model_fcst_list
set -A DATA_IN_model_fcst $DATA_IN_model_fcst_list
set -A model_fcst_dump $model_fcst_dump_list
##### Set list of variables to calculate
#export var_name_list="TMP DPT TMAX TMIN RH SPFH TMP APCP ACPCP PRATE CPRAT WATR WEASD SNOD PWAT CRAIN CSNOW CFRZR CICEP MSLET PRES PRMSL LFTX 4LFTX CAPE CIN CWAT CWORK TOZNE VRATE HGT HGT HINDEX HPBL ICEC LAND U-GWD UFLX UGRD UGRD V-GWD VFLX VGRD VGRD GUST DLWRF ULWRF ULWRF DSWRF USWRF USWRF ALBDO GFLUX LHTFL SHTFL SUNSD PEVPR TCDC TCDC TCDC TCDC TCDC TCDC PRES PRES PRES PRES PRES PRES PRES PRES TMP TMP TMP WILT FLDCP SOILW SOILW SOILW SOILW TSOIL TSOIL TSOIL TSOIL TMP PRES HGT ICAHT UGRD VGRD VWSH RH POT VVEL UGRD VGRD TMP TMP PRES HGT ICAHT UGRD VGRD RH RH USTM VSTM HLCY PRES SPFH HGT RH PLPL CAPE CAPE CIN CIN"
#export var_level_list="Z2 Z2 Z2 Z2 Z2 Z2 Z0 Z0 Z0 Z0 Z0 Z0 Z0 Z0 L0 Z0 Z0 Z0 Z0 L0 Z0 L0 Z0 Z0 Z0 Z0 L0 L0 L0 L0 Z0 L0 Z0 Z0 Z0 Z0 Z0 Z0 Z10 L0 Z0 Z0 Z10 L0 Z0 Z0 Z0 L0 Z0 Z0 L0 Z0 Z0 Z0 Z0 Z0 Z0 L0 L0 L0 L0 L0 L0 L0 L0 L0 L0 L0 L0 L0 L0 L0 L0 L0 Z0 Z0 Z0-10 Z10-40 Z40-100 Z100-200 Z0-10 Z10-40 Z40-100 Z100-200 L0 L0 L0 L0 L0 L0 L0 L9950 L9950 L9950 L9950 L9950 L9950 L0 L0 L0 L0 L0 L0 L0 L0 Z60-0 Z60-0 Z30-0 Z80 Z80 L0 L0 L255-0 L255-0 L180-0 L255-0 L180-0"
#export var_GRIBlvltyp_list="105 105 105 105 105 105 01 01 01 01 01 01 01 01 200 01 01 01 01 102 01 102 01 01 01 01 200 200 200 220 01 204 01 01 01 01 01 01 105 220 01 01 105 220 01 01 01 08 01 01 08 01 01 01 01 01 01 200 211 214 224 234 244 212 222 232 242 213 223 233 243 213 223 233 01 01 112 112 112 112 112 112 112 112 07 07 07 07 07 07 07 107 107 107 107 107 107 06 06 06 06 06 06 200 204 106 106 106 105 105 04 04 116 116 116 116 116"
#export var_GRIB1ptv_list="2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 129 2 2 129 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 133 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 130 130 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 129 2 2 2 2"
export var_name_list="TMP UGRD"
export var_level_list="Z2 Z10"
export var_GRIBlvltyp_list="105 105"
export var_GRIB1ptv_list="2 2"
export nvar=`echo $var_name_list |wc -w`
set -A var_name $var_name_list
set -A var_level $var_level_list
set -A var_GRIBlvltyp $var_GRIBlvltyp_list
set -A var_GRIB1ptv $var_GRIB1ptv_list
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
          echo ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgb${fhr}${model_fcst_dump[$nn]}${date} >> ${DATA_OUTmodel_model2model}/${model_fcst[$nn]}/${cycle}Z/${fday}/${model_fcst[$nn]}_${fday}files.txt
      done
      date=`$ndate +24 ${date}`
   done
   n=` expr $n + 1 `
done
#run Series Analysis, first model listed in model list is used as comparison/"observation"
export model_obs="${model_fcst[0]}"
n=2
while [ $n -le $nexp ] ; do #loop over experiments
   nn=` expr $n - 1 `
   v=1
   while [ $v -le $nvar ] ; do #loop over variables
        vv=` expr $v - 1 `
        echo "------------------------------------------------------------"
        echo "-------------> Running Series Analysis ${model_obs} ${model_fcst[$nn]} ${sdate}-${edate} ${fday}"
        export model_fcst_now="${model_fcst[$nn]}"
        export var_name_now="${var_name[$vv]}"
        export var_level_now="${var_level[$vv]}"
        export var_GRIBlvltyp_now="${var_GRIBlvltyp[$vv]}"
        export var_GRIB1ptv_now="${var_GRIB1ptv[$vv]}"
        series_analysis -fcst ${DATA_OUTmodel_model2model}/${model_fcst[$nn]}/${cycle}Z/${fday}/${model_fcst[$nn]}_${fday}files.txt -obs ${DATA_OUTmodel_model2model}/${model_obs}/${cycle}Z/${fday}/${model_obs}_${fday}files.txt -config ${MET_HOME}/config_files/SeriesAnalysisConfig_model2model -out ${DATA_OUTmodel_model2model}/${model_fcst[$nn]}/${cycle}Z/${fday}/seriesanalysis_${var_name_now}_${var_GRIBlvltyp_now}${var_level_now}.nc -v ${verbose}
        v=` expr $v + 1 `
   done
   n=` expr $n + 1 `
   echo "------------------------------------------------------------"
   echo
   echo
   echo
done
#############################################################################
##### Create plots
export modellist=${model_fcst[@]}
v=1
while [ $v -le $nvar ] ; do #loop over variables
  vv=` expr $v - 1 `
  export var_name_now="${var_name[$vv]}"
  export var_level_now="${var_level[$vv]}"
  export var_GRIBlvltyp_now="${var_GRIBlvltyp[$vv]}"
  export var_GRIB1ptv_now="${var_GRIB1ptv[$vv]}"
  echo "------------------------------------------------------------"
  echo "-------------> Plotting ${var_name_now} ${var_GRIBlvltyp_now}${var_level_now} ${sdate}-${edate} ${fday}"
  python ${MET_HOME}/plot/plot_plots2d_model2model.py
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
