#!/bin/ksh
if [ $machine = WCOSS ]; then
   export ACCOUNT=GFS-T2O                                ;#computer ACCOUNT task
   export CUE2RUN=dev                                    ;#dev or dev_shared         
   export CUE2FTP=transfer                               ;#queue for data transfer
   export GROUP=g01                                      ;#group of account, g01 etc
   export MET_HOME="/global/save/Mallory.Row/VRFY/met"
   export ndate="${MET_HOME}/nwprod/util/exec/ndate"
   export copygb="/nwprod/util/exec/copygb"
   export SUBJOB=${MET_HOME}/bin/sub_wcoss                   ;#script for submitting batch jobs
   export FC=/usrx/local/intel/composer_xe_2011_sp1.11.339/bin/intel64/ifort    ;#intel compiler
   export FFLAG="-O2 -convert big_endian -FR"                 ;#intel compiler options
   export APRUN=""                                            ;#affix to run batch jobs
   export STMP=/stmpd2                                        ;#temporary directory                          
   export PTMP=/ptmpd2                                        ;#temporary directory  
#----------------------------
elif [ $machine = WCOSS_C ]; then
   export ACCOUNT=GFS-T2O                                ;#computer ACCOUNT task
   export CUE2RUN=dev                                    ;#dev or dev_shared         
   export CUE2FTP=dev_transfer                           ;#queue for data transfer
   export GROUP=g01                                      ;#group of account, g01 etc
   export MET_HOME="/gpfs/hps/emc/global/noscrub/Mallory.Row/VRFY/met"
   export ndate="${MET_HOME}/nwprod/util/exec/ndate"
   export copygb="${MET_HOME}/nwprod/util/exec/copygb"
   export SUBJOB=${MET_HOME}/bin/sub_wcoss_c                   ;#script for submitting batch jobs
   export FC=/opt/intel/composer_xe_2015.3.187/bin/intel64/ifort    ;#intel compiler
   export FFLAG="-O2 -convert big_endian -FR"                 ;#intel compiler options
   export APRUN="aprun -n 1 -N 1 -j 1 -d 1"                   ;#affix to run batch jobs
   export STMP=/gpfs/hps/stmp                                 ;#temporary directory                          
   export PTMP=/gpfs/hps/ptmp                                 ;#temporary directory 
#----------------------------
elif [ $machine = THEIA ]; then
   export ACCOUNT=glbss                                  ;#computer ACCOUNT task
   export CUE2RUN=batch                                  ;#default to batch queue
   export CUE2FTP=service                                ;#queue for data transfer
   export GROUP=g01                                      ;#group of account, g01 etc
   export MET_HOME="/scratch4/NCEPDEV/global/save/Mallory.Row/VRFY/met"
   export ndate="${MET_HOME}/nwprod/util/exec/ndate"
   export copygb="${MET_HOME}/nwprod/util/exec/copygb"
   export SUBJOB=${MET_HOME}/bin/sub_theia                   ;#script for submitting batch jobs
   export FC=/apps/intel/composer_xe_2013_sp1.2.144/bin/intel64/ifort              ;#intel compiler
   export FFLAG="-O2 -convert big_endian -FR"                 ;#intel compiler options
   export APRUN=""                                            ;#affix to run batch jobs
   export STMP=/scratch4/NCEPDEV/stmp3                        ;#temporary directory                          
   export PTMP=/scratch4/NCEPDEV/stmp3                        ;#temporary directory
#----------------------------
else
 echo "machine $machine is not supportted by NCEP/ECM"
 exit 
fi
