#!/bin/ksh
startscript=`date +%s`
#############################################################################
set -A model_fcst $model_fcst_list
set -A DATA_IN_model_fcst $DATA_IN_model_fcst_list
set -A model_fcst_dump $model_fcst_dump_list
set -A regions $regions_list
set -A var_level $var_level_list
set -A plot_stats $plot_stats_list
#############################################################################
##### Set flags and paths for output directory 
#create main output directory
#echo "------------------------------------------------------------"
#echo "-------------> Output Directory"
#echo "${DATA_OUT}"
#export DATA_OUTmodel="${DATA_OUT}/model"
#export DATA_OUTconfig="${DATA_OUT}/config"
#export DATA_OUTimgs="${DATA_OUT}/imgs"
#export DATA_OUTlog="${DATA_OUT}/log"
#create branches of output directory
#mkdir ${DATA_OUTmodel}
#mkdir ${DATA_OUTconfig}
#mkdir ${DATA_OUTimgs}
#mkdir ${DATA_OUTlog}
#create output directories for models
#n=1
#while [ $n -le $nexp ] ; do
#  nn=` expr $n - 1 `
#  mkdir ${DATA_OUTmodel}/${model_fcst[$nn]}
#  mkdir ${DATA_OUTconfig}/${model_fcst[$nn]}
#  for hr in $asub ; do
#    mkdir ${DATA_OUTmodel}/${model_fcst[$nn]}/f${hr}
#    for reg in ${regions_list} ; do
#      mkdir ${DATA_OUTmodel}/${model_fcst[$nn]}/f${hr}/${reg}
#    done
#  done
#  n=` expr $n + 1 `
#done
#create output directories for images
#for hr in $asub ; do
#  mkdir ${DATA_OUTimgs}/f${hr}
#  for reg in ${regions_list} ; do
#      mkdir ${DATA_OUTimgs}/f${hr}/${reg}
#  done
#done
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
#prep regions to analyze for input into MET Grid Stat Config File
r=1
while [ $r -le $nreg ] ; do
  rr=` expr $r - 1 `
  if [ $rr -eq 0 ]; then
     regions_config='"'"${MET_HOME}/poly/${regions[$rr]}.poly"'"'
  else
     regions_config[$rr]=' "'"${MET_HOME}/poly/${regions[$rr]}.poly"'"'
  fi
  r=` expr $r + 1 `
done
#prep levels to analyze for input into MET Grid Stat Config File
export nlev=${#var_level[@]}
vl=1
while [ $vl -le $nlev ] ; do
  vvl=` expr $vl - 1 `
  if [ $vvl -eq 0 ]; then
     var_level_config='"'"${var_level[$vvl]}"'"'
  else
     var_level_config[$vvl]=' "'"${var_level[$vvl]}"'"'
  fi
  vl=` expr $vl + 1 `
done
#run MET Grid Stat and Stat Analysis
n=1
while [ $n -le $nexp ] ; do
   nn=` expr $n - 1 `
#......................... create MET Grid Stat Config File
cat <<EOF >> ${DATA_OUTconfig}/${model_fcst[$nn]}/GridStatConfig_${var_name}
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
        name  = "${var_name}" ;
        level = [ $( printf "%s," "${var_level_config[@]}" | cut -d "," -f 1-${#var_level_config[@]} ) ];
        GRIB_lvl_typ = ${var_GRIBlvltyp};
        GRIB1_ptv = ${var_GRIB1ptv};
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
   poly = [ $( printf "%s," "${regions_config[@]}" | cut -d "," -f 1-${#regions_config[@]} )];
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
output_prefix  = "${var_name}";
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
                  #save dates of analysis file with existing forecast model file to text file; for first variable on as to not keep appending
                  echo $date >> ${DATA_OUTmodel}/${model_fcst[$nn]}/f${hr}/date_modelfile_exists_${var_name}.txt
                  echo "------------------------------------------------------------"
                  echo "-------------> Running Grid Stat ${model_fcst[$nn]}, ${model_fcst[$nn]}_anl f${hr}   ${var_name} ${var_level[@]}"
                  grid_stat ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbf${hr}${model_fcst_dump[$nn]}${fcstdate} ${DATA_IN_model_fcst[$nn]}/${model_fcst[$nn]}/pgbanl${model_fcst_dump[$nn]}${date} ${DATA_OUTconfig}/${model_fcst[$nn]}/GridStatConfig_${var_name} -outdir ${DATA_OUTmodel}/${model_fcst[$nn]}/f${hr} -log ${DATA_OUTlog}/${model_fcst[$nn]}_f${hr}_${var_name}.log -v ${verbose}
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
           r=1
           while [ $r -le $nreg ] ; do
             rr=` expr $r - 1 `
             vl=1
             while [ $vl -le $nlev ] ; do
                 vvl=` expr $vl - 1 `
                 stat_analysis -lookin ${DATA_OUTmodel}/${model_fcst[$nn]}/f${hr} -job filter -dump_row ${DATA_OUTmodel}/${model_fcst[$nn]}/f${hr}/${regions[$rr]}/statanalysisCNT_${var_name}_${var_level[$vvl]}.txt -line_type CNT -vx_mask ${regions[$rr]} -fcst_var ${var_name} -fcst_lev ${var_level[$vvl]} -v ${verbose} 
                 stat_analysis -lookin ${DATA_OUTmodel}/${model_fcst[$nn]}/f${hr} -job filter -dump_row ${DATA_OUTmodel}/${model_fcst[$nn]}/f${hr}/${regions[$rr]}/statanalysisSL1L2_${var_name}_${var_level[$vvl]}.txt -line_type SL1L2 -vx_mask ${regions[$rr]} -fcst_var ${var_name} -fcst_lev ${var_level[$vvl]} -v ${verbose}
                 vl=` expr $vl + 1 `
             done
             r=` expr $r + 1 `
           done
       done
   n=` expr $n + 1 `
done
echo
echo
echo
echo 
#############################################################################
##### Use python to plot output
#plotting
if [ $plot == yes ] ; then
   r=1
   while [ $r -le $nreg ] ; do
       rr=` expr $r - 1 `
       for hr in $asub; do
           echo "------------------------------------------------------------"
           echo 'Plotting' ${var_name} 'f'${hr} ${regions[$rr]}
           vl=1
           while [ $vl -le $nlev ] ; do
             vvl=` expr $vl - 1 `
             echo "------------------------------------"
             echo "----------> ${var_level[$vvl]}" 
             export modellist=${model_fcst[@]}
             export fhr=${hr}
             export DATA_OUTimgs_now=${DATA_OUTimgs}/f${hr}/${regions[$rr]}
             export varname=${var_name}
             export varlevel=${var_level[$vvl]}
             export reg=${regions[$rr]}
             export statlist=${plot_stats[@]}
             python ${MET_HOME}/plot/out_sl1l2stat.py
             python ${MET_HOME}/plot/out_cntstat.py
             python ${MET_HOME}/plot/plot_sl1l2stat.py
             python ${MET_HOME}/plot/plot_cntstat.py
             vl=` expr $vl + 1 `
          done
       done 
       echo
       echo
       r=` expr $r + 1 `
   done
fi 
#
endscript=`date +%s`
runtime_s=$((endscript-startscript))
runtime_m=$((runtime_s/60))
echo
echo
echo
echo "Run time: $runtime_s s; $runtime_m m"
