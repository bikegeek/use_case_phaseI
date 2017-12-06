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
from matplotlib.colors import Normalize
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
fcsthrs = np.arange(fstart,fend+fint,fint)
nexp = int(os.environ['nexp'])
grid = os.environ['grid']
reg = os.environ['reg']
DATA_OUTmodel = os.environ['DATA_OUTmodel']
parsum_dir_lookin = os.environ['parsum_dir_lookin']
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
#############################################################################
##### Read data in data, compute statistics, and plot
#read in data
s=1
while s <= nstats: #loop over statistics
   stat_now_name = plot_stats[s-1]
   if stat_now_name == 'ac':
      s+=1
   else:
      print '--- '+str(stat_now_name)
      models_tp_stat_array = np.empty([nexp, len(fcsthrs), len(var_level)])
      n=1
      while n <= nexp: #loop over experiments
         print n, model_fcst[n-1]
         v = 1
         while v <= nlev:
               varlevel = varlevellist[v-1]
               #get file name
               pres_mean_file = str(DATA_OUTmodel)+'/'+str(model_fcst[n-1])+'/pres/'+str(cyc)+'Z/'+str(reg)+'/'+str(stat_now_name)+'_mean_'+str(varname)+str(varlevel)+'.txt'
               #get number of rows
               nrow = sum(1 for line in open(pres_mean_file))
               #get number of columns
               with file(pres_mean_file) as f:
                    line_header = f.readline()
                    line = f.readline()
                    ncol = len(line.split())
               #read data file and put in array
               data = list()
               with open(pres_mean_file) as f:
                  for line in f:
                     line_split = line.split()
                     data.append(line_split)
               data_array = np.asarray(data)
               #assign variables
               frcst_hr = data_array[:,0].astype(int)
               stat_now_mean = data_array[:,1]
               for x in range(len(stat_now_mean)):
                  if stat_now_mean[x] == '--':
                     stat_now_mean[x] = np.nan
               stat_now_mean = stat_now_mean.astype(float)
               models_tp_stat_array[n-1,:,v-1] = stat_now_mean
               v+=1
         n+=1
      yy,xx = np.meshgrid(var_level, frcst_hr)
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
         fig = plt.figure(figsize=(19,12))
         gs = gridspec.GridSpec(2,3)
         gs.update(wspace=0.3, hspace=0.25)
      elif nexp > 6:
         fig = plt.figure(figsize=(21,17))
         gs = gridspec.GridSpec(3,3)
         gs.update(wspace=0.35, hspace=0.25)
      while a <= nexp:
         ax = plt.subplot(gs[a-1])
         #ax.contourf(xxv, yyv, np.ones_like(xxv)*np.nan)
         if a == 1:
            if stat_now_name == 'bias':
               c0levels = pd.get_clevels(models_tp_stat_array[a-1,:,:])
               C0 = ax.contourf(xx, yy, models_tp_stat_array[a-1,:,:], levels=c0levels, cmap=plt.cm.RdYlGn_r, locator=matplotlib.ticker.MaxNLocator(symmetric=True), extend='both')
            else:
               C0 = ax.contourf(xx, yy, models_tp_stat_array[a-1,:,:], cmap=plt.cm.BuPu, extend='both')
            C = ax.contour(xx, yy, models_tp_stat_array[a-1,:,:], levels=C0.levels, colors='k', linewidths=1.0)
            ax.clabel(C,C0.levels, fmt='%1.2f', inline=True, fontsize=12.5)
            ax.set_title(str(model_fcst[a-1]), loc='left')
         elif a == 2:
            if stat_now_name == 'bias':
               C1 = ax.contourf(xx, yy, models_tp_stat_array[a-1,:,:], levels=C0.levels, cmap=plt.cm.RdYlGn_r, extend='both')
               C = ax.contour(xx, yy, models_tp_stat_array[a-1,:,:], levels=C0.levels, colors='k', linewidths=1.0)
               ax.clabel(C,C0.levels, fmt='%1.2f', inline=True, fontsize=12.5)
               ax.set_title(str(model_fcst[a-1]), loc='left')
            else:
               c1levels = pd.get_clevels(models_tp_stat_array[a-1,:,:]-models_tp_stat_array[0,:,:])
               C1 = ax.contourf(xx, yy, models_tp_stat_array[a-1,:,:]-models_tp_stat_array[0,:,:], levels=c1levels, cmap=plt.cm.coolwarm, locator=matplotlib.ticker.MaxNLocator(symmetric=True), extend='both')
               C = ax.contour(xx, yy, models_tp_stat_array[a-1,:,:]-models_tp_stat_array[0,:,:], levels=C1.levels, colors='k', linewidths=1.0)
               ax.clabel(C,C1.levels, fmt='%1.2f', inline=True, fontsize=12.5)
               ax.set_title(str(model_fcst[a-1])+'-'+str(model_fcst[0]), loc='left')
         elif a > 2:
            if stat_now_name == 'bias':
               C1 = ax.contourf(xx, yy, models_tp_stat_array[a-1,:,:], levels=C0.levels, cmap=plt.cm.RdYlGn_r, extend='both')
               C = ax.contour(xx, yy, models_tp_stat_array[a-1,:,:], levels=C0.levels, colors='k', linewidths=1.0)
               ax.clabel(C,C0.levels, fmt='%1.2f', inline=True, fontsize=12.5)
               ax.set_title(str(model_fcst[a-1]), loc='left')
            else:
               ax.contourf(xx, yy, models_tp_stat_array[a-1,:,:]-models_tp_stat_array[0,:,:], levels=C1.levels, cmap=plt.cm.coolwarm, extend='both')
               C = ax.contour(xx, yy, models_tp_stat_array[a-1,:,:]-models_tp_stat_array[0,:,:], levels=C1.levels, colors='k', linewidths=1.0)
               ax.clabel(C,C1.levels, fmt='%1.2f', inline=True, fontsize=12.5)
               ax.set_title(str(model_fcst[a-1])+'-'+str(model_fcst[0]), loc='left')
         ax.grid(True)
         ax.set_xlabel('Forecast Hour')
         ax.set_xticks(frcst_hr)
         ax.set_xticklabels(frcst_hr)
         ax.set_xlim([frcst_hr[0],frcst_hr[-1]])
         ax.set_ylabel('Pressure Level')
         ax.set_yscale("log")
         ax.set_yticks(var_level)
         ax.set_yticklabels(var_level)
         ax.set_ylim([var_level[0],var_level[-1]])
         if a > 1 and a == nexp:
            cax = fig.add_axes([0.1, -0.05, 0.8, 0.05])
            cbar = fig.colorbar(C1, cax=cax, orientation='horizontal')
            #cbar.set_ticklabels(C1.levels)
         a+=1
      if reg == 'FULL':
         fig.suptitle(str(varname)+': '+str(stat_now_name)+'\n'+str(grid)+' valid '+str(cyc)+'Z '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' Mean\n\n', fontsize=14, fontweight='bold')
         plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_fhrmeans_'+str(varname)+'_'+str(grid)+'_tp.png', bbox_inches='tight')
      else:
         fig.suptitle(str(varname)+': '+str(stat_now_name)+'\n'+str(grid)+':'+str(reg)+' valid '+str(cyc)+'Z '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' Mean\n\n', fontsize=14, fontweight='bold')
         plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_fhrmeans_'+str(varname)+'_'+str(grid)+str(reg)+'_tp.png', bbox_inches='tight')
      s+=1
