#!/bin/ksh
############## set machine variables
export machine=WCOSS              #WCOSS, WCOSS_C, THEIA
export machine=$(echo $machine|tr '[a-z]' '[A-Z]')
#MAKE SURE PATHS IN setup_envs.sh ARE SET CORRECTLY BEFORE RUNNING
set -a;. `pwd`/setup_envs.sh $machine
############## input variables
# set flags and paths for data ; file format /${model}/pgbf${fhr}${dump}${yyyymmddcc}
#export model_fcst_list="gfs" #first listing is "truth" model for model-to-model comparison in plots2d; in grid2grid, models being verified against own analysis, max. # 8
#export DATA_IN_model_fcst_list="/global/noscrub/emc.glopara/global" #can be more than one cooresponding to number in model_fcst_list
#export model_fcst_dump_list=".gfs." #can be more than one cooresponding to number in model_fcst_list
#
#export model_fcst_list="gfs ecm ukm cmc fno jma cfsr" #first listing is "truth" model for model-to-model comparison in plots2d; in grid2grid, models being verified against own analysis, max. # 9
#export DATA_IN_model_fcst_list="/global/noscrub/emc.glopara/global /global/noscrub/emc.glopara/global /global/noscrub/emc.glopara/global /global/noscrub/emc.glopara/global /global/noscrub/emc.glopara/global /global/noscrub/emc.glopara/global /global/noscrub/emc.glopara/global" #can be more than one cooresponding to number in model_fcst_list
#export model_fcst_dump_list=".gfs. .ecm. .ukm. .cmc. .fno. .jma. .cfsr." #can be more than one cooresponding to number in model_fcst_list
#
export model_fcst_list="gfs prnemsgiv" #first listing is "truth" model for model-to-model comparison in plots2d; in grid2grid, models being verified against own analysis, max. # 8
export DATA_IN_model_fcst_list="/global/noscrub/emc.glopara/global /gpfs/hps3/emc/global/noscrub/emc.glopara/archive" #can be more than one cooresponding to number in model_fcst_list
export model_fcst_dump_list=".gfs. .gfs." #can be more than one cooresponding to number in model_fcst_list
############## output variables
export DATA_OUTmain="/global/save/Mallory.Row/VRFY/met/out_prnemsgiv"
if [ -d "$DATA_OUTmain" ] ; then
   rm -r ${DATA_OUTmain}
fi   
mkdir ${DATA_OUTmain}
############## what to run
grid2grid=YES #grid-to-grid verification, using model's analysis as obs.
precip=NO #compute contingency table counts and plot statistics for 24 hr accumulated precip
grid2obs=NO #grid-to-obs verification
plots2d=NO #2D plots of model-to-model and model-to-obs comparaison 
#############################################################################
#### set variables and submit scripts
############################
if [ $grid2grid = YES ] ; then
   compute=yes #calculate partial sums
   plot=no #plot statistics from partial sums
   sfc=yes #compute and/or plot surface fields
   export batch=yes #submit jobs in batch or not
   export parsum_dir="/global/noscrub/Mallory.Row/archive/grid2grid" #where to save/access partial sum data from MET; unset(comment out) leaves in appropriate DATA_OUTmain folder
   #file characteristics ; file format /${model}/pgbf${fhr}${dump}${yyyymmddcc}
   export start_date="20170924" #year month date
   export end_date="20170927" #year month date
   export fcycle_list="00 06 12 18" #forecast cycles/hours to be verified at, two digit format 
   export fstart="0"  #forecast hour to start at
   export fend="384"   #forecast hour to end at
   export fint="6"  #interval of forecast hours                           
   export grid="G2"   #pgb file resolution, G2->2.5deg; G3->1deg; G4->0.5deg; G193->0.25deg
   #which regions to compute stats over
   export regions_list="NHX SHX TRO PNA" #regions to generate stats for besides full grid; needs .nc mask in $MET_HOME/poly
   export sfc_regions_list="NHX SHX N60 S60 TRO NPO SPO NAO SAO CONUS CAM NSA"
   #etc
   export plot_stats_list="ac bias rms msess rsd emd epv pcor" #stats to plot, options:ac bias rms msess rsd emd epv pcor
   export verbose="2" #verbosity of MET output; 1-5
   export nexp=`echo $model_fcst_list |wc -w`
   export nreg=`echo $regions_list |wc -w`
   export nsreg=`echo $sfc_regions_list |wc -w`
   #create stat output directories
   set -a;. ${MET_HOME}/scripts/mkdir_grid2grid.sh
   #gather lists of variables
   export listvar1=MET_HOME,ndate
   export listvar2=model_fcst_list,DATA_IN_model_fcst_list,model_fcst_dump_list,DATA_OUTmain,parsum_dir,start_date,end_date,fstart,fend,fint,grid,regions_list,sfc_regions_list,plot_stats_list,verbose,nexp,nreg,nsreg,cycle
   export listvar3=DATA_OUT,DATA_OUTmodel,DATA_OUTimgs,DATA_OUTlog
   export listvar="$listvar1,$listvar2,$listvar3"
   #submit scripts
   if [ $compute = no ] ; then
       if [ $plot = yes ] ; then
          for fcycle in $fcycle_list ; do
              export cycle=${fcycle}
              ${MET_HOME}/scripts/plot_grid2grid.sh 1>${DATA_OUT}/log/plot_grid2grid_c${cycle}.out 2>&1 &
              if [ $sfc = yes ] ; then ${MET_HOME}/scripts/plot_grid2grid_sfc.sh 1>${DATA_OUT}/log/plot_grid2grid_sfc_c${cycle}.out 2>&1 & ; fi
          done
       fi
   else
       if [ $plot = yes ] ; then
          for fcycle in $fcycle_list ; do
              export cycle=${fcycle}
              if [ $batch = yes] ; then
                 $SUBJOB -e $listvar,batch -a $ACCOUNT  -q "$CUE2RUN" -g $GROUP -p 1/1/N -r 2048/1 -t 6:00:00 -j compute_plot_grid2grid_c${cycle} -o ${DATA_OUT}/log/compute_plot_grid2grid_c${cycle}.out  ${MET_HOME}/scripts/compute_plot_grid2grid.sh
                  if [ $sfc = yes ] ; then $SUBJOB -e $listvar,batch -a $ACCOUNT  -q "$CUE2RUN" -g $GROUP -p 1/1/N -r 2048/1 -t 6:00:00 -j compute_plot_grid2grid_sfc_c${cycle} -o ${DATA_OUT}/log/compute_plot_grid2grid_sfc_c${cycle}.out  ${MET_HOME}/scripts/compute_plot_grid2grid_sfc.sh ; fi
              else
                 ${MET_HOME}/scripts/compute_plot_grid2grid.sh 1>${DATA_OUT}/log/compute_plot_grid2grid_c${cycle}.out 2>&1 &
                 if [ $sfc = yes ] ; then ${MET_HOME}/scripts/compute_plot_grid2grid_sfc.sh 1>${DATA_OUT}/log/compute_plot_grid2grid_sfc_c${cycle}.out 2>&1 & ; fi
              fi
          done
       else
          for fcycle in $fcycle_list ; do
              export cycle=${fcycle}
              if [ $batch = yes ] ; then
                  $SUBJOB -e $listvar -a $ACCOUNT  -q "$CUE2RUN" -g $GROUP -p 1/1/N -r 2048/1 -t 6:00:00 -j compute_grid2grid_pres_c${cycle} -o ${DATA_OUT}/log/compute_grid2grid_pres_c${cycle}.out  ${MET_HOME}/scripts/compute_grid2grid_pres.sh
                  $SUBJOB -e $listvar -a $ACCOUNT  -q "$CUE2RUN" -g $GROUP -p 1/1/N -r 2048/1 -t 6:00:00 -j compute_grid2grid_anom_c${cycle} -o ${DATA_OUT}/log/compute_grid2grid_anom_c${cycle}.out  ${MET_HOME}/scripts/compute_grid2grid_anom.sh
                  if [ $sfc = yes ] ; then $SUBJOB -e $listvar -a $ACCOUNT  -q "$CUE2RUN" -g $GROUP -p 1/1/N -r 2048/1 -t 6:00:00 -j compute_grid2grid_sfc_c${cycle} -o ${DATA_OUT}/log/compute_grid2grid_sfc_c${cycle}.out  ${MET_HOME}/scripts/compute_grid2grid_sfc.sh ; fi
              else
                  ${MET_HOME}/scripts/compute_grid2grid_pres.sh 1>${DATA_OUT}/log/compute_grid2grid_pres_c${cycle}.out 2>&1 & 
                  ${MET_HOME}/scripts/compute_grid2grid_anom.sh 1>${DATA_OUT}/log/compute_grid2grid_anom_c${cycle}.out 2>&1 &
                  if [ $sfc = yes ] ; then ${MET_HOME}/scripts/compute_grid2grid_sfc.sh 1>${DATA_OUT}/log/compute_grid2grid_sfc_c${cycle}.out 2>&1 & ; fi
              fi
          done
       fi
   fi  
fi
############################
if [ $precip = YES ] ; then
   compute=yes #calculate contingency table counts
   plot=no #plot statistics from contingency tavle
   export contable_dir="/global/noscrub/Mallory.Row/archive/precip" #where to save/access continegency table data from MET; unset(comment out) leaves in appropriate DATA_OUTmain folder
   #file characteristics ; file format /${model}/${file_type}${fhr}${dump}${yyyymmdd}${cyc}
   export start_date="20170806" #year month date
   export end_date="20170807" #year month date
   export fcycle_list="00 12" #forecast cycles/hours to be verified at, 00Z or 12Z only
   export file_type_lists="pgbf pgbf pgbf" #ex. flxf or pgbf
   export model_var="APCP" #either APCP or PRATE (to add in future)
   export grid="G211"   #NCEP grid to convert to
   #define forecast ranges valid 12Z to 12Z (forecast hours for 12Z = forecast hours +12 for 00Z), 12Z: [fstart_r1,fend_r2,24] 00Z: [fstart_r1+12, fend_r2+12, 24]
   export fstart_r1="0"  #forecast hour to start at, start of first 24 hour range, based on 12Z-12Z
   export fend_r2="168"   #forecast hour to end at, end of last 24 hour range, based on 12Z-12Z
   #which regions to compute stats over
   export regions_list="CONUS EAST WEST" #regions to generate stats for besides full grid; needs .nc in $MET_HOME/poly
   #thresholds to compute stats for (>= #)
   export threshold_list="0.2 2 5 10 15 25 35 50 75" #in mm
   #obs file (valid at yyyymm(dd-1)12z-yyyymmdd12Z) format: ${precip_obs_dir}/${precip_obs_file_prefix}${validdate(yyyymmdd)}${precip_obs_file_suffix}, variable APCP
   export obs_name="CCPA"
   export precip_obs_dir="/ensemble2/noscrub/Yan.Luo/daily_1deg_ccpa"
   export precip_obs_file_prefix="ccpa_conus_1.0d_" #leave blank if none
   export precip_obs_file_suffix="" #leave blank if none
   #etc
   export plot_stats_list="bias ets" #stats to plot
   export verbose="1" #verbosity of MET output; 1-5
   export nexp=`echo $model_fcst_list |wc -w`
   export nreg=`echo $regions_list |wc -w`
   export nthrs=`echo $threshold_list |wc -w`
   #create precip output directories
   set -a;. ${MET_HOME}/scripts/mkdir_precip.sh
   #submit scripts
   if [ $compute = no ] ; then
       if [ $plot = yes ] ; then
          for fcycle in $fcycle_list ; do
              export cycle=${fcycle}
               ${MET_HOME}/scripts/plot_precip.sh 1>${DATA_OUT}/log/plot_precip_c${cycle}.out 2>&1 &
          done
       fi
   else
       if [ $plot = yes ] ; then
          for fcycle in $fcycle_list ; do
              export cycle=${fcycle}
              ${MET_HOME}/scripts/compute_plot_precip.sh 1>${DATA_OUT}/log/compute_precip_c${cycle}.out 2>&1 &
          done
       else
          for fcycle in $fcycle_list ; do
              export cycle=${fcycle}
              ${MET_HOME}/scripts/compute_precip.sh 1>${DATA_OUT}/log/compute_precip_c${cycle}.out 2>&1 &
          done
       fi
   fi
fi
############################
if [ $grid2obs = YES ] ; then
   compute=no
   plot=yes
   export batch=no #submit jobs in batch or not
   export grid2obs_dir="/global/noscrub/Mallory.Row/archive/grid2obs"
   #file characteristics ; file format /${model}/pgbf${fhr}${dump}${yyyymmddcc}
   export start_date="20170701" #year month date
   export end_date="20170731" #year month date
   export fcycle_list="00" #forecast cycles/hours to be verified at, two digit format 
   export fstart="0"  #forecast hour to start at
   export fend="168"   #forecast hour to end at
   export fint_upper_air="12"
   export fint_conus_sfc="12"
   export upper_air_grid="G3" #NCEP grid to convert to
   export conus_sfc_grid="G3" #NCEP grid to convert to
   export prepbufr_dir="/global/noscrub/Fanglin.Yang/prepbufr"  #directory where prepbufr data are save 
   #which regions to compute stats over
   export upper_air_regions_list="G236" #regions to generate stats for besides full upper_air_grid; needs .nc mask
   export conus_sfc_regions_list="EAST" #regions to generate stats for besides full conus_sfc_grid; needs .poly mask in $MET_HOME/poly
   #export upper_air_regions_list="G236 GEUR GASI GAFR GAUS GNA GSA GNH GSH GTRP" #regions to generate stats for besides full upper_air_grid; needs .nc mask
   #export conus_sfc_regions_list="CONUS EAST WEST NWC SWC NMT SMT GRB SWD NPL SPL MDW LMV GMC NEC SEC APL WCA ECA ATC NAK SAK NPO MEX" #regions to generate stats for besides full conus_sfc_grid; needs .poly mask in $MET_HOME/poly
   #etc
   export plot_stats_list="bias rms" #stats to plot, options:bias rms
   export verbose="1" #verbosity of MET output; 1-5
   export nexp=`echo $model_fcst_list |wc -w`
   export nuareg=`echo $upper_air_regions_list |wc -w`
   export ncsfcreg=`echo $conus_sfc_regions_list |wc -w`
   #create grid2obs output directories
   set -a;. ${MET_HOME}/scripts/mkdir_grid2obs.sh
   #gather lists of variables
   export listvar1=MET_HOME,ndate
   export listvar2=model_fcst_list,DATA_IN_model_fcst_list,model_fcst_dump_list,DATA_OUTmain,grid2obs_dir,start_date,end_date,fstart,fend,fint_upper_air,fint_conus_sfc,upper_air_grid,conus_sfc_grid,prepbufr_dir,upper_air_regions_list,conus_sfc_regions_list,plot_stats_list,verbose,nexp,nuareg,ncsfcreg,cycle
   export listvar3=DATA_OUT,DATA_OUTmodel,DATA_OUTimgs,DATA_OUTlog
   export listvar="$listvar1,$listvar2,$listvar3"
   #submit scripts
   if [ $compute = no ] ; then
       if [ $plot = yes ] ; then
          for fcycle in $fcycle_list ; do
              export cycle=${fcycle}
               ${MET_HOME}/scripts/plot_grid2obs.sh 1>${DATA_OUT}/log/plot_grid2obs_c${cycle}.out 2>&1 &
          done
       fi
   else
       if [ $plot = yes ] ; then
          for fcycle in $fcycle_list ; do
              export cycle=${fcycle}
              if [ $batch = yes ] ; then
                 $SUBJOB -e $listvar,batch -a $ACCOUNT  -q "$CUE2RUN" -g $GROUP -p 1/1/N -r 2048/1 -t 6:00:00 -j compute_plot_grid2obs_upper_air_c${cycle} -o ${DATA_OUT}/log/compute_plot_grid2obs_upper_air_c${cycle}.out  ${MET_HOME}/scripts/compute_plot_grid2obs_upper_air.sh
                 $SUBJOB -e $listvar,batch -a $ACCOUNT  -q "$CUE2RUN" -g $GROUP -p 1/1/N -r 2048/1 -t 6:00:00 -j compute_plot_grid2obs_conurs_sfc_c${cycle} -o ${DATA_OUT}/log/compute_plot_grid2obs_conus_sfc_c${cycle}.out  ${MET_HOME}/scripts/compute_plot_grid2obs_conus_sfc.sh
              else
                 ${MET_HOME}/scripts/compute_plot_grid2obs_upper_air.sh 1>${DATA_OUT}/log/compute_plot_grid2obs_upper_air_c${cycle}.out 2>&1 &
                 ${MET_HOME}/scripts/compute_plot_grid2obs_conus_sfc.sh 1>${DATA_OUT}/log/compute_plot_grid2obs_conus_sfc_c${cycle}.out 2>&1 &
              fi
          done
       else
          if [ $batch = yes ] ; then
             $SUBJOB -e $listvar -a $ACCOUNT  -q "$CUE2RUN" -g $GROUP -p 1/1/N -r 2048/1 -t 6:00:00 -j compute_grid2obs_upper_air_c${cycle} -o ${DATA_OUT}/log/compute_grid2obs_upper_air_c${cycle}.out  ${MET_HOME}/scripts/compute_grid2obs_upper_air.sh
             $SUBJOB -e $listvar -a $ACCOUNT  -q "$CUE2RUN" -g $GROUP -p 1/1/N -r 2048/1 -t 6:00:00 -j compute_grid2obs_conurs_sfc_c${cycle} -o ${DATA_OUT}/log/compute_grid2obs_conus_sfc_c${cycle}.out  ${MET_HOME}/scripts/compute_grid2obs_conus_sfc.sh
          else
             ${MET_HOME}/scripts/compute_grid2obs_upper_air.sh 1>${DATA_OUT}/log/compute_grid2obs_upper_air_c${cycle}.out 2>&1 &
             ${MET_HOME}/scripts/compute_grid2obs_conus_sfc.sh 1>${DATA_OUT}/log/compute_grid2obs_conus_sfc_c${cycle}.out 2>&1 &
          fi
       fi
   fi
fi
############################
if [ $plots2d = YES ] ; then
   #file characteristics ; file format /${model}/pgbf${fhr}${dump}${yyyymmddcc}
   export start_date="20170101" #year month date
   export end_date="20170105" #year month date
   export fcycle_list="00 06 12 18" #forecast cycles/hours to be verified at, two digit format
   export fday_list="d01" #forecast days to verify, either analysis (anl) or number for forecast day (dXX)
   export grid="G2" #NCEP grid to convert to
   #observations
   export obs_dir="/global/save/Mallory.Row/data/obdata_CFcomp"
   export climo="yes" #use climatology (yes) or monthly means (no, valid 3/2000-2/2017) of observations
   #etc
   export verbose="2" #verbosity of MET output; 1-5
   export nexp=`echo $model_fcst_list |wc -w`
   #create 2dplots output directories
   set -a;. ${MET_HOME}/scripts/mkdir_plots2d.sh
   #submit scripts
   for fcycle in $fcycle_list ; do
     export cycle=${fcycle}
     for fday in ${fday_list} ; do
        export fday=${fday}
        ${MET_HOME}/scripts/plots2d_model2obs.sh 1>${DATA_OUT_model2obs}/log/plots2d_model2obs_c${cycle}_${fday}.out 2>&1 &
        ${MET_HOME}/scripts/plots2d_model2model.sh 1>${DATA_OUT_model2model}/log/plots2d_model2model_c${cycle}_${fday}.out 2>&1 &
     done
   done
fi
############################
exit
