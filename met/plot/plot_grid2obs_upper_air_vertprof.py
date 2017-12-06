#############################################################################
##### Import python modules
import os
import numpy as np
import netCDF4 as netcdf
import numpy as np
import datetime as datetime
import calendar as cal
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.gridspec as gridspec
from mpl_toolkits.basemap import Basemap, addcyclic
import plot_defs as pd
import warnings
##### Settings
np.set_printoptions(suppress=True)
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['axes.labelsize'] = 15
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 15
plt.rcParams['ytick.labelsize'] = 15
plt.rcParams['axes.titlesize'] = 15
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.formatter.useoffset'] = False
warnings.filterwarnings('ignore')
#############################################################################
##### Read in data and set variables
#forecast dates
month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
sdate = os.environ['start_date']
syear = int(sdate[:4])
smon = int(sdate[4:6])
smonth = month_name[smon-1]
sday = int(sdate[6:8])
edate=os.environ['end_date']
eyear = int(edate[:4])
emon = int(edate[4:6])
emonth = month_name[emon-1]
eday = int(edate[6:8])
fcsthr_in = int(os.environ['fcsthr'])
fcstday = fcsthr_in/24
sd = datetime.datetime(syear, smon, sday)
ed = datetime.datetime(eyear, emon, eday)+datetime.timedelta(days=1)
tdelta = datetime.timedelta(days=1)
dates = md.drange(sd, ed, tdelta)
#model info
model_fcst = os.environ['modellist'].split(' ')
cyc = os.environ['cycle']
nexp = int(os.environ['nexp'])
grid = os.environ['upper_air_grid']
reg = os.environ['reg']
DATA_OUTmodel = os.environ['DATA_OUTmodel']
#output info
DATA_OUTimgs_now = os.environ['DATA_OUTimgs_now']
plot_stats = os.environ['stats'].split(' ')
nstats = int(os.environ['nstats'])
varname = os.environ['varname']
varlevellist = os.environ['varlevellist'].split(' ')
nlev = int(os.environ['nlev'])
#remove 'P' prior to pressure level
var_level = np.empty(len(varlevellist), dtype=int)
for v in range(len(varlevellist)):
    varlevellist_now = varlevellist[v]
    var_level[v] = varlevellist_now[1:]
#etc
colors = ['k','g', 'r', 'b', 'darkorange', 'darkorchid', 'palevioletred', 'dodgerblue', 'dimgrey']
#############################################################################
##### Read data in data, compute statistics, and plot
#read in data
s=1
while s <= nstats: #loop over statistics
   stat_now_name = plot_stats[s-1]
   models_tp_stat_array = np.empty([nexp, len(dates), len(var_level)])
   models_dates_array = np.empty([nexp, len(dates)])
   print '--- '+str(stat_now_name)
   vertprof_model_means = np.empty([nexp,nlev])
   n=1
   while n <= nexp: #loop over experiments
      print n, model_fcst[n-1]
      #get file name
      if fcsthr_in < 10:
         fcsthr = '0'+str(fcsthr_in)
      else:
         fcsthr = str(fcsthr_in)
      v=1 
      while v <= nlev:
           varlevel = varlevellist[v-1]
           grid2obs_file = str(DATA_OUTmodel)+'/'+str(model_fcst[n-1])+'/upper_air/'+str(cyc)+'Z/'+str(reg)+'/grid2obs_f'+str(fcsthr)+'_'+str(varname)+str(varlevel)+'.txt'
           #get number of rows
           nrow = sum(1 for line in open(grid2obs_file))
           #get number of columns
           with file(grid2obs_file) as f:
              line_header = f.readline()
              line = f.readline()
              ncol = len(line.split())
           if nrow == 0: #file blank if stat analysis filters were not all met
              stat_now = np.ones_like(dates)*np.nan
              modeldates=dates
              models_dates_array[n-1,:] = modeldates
              vertprof_model_means[n-1,v-1] = np.mean(stat_now)
           else:
              #read data file and put in array
              data = list()
              l = 0
              with open(grid2obs_file) as f:
                 for line in f:
                   if l != 0:
                     line_split = line.split()
                     data.append(line_split)
                   l+=1
              data_array = np.asarray(data)
              #get existing model date files
              dates_list = []
              valid_dates = data_array[:,4]
              dateformat = "%Y%m%d_%H%M%S"
              for d in range(len(valid_dates)):
                  modeldate = datetime.datetime.strptime(valid_dates[d], dateformat)
                  dates_list.append(int(md.date2num(modeldate)))
              modeldates = np.asarray(dates_list)
              #parse between sl1l2 and vl1l2 data
              parsum = data_array[:,23:].astype(float)
              if varname == 'UGRD_VGRD':
                   ufbar = parsum[:,0]
                   vfbar = parsum[:,1] 
                   uobar = parsum[:,2]
                   vobar = parsum[:,3]
                   uvfobar = parsum[:,4]
                   uvffbar = parsum[:,5]
                   uvoobar = parsum[:,6]
                   if stat_now_name == 'bias':
                      stat_now = np.ma.masked_invalid(np.sqrt(uvffbar) - np.sqrt(uvoobar))
                   if stat_now_name == 'rms':
                      stat_now = np.ma.masked_invalid(np.sqrt(uvffbar + uvoobar - (2*uvfobar)))
                   vertprof_model_means[n,v] = np.mean(stat_now)
              else:
                   fbar = parsum[:,0]
                   obar = parsum[:,1]
                   fobar = parsum[:,2]
                   ffbar = parsum[:,3]
                   oobar = parsum[:,4]
                   if stat_now_name == 'bias':
                      stat_now = np.ma.masked_invalid(fbar - obar)
                   if stat_now_name == 'rms':
                      stat_now = np.ma.masked_invalid(np.sqrt(ffbar + oobar - (2*fobar)))
                   vertprof_model_means[n-1,v-1] = np.mean(stat_now)
           v+=1
           if n == 1:
              fig, ax = plt.subplots(1,1,figsize=(10,12))
              ax.plot(np.zeros_like(vertprof_model_means[n-1,:]), var_level, color='silver', ls='-', linewidth=2.0)
              ax.plot(vertprof_model_means[n-1,:], var_level, color=colors[n-1], ls='-', linewidth=2.0, marker='o', markersize=7, label=model_fcst[n-1])
              ax.grid(True)
              ax.set_xlabel(str(stat_now_name))
              ax.set_ylabel('Pressure Level')
              ax.set_yscale("log")
              ax.set_yticks(var_level)
              ax.set_yticklabels(var_level)
              ax.set_ylim([var_level[0],var_level[-1]])
              ax.tick_params(axis='x', pad=10)
              ax.tick_params(axis='y', pad=15)
              if reg == 'FULL':
                 ax.set_title(str(varname)+' '+str(varlevel)+': '+str(stat_now_name)+'\n'+str(grid)+' initialized '+str(cyc)+'Z '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' f'+str(fcsthr)+'\n\n', fontsize=14, fontweight='bold')
              else:
                 ax.set_title(str(varname)+' '+str(varlevel)+': '+str(stat_now_name)+'\n'+str(grid)+':'+str(reg)+' initialized '+str(cyc)+'Z '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' f'+str(fcsthr)+'\n\n', fontsize=14, fontweight='bold')
           else:
               ax.plot(vertprof_model_means[n-1,:], var_level,  color=colors[n-1],  ls='--', marker='o', markersize=7, label=model_fcst[n-1])
           if n == nexp:
               plt.legend(bbox_to_anchor=(0.025, 1.01, 0.95, .102), loc=3, ncol=nexp, fontsize='13', mode="expand", borderaxespad=0.)
               #if reg == 'FULL':
               #   if fcsthr_in % 24 == 0:
               #      plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_day'+str(fcstday)+'_'+str(varname)+'_'+str(grid)+'_vp.png', bbox_inches='tight')
               #   else:
               #      plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_f'+str(fcsthr)+'_'+str(varname)+'_'+str(grid)+'_vp.png', bbox_inches='tight')
               #else:
               #   if fcsthr_in % 24 == 0:
               #      plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_day'+str(fcstday)+'_'+str(varname)+'_'+str(grid)+str(reg)+'_vp.png', bbox_inches='tight')
               #   else:
               #      plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_f'+str(fcsthr)+'_'+str(varname)+'_'+str(grid)+str(reg)+'_vp.png', bbox_inches='tight')
               if reg == 'FULL':
                  plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_f'+str(fcsthr)+'_'+str(varname)+'_'+str(grid)+'_vp.png', bbox_inches='tight')
               else:
                  plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_f'+str(fcsthr)+'_'+str(varname)+'_'+str(grid)+str(reg)+'_vp.png', bbox_inches='tight') 

      n+=1
   s+=1
