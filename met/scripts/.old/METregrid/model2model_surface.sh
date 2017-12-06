#!/bin/sh
startscript=`date +%s`
#############################################################################
##### Set flags and paths for data
##### File format /${model}/pgb${asub}${dump}${yyyymmddcc}"
##### Variables to Change
#models being used as "forecast" models
export model_fcst=("pr4rn_1505") #can be more than one
export DATA_IN_model_fcst=("/global/noscrub/emc.glopara/archive") #can be more than one cooresponding to number of model_fcst
export model_fcst_dump=(".gfs.")
#models being used as "observation"
export model_obs="gfs2016"
export DATA_IN_model_obs="/global/noscrub/emc.glopara/archive"
export model_obs_dump=".gfs."
#file characteristics
export asub="f06 f12 f18 f24" #either forecast four [fxxx] or analysis [anl]
export sdate="2015060100" #year month date cycle
export edate="2015123100" #year month date cycle
export grid="G2"   #pgb file resolution, G2->2.5deg; G3->1deg; G4->0.5deg; G193->0.25deg
#characteristics of variables to analyze
export var_name=("TMP" "DPT" "TMAX" "TMIN" "RH" "SPFH" "TMP" "APCP" "ACPCP" "PRATE" "CPRAT" "WATR" "WEASD" "SNOD" "PWAT" "CRAIN" "CSNOW" "CFRZR" "CICEP" "MSLET" "PRES" "PRMSL" "LFTX" "4LFTX" "CAPE" "CIN" "CWAT" "CWORK" "TOZNE" "VRATE" "HGT" "HGT" "HINDEX" "HPBL" "ICEC" "LAND" "U-GWD" "UFLX" "UGRD" "UGRD" "V-GWD" "VFLX" "VGRD" "VGRD" "GUST" "DLWRF" "ULWRF" "ULWRF" "DSWRF" "USWRF" "USWRF" "ALBDO" "GFLUX" "LHTFL" "SHTFL" "SUNSD" "PEVPR" "TCDC" "TCDC" "TCDC" "TCDC" "TCDC" "TCDC" "PRES" "PRES" "PRES" "PRES" "PRES" "PRES" "PRES" "PRES" "TMP" "TMP" "TMP" "WILT" "FLDCP" "SOILW" "SOILW" "SOILW" "SOILW" "TSOIL" "TSOIL" "TSOIL" "TSOIL" "TMP" "PRES" "HGT" "ICAHT" "UGRD" "VGRD" "VWSH" "RH" "POT" "VVEL" "UGRD" "VGRD" "TMP" "TMP" "PRES" "HGT" "ICAHT" "UGRD" "VGRD" "RH" "RH" "USTM" "VSTM" "HLCY" "PRES" "SPFH" "HGT" "RH" "PLPL" "CAPE" "CAPE" "CIN" "CIN")
export var_level=("Z2" "Z2" "Z2" "Z2" "Z2" "Z2" "Z0" "Z0" "Z0" "Z0" "Z0" "Z0" "Z0" "Z0" "L0" "Z0" "Z0" "Z0" "Z0" "L0" "Z0" "L0" "Z0" "Z0" "Z0" "Z0" "L0" "L0" "L0" "L0" "Z0" "L0" "Z0" "Z0" "Z0" "Z0" "Z0" "Z0" "Z10" "L0" "Z0" "Z0" "Z10" "L0" "Z0" "Z0" "Z0" "L0" "Z0" "Z0" "L0" "Z0" "Z0" "Z0" "Z0" "Z0" "Z0" "L0" "L0" "L0" "L0" "L0" "L0" "L0" "L0" "L0" "L0" "L0" "L0" "L0" "L0" "L0" "L0" "L0" "Z0" "Z0" "Z0-10" "Z10-40" "Z40-100" "Z100-200" "Z0-10" "Z10-40" "Z40-100" "Z100-200" "L0" "L0" "L0" "L0" "L0" "L0" "L0" "L9950" "L9950" "L9950" "L9950" "L9950" "L9950" "L0" "L0" "L0" "L0" "L0" "L0" "L0" "L0" "Z60-0" "Z60-0" "Z30-0" "Z80" "Z80" "L0" "L0" "L255-0" "L255-0" "L180-0" "L255-0" "L180-0") 
export var_GRIBlvltyp=("105" "105" "105" "105" "105" "105" "01" "01" "01" "01" "01" "01" "01" "01" "200" "01" "01" "01" "01" "102" "01" "102" "01" "01" "01" "01" "200" "200" "200" "220" "01" "204" "01" "01" "01" "01" "01" "01" "105" "220" "01" "01" "105" "220" "01" "01" "01" "08" "01" "01" "08" "01" "01" "01" "01" "01" "01" "200" "211" "214" "224" "234" "244" "212" "222" "232" "242" "213" "223" "233" "243" "213" "223" "233" "01" "01" "112" "112" "112" "112" "112" "112" "112" "112" "07" "07" "07" "07" "07" "07" "07" "107" "107" "107" "107" "107" "107" "06" "06" "06" "06" "06" "06" "200" "204" "106" "106" "106" "105" "105" "04" "04" "116" "116" "116" "116" "116")
export var_GRIB1ptv=("2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "129" "2" "2" "129" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "133" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "130" "130" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "2" "129" "2" "2" "2" "2")
#export var_name=("TMP")
#export var_level=("Z2")
#export var_GRIBlvltyp=("105")
#export var_GRIB1ptv=("2")
#MET paths
export MET_HOME="/global/save/Mallory.Row/VRFY/met" #MET home
export verbose="1" #verbosity of MET output; 1-5
export plot="yes" #add scripts to generate plots at line 222
#output data paths
export DATA_OUT="/global/save/Mallory.Row/VRFY/met/out_surface_METregrid"
#etc
export ndate="${MET_HOME}/nwprod/util/exec/ndate"
export copygb="${MET_HOME}/nwprod/util/exec/copygb"
export nexp=${#model_fcst[@]}
export nvar=${#var_name[@]}
#############################################################################
##### Set flags and paths for output directory 
#create main output directory
if [ -d "$DATA_OUT" ]
then
   echo "$DATA_OUT directory exists, removing and creating new one"
   rm -r $DATA_OUT
   mkdir $DATA_OUT
else
   echo "$DATA_OUT directory not found, creating new directory"
   mkdir $DATA_OUT
fi
export DATA_OUTmodel="${DATA_OUT}/model"
export DATA_OUTconfig="${DATA_OUT}/config"
export DATA_OUTimgs="${DATA_OUT}/imgs"
export DATA_OUTlog="${DATA_OUT}/log"
#create branches of output directory
mkdir ${DATA_OUTmodel}
mkdir ${DATA_OUTconfig}
mkdir ${DATA_OUTimgs}
mkdir ${DATA_OUTlog}
#create output directories for "forecast" models
n=1
while [ $n -le $nexp ] ; do
  nn=` expr $n - 1 `
  mkdir ${DATA_OUTmodel}/${model_fcst[$nn]}
  mkdir ${DATA_OUTimgs}/${model_fcst[$nn]}
  n=` expr $n + 1 `
done
#create output directories for "observation" models
mkdir ${DATA_OUTmodel}/${model_obs}
#############################################################################
##### Create text files of list of model file paths
#output file that contains forecast model file paths
n=1
while [ $n -le $nexp ] ; do
   date=${sdate}
   while [ $date -le $edate ] ; do
       for hr in $asub; do
           nn=` expr $n - 1 `
           echo ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgb${hr}${model_fcst_dump[$nn]}${date} >> ${DATA_OUTmodel}/${model_fcst[$nn]}/${model_fcst[$nn]}_files.txt 
       done
       date=`$ndate +24 ${date}`
   done
   n=` expr $n + 1 `
done
#output file that contains forecast model file paths
date=${sdate}
while [ $date -le $edate ] ; do
   for hr in $asub; do
           echo ${DATA_IN_model_obs}/${model_obs}/pgb${hr}${model_obs_dump}${date} >> ${DATA_OUTmodel}/${model_obs}/${model_obs}_files.txt
    done
    date=`$ndate +24 ${date}`
done
#############################################################################
##### Use MET Series Analysis to generate output
##### to edit output statistics edit config file template below
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
#loop through MET Series Analysis by experiment and variable
n=1
v=1
while [ $n -le $nexp ] ; do
    nn=` expr $n - 1 `
    while [ $v -le $nvar ] ; do
        vv=` expr $v - 1 `
#......................... create MET Series Analysis Config File
cat <<EOF >> ${DATA_OUTconfig}/SeriesAnalysisConfig_model2model_${var_name[$vv]}_${var_GRIBlvltyp[$vv]}${var_level[$vv]}
// Series-Analysis configuration file.
//
// For additional information, see the MET_BASE/config/README file.
//
////////////////////////////////////////////////////////////////////////////////

//
// Output model name to be written
//
model = "${model_fcst[$nn]}";

//
// Output observation type to be written
//
obtype = "${model_obs}";

////////////////////////////////////////////////////////////////////////////////

//
// Verification grid
//

regrid = { to_grid = "${GGG}"; method = BILIN; width = 2; }
////////////////////////////////////////////////////////////////////////////////


//
// Forecast and observation fields to be verified
//
fcst = {

   field = [
      {
        name  = "${var_name[$vv]}";
        level = [ "${var_level[$vv]}" ];
        GRIB_lvl_typ = ${var_GRIBlvltyp[$vv]};
        GRIB1_ptv = ${var_GRIB1ptv[$vv]};
      }
   ];

}
obs = fcst;

////////////////////////////////////////////////////////////////////////////////

//
// Climatology mean data
//

////////////////////////////////////////////////////////////////////////////////

//
// Confidence interval settings
//

////////////////////////////////////////////////////////////////////////////////

//
// Verification masking regions
//

//
// Number of grid points to be processed concurrently.  Set smaller to use
// less memory but increase the number of passes through the data.
//
block_size = 70000;

//
// Ratio of valid matched pairs to compute statistics for a grid point
//
vld_thresh = 1.0;

////////////////////////////////////////////////////////////////////////////////

//
// Statistical output types
//
output_stats = {
   fho    = [];
   ctc    = [];
   cts    = [];
   mctc   = [];
   mcts   = [];
   cnt    = [ "OBAR", "ME", "RMSE"];
   sl1l2  = [];
   sal1l2 = [];
   pct    = [];
   pstd   = [];
   pjc    = [];
   prc    = [];
}


////////////////////////////////////////////////////////////////////////////////

rank_corr_flag = FALSE;
tmp_dir        = "/tmp";
version        = "V5.2";

////////////////////////////////////////////////////////////////////////////////

EOF
#.........................
        #run MET Series Analysis
        echo "------------------------------------------------------------"
        echo "-------------> Running Series Analysis ${model_fcst[$nn]}, ${model_obs}    ${var_name[$vv]} ${var_GRIB1ptv[$vv]} ${var_GRIBlvltyp[$vv]} ${var_level[$vv]}"
        series_analysis -fcst ${DATA_OUTmodel}/${model_fcst[$nn]}/${model_fcst[$nn]}_files.txt -obs ${DATA_OUTmodel}/${model_obs}/${model_obs}_files.txt -out ${DATA_OUTmodel}/${model_fcst[$nn]}/${model_fcst[$nn]}_${model_obs}_${var_name[$vv]}_${var_GRIBlvltyp[$vv]}${var_level[$vv]}.nc -config ${DATA_OUTconfig}/SeriesAnalysisConfig_model2model_${var_name[$vv]}_${var_GRIBlvltyp[$vv]}${var_level[$vv]} -log ${DATA_OUTlog}/${model_fcst[$nn]}_${model_obs}_${var_name[$vv]}_${var_GRIBlvltyp[$vv]}${var_level[$vv]}.log -v ${verbose}
        if [ $plot = yes ]
        then
           #export environmental variables for plot scripts
           export datafile="${DATA_OUTmodel}/${model_fcst[$nn]}/${model_fcst[$nn]}_${model_obs}_${var_name[$vv]}_${var_GRIBlvltyp[$vv]}${var_level[$vv]}.nc"
           export model_fcst_name=${model_fcst[$nn]}
           export model_obs_name=${model_obs}
           export varname=${var_name[$vv]}
           export varGRIBlvltyp=${var_GRIBlvltyp[$vv]}
           export varlevel=${var_level[$vv]}
           #run plotting scripts
           echo "-------------> Plotting $model_fcst_name, $model_obs_name   $varname ${var_GRIB1ptv[$vv]} $varGRIBlvltyp $varlevel"
           python ${MET_HOME}/plot/plot_ME.py
           echo "------------------------------------------------------------"
           echo
           echo
       fi
       v=` expr $v + 1 `
    done
    n=` expr $n + 1 `
done
endscript=`date +%s`
runtime_s=$((endscript-startscript))
runtime_m=$((runtime_s/60))
echo
echo
echo
echo "Run time: $runtime_s s; $runtime_m m"
