#!/bin/sh
echo
startscript=`date +%s`
#############################################################################
##### Set flags and paths for data
##### File format /${model}/pgb${asub}${dump}${yyyymmddcc}"
##### Variables to Change
#forecast models
#export model_fcst=("pr4rn_1505") #first listing is "truth" model, i.e nonparallel; being verified against own analysis
#export DATA_IN_model_fcst=("/global/noscrub/emc.glopara/archive" "/global/noscrub/emc.glopara/archive") #can be more than one cooresponding to number of model_fcst
#export model_fcst_dump=(".gfs." ".gfs.")
#file characteristics
#export asub="240" #forecast hour
#export sdate="2015051000" #year month date cycle
#export edate="2015123100" #year month date cycle
#export grid="G2"   #pgb file resolution, G2->2.5deg; G3->1deg; G4->0.5deg; G193->0.25deg
#characteristics of variables to analyze
#export var_name=("HGT" "HGT" "HGT" "HGT" "HGT" "HGT" "HGT" "HGT" "HGT")
#export var_level=("P1000" "P850" "P700" "P500" "P200" "P100" "P50" "P10")
#export var_GRIBlvltyp=("100" "100" "100" "100" "100" "100" "100" "100" "100")
#export var_GRIB1ptv=("2" "2" "2" "2" "2" "2" "2" "2" "2")
#export var_name=("HGT")
#export var_level=("P500")
#export var_GRIBlvltyp=("100")
#export var_GRIB1ptv=("2")
#MET paths
#export MET_HOME="/global/save/Mallory.Row/VRFY/met" #MET home
#export verbose="1" #verbosity of MET output; 1-5
#export plot="yes" #add scripts to generate plots at line 222
#export plot_stats=("RMSE")
#output data paths
#export DATA_OUT="/global/save/Mallory.Row/VRFY/met/out_gridstat_METregrid"
#etc
#export ndate="${MET_HOME}/nwprod/util/exec/ndate"
#export nexp=${#model_fcst[@]}
#export nstats=${#plot_stats[@]}
#export nvar=${#var_name[@]}
#############################################################################
##### Set flags and paths for output directory 
#create main output directory
echo "------------------------------------------------------------"
echo "-------------> Output Directory"
if [ -d "$DATA_OUT" ] ; then
   echo "$DATA_OUT directory exists, removing and creating new one"
   rm -r $DATA_OUT
   mkdir $DATA_OUT
else
   echo "$DATA_OUT directory not found, creating new directory"
   mkdir $DATA_OUT
fi
echo
export DATA_OUTmodel="${DATA_OUT}/model"
export DATA_OUTconfig="${DATA_OUT}/config"
export DATA_OUTimgs="${DATA_OUT}/imgs"
export DATA_OUTlog="${DATA_OUT}/log"
#create branches of output directory
mkdir ${DATA_OUTmodel}
mkdir ${DATA_OUTconfig}
mkdir ${DATA_OUTimgs}
mkdir ${DATA_OUTlog}
#create output directories for models
n=1
while [ $n -le $nexp ] ; do
  nn=` expr $n - 1 `
  mkdir ${DATA_OUTmodel}/${model_fcst[$nn]}
  mkdir ${DATA_OUTconfig}/${model_fcst[$nn]}
  for hr in $asub ; do
      mkdir ${DATA_OUTmodel}/${model_fcst[$nn]}/f${hr}
  done
  n=` expr $n + 1 `
done
#create output directories for images
for hr in $asub ; do
    mkdir ${DATA_OUTimgs}/f${hr}
done
#############################################################################
##### Use MET Grid Stat and Stat Analysis to generate continous stats using 
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
#run MET Grid Stat and Stat Analysis
n=1
while [ $n -le $nexp ] ; do
   nn=` expr $n - 1 `
   v=1 
   while [ $v -le $nvar ] ; do
       vv=` expr $v - 1 `
#......................... create MET Grid Stat Config File
cat <<EOF >> ${DATA_OUTconfig}/${model_fcst[$nn]}/GridStatConfig_${var_name[$vv]}_${var_GRIBlvltyp[$vv]}${var_level[$vv]}
////////////////////////////////////////////////////////////////////////////////
//
// Grid Stat configuration file.
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
obtype = "${model_fcst[$nn]}_anl";

////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////

//
// Verification grid
//
regrid = {
   to_grid    = "${GGG}";
   method     = BILIN;
   width      = 2;
   vld_thresh = 0.5;
}

////////////////////////////////////////////////////////////////////////////////

cat_thresh  = [ NA ];
cnt_thresh  = [ NA ];
cnt_logic   = UNION;
wind_thresh = [ NA ];
wind_logic  = UNION;

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
};
obs = fcst;

////////////////////////////////////////////////////////////////////////////////

//
// Climatology mean data
//
climo_mean = {

   file_name = [];
   field     = [];

   regrid = {
      method     = NEAREST;
      width      = 1;
      vld_thresh = 0.5;
   }

   time_interp_method = DW_MEAN;
   match_day          = FALSE;
   time_step          = 21600;
}

///////////////////////////////////////////////////////////////////////////////

//
// Verification masking regions
//

mask = {
   grid = [ "FULL" ];
   poly = [];
}

////////////////////////////////////////////////////////////////////////////////

//
// Confidence interval settings
//

ci_alpha  = [ 0.05 ];

boot = {
   interval = PCTILE;
   rep_prop = 1.0;
   n_rep    = 0;
   rng      = "mt19937";
   seed     = "";
}

////////////////////////////////////////////////////////////////////////////////

//
// Data smoothing methods
//
interp = {
   field      = BOTH;
   vld_thresh = 1.0;

   type = [
      {
         method = NEAREST;
         width  = 1;
      }
   ];
}

////////////////////////////////////////////////////////////////////////////////

//
// Statistical output types
//


     output_flag = {
        fho    = NONE;
        ctc    = NONE;
        cts    = NONE;
        mctc   = NONE;
        mcts   = NONE;
        cnt    = STAT;
        sl1l2  = STAT;
        sal1l2 = NONE;
        vl1l2  = NONE;
        val1l2 = NONE;
        pct    = NONE;
        pstd   = NONE;
        pjc    = NONE;
        prc    = NONE;
        nbrctc = NONE;
        nbrcts = NONE;
        nbrcnt = NONE;
 }
//
// NetCDF matched pairs output file
//

nc_pairs_flag   = {

   latlon = FALSE;
   raw    = FALSE;
   diff   = FALSE;
   climo  = FALSE;
   weight = FALSE;
   nbrhd  = FALSE;
};

grid_weight_flag = COS_LAT;
////////////////////////////////////////////////////////////////////////////////

rank_corr_flag = FALSE;
tmp_dir        = "/tmp";
output_prefix  = "${var_name[$vv]}_${var_GRIBlvltyp[$vv]}${var_level[$vv]}";
version        = "V5.2";

////////////////////////////////////////////////////////////////////////////////

EOF
#.........................
     date=${sdate}
     while [ $date -le $edate ] ; do
           for hr in $asub; do
               fcstdate=`$ndate -${hr} ${date}`
               #run MET Grid Stat
               if [ -e "${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf${hr}${model_fcst_dump[$nn]}${fcstdate}" ] ; then
                  echo $date >> ${DATA_OUTmodel}/${model_fcst[$nn]}/f${hr}/date_modelfile_exits.txt
                  echo "------------------------------------------------------------"
                  echo "-------------> Running Grid Stat ${model_fcst[$nn]}, ${model_fcst[$nn]}_anl f${hr}   ${var_name[$vv]} ${var_GRIB1ptv[$vv]} ${var_GRIBlvltyp[$vv]} ${var_level[$vv]}"
                  grid_stat ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf${hr}${model_fcst_dump[$nn]}${fcstdate} ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbanl${model_fcst_dump[$nn]}${date} ${DATA_OUTconfig}/${model_fcst[$nn]}/GridStatConfig_${var_name[$vv]}_${var_GRIBlvltyp[$vv]}${var_level[$vv]} -outdir ${DATA_OUTmodel}/${model_fcst[$nn]}/f${hr} -log ${DATA_OUTlog}/${model_fcst[$nn]}_f${hr}_${var_name[$vv]}_${var_GRIBlvltyp[$vv]}${var_level[$vv]}.log -v ${verbose}
                  #if [ $date -eq $edate ]; then
                  #   ncecat ${DATA_OUTmodel}/${model_fcst[$nn]}/grid_stat_${var_name[$vv]}_${var_GRIBlvltyp[$vv]}${var_level[$vv]}_${hr}0000L_*_pairs.nc -O ${DATA_OUTmodel}/${model_fcst[$nn]}/f${hr}_${var_name[$vv]}_${var_GRIBlvltyp[$vv]}${var_level[$vv]}_${sdate}_${edate}.nc
                  #   ncra ${DATA_OUTmodel}/${model_fcst[$nn]}/f${hr}_${var_name[$vv]}_${var_GRIBlvltyp[$vv]}${var_level[$vv]}_${sdate}_${edate}.nc -O ${DATA_OUTmodel}/${model_fcst[$nn]}/f${hr}_${var_name[$vv]}_${var_GRIBlvltyp[$vv]}${var_level[$vv]}_${sdate}_${edate}_avg.nc
                  # fi
               else 
                 echo "------------------------------------------------------------"
                 echo "-------------> ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf${hr}${model_fcst_dump[$nn]}${fcstdate} does not exist"
               fi     
           done
       date=`$ndate +24 ${date}`
       done
       for hr in $asub ; do
           echo "------------------------------------"
           echo "----------> Running Stat Analysis"
           stat_analysis -lookin ${DATA_OUTmodel}/${model_fcst[$nn]}/f${hr} -job filter -dump_row ${DATA_OUTmodel}/${model_fcst[$nn]}/f${hr}/statanalysisCNT_${var_name[$vv]}_${var_GRIBlvltyp[$vv]}${var_level[$vv]}.txt -line_type CNT -v ${verbose} 
           stat_analysis -lookin ${DATA_OUTmodel}/${model_fcst[$nn]}/f${hr} -job filter -dump_row ${DATA_OUTmodel}/${model_fcst[$nn]}/f${hr}/statanalysisSL1L2_${var_name[$vv]}_${var_GRIBlvltyp[$vv]}${var_level[$vv]}.txt -line_type SL1L2 -v ${verbose}
       done
       v=` expr $v + 1 `
   done
   n=` expr $n + 1 `
   echo
   echo
   echo
done
echo
echo
echo
echo 
#############################################################################
##### Use python to plot output
#plotting
if [ $plot == yes ] ; then
   v=1
   while [ $v -le $nvar ] ; do
       vv=` expr $v - 1 `
       for hr in $asub; do 
           export modellist=${model_fcst[@]}
           export fhr=${hr}
           export DATA_OUTimgs_now=${DATA_OUTimgs}/f${hr}
           export varname=${var_name[$vv]}
           export varGRIBlvltyp=${var_GRIBlvltyp[$vv]}
           export varlevel=${var_level[$vv]}
           export statlist=${plot_stats[@]}
           echo "------------------------------------------------------------"
           echo 'Plotting' $varname 'f'${hr} $varGRIBlvltyp $varlevel
           python ${MET_HOME}/plot/out_sl1l2stat.py
           #python ${MET_HOME}/plot/out_cntstat.py
           python ${MET_HOME}/plot/plot_sl1l2stat.py
           #python ${MET_HOME}/plot/plot_cntstat.py
       done 
       v=` expr $v + 1 `
   done
fi 

endscript=`date +%s`
runtime_s=$((endscript-startscript))
runtime_m=$((runtime_s/60))
echo
echo
echo
echo "Run time: $runtime_s s; $runtime_m m"
