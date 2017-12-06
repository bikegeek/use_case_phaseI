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
fcsthr_e = int(os.environ['fend'])
fcsthr_s = int(os.environ['fstart'])
fcsthrs = np.arange(fcsthr_s,fcsthr_e+24,24)
#model info
model_fcst = os.environ['modellist'].split(' ')
cyc = os.environ['cycle']
nexp = int(os.environ['nexp'])
grid = os.environ['grid']
reg = os.environ['reg']
DATA_OUTmodel = os.environ['DATA_OUTmodel']
contable_dir_lookin = os.environ['contable_dir_lookin']
#output info
DATA_OUTimgs_now = os.environ['DATA_OUTimgs_now']
plot_stats = os.environ['stats'].split(' ')
nstats = int(os.environ['nstats'])
thrs_levels = os.environ['thrs_levels'].split(' ')
varname = os.environ['varname']
#############################################################################
##### Read data in data, compute statistics, and plot
#read in data
#ets and bias threshold forecast hour mean
models_stat_array = np.empty([nexp, len(thrs_levels), len(fcsthrs)])
s=1
while s <= nstats: #loop over statistics
   stat_now_name = plot_stats[s-1]
   print '--- '+str(stat_now_name)
   n=1
   while n <= nexp: #loop over experiments
      print n, model_fcst[n-1]
      fcsthr_in = fcsthr_s
      ff = 0
      while fcsthr_in <= fcsthr_e: 
         #get file name
         if fcsthr_in < 10:
            precip_mean_file = str(DATA_OUTmodel)+'/'+str(model_fcst[n-1])+'/'+str(cyc)+'Z/'+str(reg)+'/'+str(stat_now_name)+'_mean_f0'+str(fcsthr_in)+'.txt'
         else:
            precip_mean_file = str(DATA_OUTmodel)+'/'+str(model_fcst[n-1])+'/'+str(cyc)+'Z/'+str(reg)+'/'+str(stat_now_name)+'_mean_f'+str(fcsthr_in)+'.txt' 
         #get number of rows
         nrow = sum(1 for line in open(precip_mean_file))
         #get number of columns
         with file(precip_mean_file) as f:
            line_header = f.readline()
            line = f.readline()
            ncol = len(line.split())
         data = list()
         with open(precip_mean_file) as f:
            for line in f:
               line_split = line.split()
               data.append(line_split)
         data_array = np.asarray(data)
         #set variables
         thrs = data_array[:,0].astype(float)
         thrs_mean = data_array[:,1]
         for x in range(len(thrs_mean)):
             if thrs_mean[x] == '--':
                thrs_mean[x] = np.nan
         thrs_mean = thrs_mean.astype(float)
         models_stat_array[n-1,:,ff] = thrs_mean
         ff+=1
         fcsthr_in+=24
      n+=1
   thrs_ticks = np.arange(0,len(thrs),1)
   yy,xx = np.meshgrid(fcsthrs, thrs_ticks)
   a = 1
   if nexp == 1:
      fig = plt.figure(figsize=(10,12))
      gs = gridspec.GridSpec(2,1)
      gs.update(wspace=0.1, hspace=0.1)
   elif nexp == 2:
      fig = plt.figure(figsize=(10,12))
      gs = gridspec.GridSpec(2,1)
      gs.update(wspace=0.1, hspace=0.2)
   elif nexp > 2 and nexp <= 4:
      fig = plt.figure(figsize=(15,12))
      gs = gridspec.GridSpec(2,2)
      gs.update(wspace=0.3, hspace=0.25)
   elif nexp > 4 and nexp <= 6:
      fig = plt.figure(figsize=(18,12))
      gs = gridspec.GridSpec(2,3)
      gs.update(wspace=0.3, hspace=0.25)
   elif nexp > 6:
      fig = plt.figure(figsize=(21,17))
      gs = gridspec.GridSpec(3,3)
      gs.update(wspace=0.35, hspace=0.25)
   while a <= nexp:
       ax = plt.subplot(gs[a-1])
       if a == 1:
          C0 = ax.contourf(xx, yy, models_stat_array[a-1,:,:], cmap=plt.cm.GnBu, extend='both')
          C = ax.contour(xx, yy, models_stat_array[a-1,:,:], levels=C0.levels, colors='k', linewidths=1.0)
          ax.clabel(C,C0.levels, fmt='%1.2f', inline=True, fontsize=12.5)
          ax.set_title(str(model_fcst[a-1]), loc='left')
       elif a == 2:
            if stat_now_name == 'bias':
               C1 = ax.contourf(xx, yy, models_stat_array[a-1,:,:], levels=C0.levels, cmap=plt.cm.GnBu, extend='both')
               C = ax.contour(xx, yy, models_stat_array[a-1,:,:], levels=C0.levels, colors='k', linewidths=1.0)
               ax.clabel(C,C0.levels, fmt='%1.2f', inline=True, fontsize=12.5)
               ax.set_title(str(model_fcst[a-1]), loc='left')
            else:
               C1 = ax.contourf(xx, yy, models_stat_array[a-1,:,:]-models_stat_array[0,:,:], cmap=plt.cm.coolwarm, extend='both')
               C = ax.contour(xx, yy, models_stat_array[a-1,:,:]-models_stat_array[0,:,:], levels=C1.levels, colors='k', linewidths=1.0)
               ax.clabel(C,C1.levels, fmt='%1.2f', inline=True, fontsize=12.5)
               ax.set_title(str(model_fcst[a-1])+'-'+str(model_fcst[0]), loc='left')
       elif a > 2:
            if stat_now_name == 'bias':
               ax.contourf(xx, yy, models_stat_array[a-1,:,:], levels=C0.levels, cmap=plt.cm.GnBu, extend='both')
               C = ax.contour(xx, yy, models_stat_array[a-1,:,:], levels=C0.levels, colors='k', linewidths=1.0)
               ax.clabel(C,C0.levels, fmt='%1.2f', inline=True, fontsize=12.5)
               ax.set_title(str(model_fcst[a-1]), loc='left')
            else:
               ax.contourf(xx, yy, models_stat_array[a-1,:,:]-models_stat_array[0,:,:], levels=C1.levels, cmap=plt.cm.coolwarm, extend='both')
               C = ax.contour(xx, yy, models_stat_array[a-1,:,:]-models_stat_array[0,:,:], levels=C1.levels, colors='k', linewidths=1.0)
               ax.clabel(C,C1.levels, fmt='%1.2f', inline=True, fontsize=12.5)
               ax.set_title(str(model_fcst[a-1])+'-'+str(model_fcst[0]), loc='left')
       ax.grid(True)
       ax.set_xlabel('Threshold')
       ax.set_xticklabels(thrs)
       ax.set_xlim([0,thrs_ticks[len(thrs_ticks)-1]])
       ax.set_ylabel('Forecast Hours')
       ax.set_yticks(fcsthrs)
       ax.set_yticklabels(fcsthrs)
       ax.set_ylim([fcsthrs[0],fcsthrs[-1]])
       #ax.tick_params(axis='x', pad=10)
       #ax.tick_params(axis='y', pad=15)
       if a > 1 and a == nexp:
          cax = fig.add_axes([0.1, -0.05, 0.8, 0.05])
          fig.colorbar(C1, cax=cax, orientation='horizontal')
       a+=1
   if reg == 'FULL':
      fig.suptitle(str(varname)+': '+str(stat_now_name)+'\n'+str(grid)+' valid '+str(cyc)+'Z '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' Mean\n\n', fontsize=14, fontweight='bold')
      plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'mean_'+str(cyc)+'Z.png', bbox_inches='tight')
   else:
      fig.suptitle(str(varname)+': '+str(stat_now_name)+'\n'+str(grid)+':'+str(reg)+' valid '+str(cyc)+'Z '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' Mean\n\n', fontsize=14, fontweight='bold')
      plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'mean_'+str(cyc)+'Z.png', bbox_inches='tight')
   s+=1  
