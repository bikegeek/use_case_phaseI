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
#import matplotlib.dates as md
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
#model info
model_fcst = os.environ['modellist'].split(' ')
cyc = os.environ['cycle']
fstart = int(os.environ['fstart'])
fend = int(os.environ['fend'])
fint = int(os.environ['fint'])
nexp = int(os.environ['nexp'])
grid = os.environ['grid']
reg = os.environ['reg']
DATA_OUTmodel = os.environ['DATA_OUTmodel']
parsum_dir_lookin = os.environ['parsum_dir_lookin']
#output info
DATA_OUTimgs_now = os.environ['DATA_OUTimgs_now']
varname = os.environ['varname']
varlevel = os.environ['varlevel']
#etc
colors = ['k', 'g', 'r', 'b', 'darkorange', 'darkorchid', 'palevioletred', 'dodgerblue', 'dimgrey']
#############################################################################
##### Read data in data, compute statistics, and plot
#read in data
n=1
while n <= nexp: #loop over experiments
   #get file name
   sfc_mean_file = str(DATA_OUTmodel)+'/'+str(model_fcst[n-1])+'/sfc/'+str(cyc)+'Z/'+str(reg)+'/fbar_mean_'+str(varname)+str(varlevel)+'.txt'
   #get number of rows
   nrow = sum(1 for line in open(sfc_mean_file))
   #get number of columns
   with file(sfc_mean_file) as f:
      line_header = f.readline()
      line = f.readline()
      ncol = len(line.split())
   #read data file and put in array
   data = list()
   with open(sfc_mean_file) as f:
      for line in f:
          line_split = line.split()
          data.append(line_split)
   data_array = np.asarray(data)
   #assign variables
   frcst_hr = data_array[:,0].astype(float)
   stat_now_mean = data_array[:,1]
   for x in range(len(stat_now_mean)):
       if stat_now_mean[x] == '--':
          stat_now_mean[x] = np.nan
   stat_now_mean = stat_now_mean.astype(float)
   count_nan = np.count_nonzero(np.isnan(stat_now_mean))
   stat_now_name = 'fbar'
   #plot individual statistic forecast hour mean time seres
   if n == 1:
         fig, (ax1, ax2) = plt.subplots(2,1,figsize=(10,10), sharex=True)
         #forecast hour mean
         if count_nan != len(stat_now_mean):
            print n, model_fcst[n-1]
            ax1.plot(frcst_hr,stat_now_mean, color=colors[n-1], ls='-', linewidth=2.0, marker='o', markersize=7, label=model_fcst[n-1])
         stat_exp1 = stat_now_mean
         ax1.grid(True)
         ax1.set_xticks(np.arange(fstart,fend+fint,fint))
         ax1.set_xlim([fstart,fend])
         ax1.tick_params(axis='y', pad=15)
         if reg == 'FULL':
            ax1.set_title(str(varname)+' '+str(varlevel)+': '+str(stat_now_name)+'\n'+str(grid)+' valid '+str(cyc)+'Z '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' Mean\n\n', fontsize=14, fontweight='bold')
         else:
            ax1.set_title(str(varname)+' '+str(varlevel)+': '+str(stat_now_name)+'\n'+str(grid)+':'+str(reg)+' valid '+str(cyc)+'Z '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' Mean\n\n', fontsize=14, fontweight='bold')
         #difference
         ax2.plot(frcst_hr, np.zeros_like(frcst_hr), color='k')
         ax2.text(0.01, 0.9, 'Differences outside the outline bars are\n significant at the 95% confidence interval', fontsize=11, bbox={'facecolor':'white', 'alpha':0, 'pad':5}, transform=ax2.transAxes)
         ax2.set_xticks(np.arange(fstart,fend+fint,fint))
         ax2.set_xlim([fstart,fend])
         ax2.set_xlabel('Forecast Hour')
         ax2.tick_params(axis='x', pad=10)
         ax2.tick_params(axis='y', pad=15)
         ax2.set_title('Difference with Respect to '+str(model_fcst[0]))
         ax2.grid(True)
   else:
         if count_nan != len(stat_now_mean):
            print n, model_fcst[n-1]
            #forecast hour mean
            ax1.plot(frcst_hr,stat_now_mean, color=colors[n-1], ls='-', marker='o', markersize=7, label=model_fcst[n-1])
            #differnce
            ax2.plot(frcst_hr, stat_now_mean - stat_exp1, color=colors[n-1], ls='-', marker='o', markersize=7, label=model_fcst[n-1])
   if n == nexp:
      plt.legend(bbox_to_anchor=(0.0, 1.02, 1.0, .102), loc=3, ncol=nexp, fontsize='13', mode="expand", borderaxespad=0.)
      if reg == 'FULL':
           plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_fhrmeans_'+str(varname)+'_'+str(varlevel)+'_'+str(grid)+'.png', bbox_inches='tight')
      else:
           plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_fhrmeans_'+str(varname)+'_'+str(varlevel)+'_'+str(grid)+str(reg)+'.png', bbox_inches='tight')
   n+=1
