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
fcsthr_e = int(os.environ['fcsthr'])
fcsthr_s = fcsthr_e - 24
if fcsthr_s < 10:
   fcsthr_s = '0'+str(fcsthr_s)
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
varname = os.environ['varname']
#############################################################################
##### Read data in data, compute statistics, and plot
#read in data
#ets and bias threshold mean time series
n=1
while n <= nexp: #loop over experiments
   #get file name
   if fcsthr_e < 10:
      ets_mean_file = str(DATA_OUTmodel)+'/'+str(model_fcst[n-1])+'/'+str(cyc)+'Z/'+str(reg)+'/ets_mean_f0'+str(fcsthr_e)+'.txt'
      bias_mean_file = str(DATA_OUTmodel)+'/'+str(model_fcst[n-1])+'/'+str(cyc)+'Z/'+str(reg)+'/bias_mean_f0'+str(fcsthr_e)+'.txt'
   else:
      ets_mean_file = str(DATA_OUTmodel)+'/'+str(model_fcst[n-1])+'/'+str(cyc)+'Z/'+str(reg)+'/ets_mean_f'+str(fcsthr_e)+'.txt'
      bias_mean_file = str(DATA_OUTmodel)+'/'+str(model_fcst[n-1])+'/'+str(cyc)+'Z/'+str(reg)+'/bias_mean_f'+str(fcsthr_e)+'.txt'
   #get number of rows
   nrow_ets = sum(1 for line in open(ets_mean_file))
   nrow_bias = sum(1 for line in open(bias_mean_file))
   #get number of columns
   with file(ets_mean_file) as f:
      line_header = f.readline()
      line = f.readline()
      ncol_ets = len(line.split())
   with file(bias_mean_file) as f:
      line_header = f.readline()
      line = f.readline()
      ncol_bias = len(line.split())
   #read data file and put in array
   data_ets = list()
   with open(ets_mean_file) as f:
      for line in f:
          line_split = line.split()
          data_ets.append(line_split)
   data_array_ets = np.asarray(data_ets)
   data_bias = list()
   with open(bias_mean_file) as f:
      for line in f:
          line_split = line.split()
          data_bias.append(line_split)
   data_array_bias = np.asarray(data_bias)
   #set variables
   thrs_ets = data_array_ets[:,0].astype(float)
   thrs_ets_mean = data_array_ets[:,1]
   for x in range(len(thrs_ets_mean)):
       if thrs_ets_mean[x] == '--':
          thrs_ets_mean[x] = np.nan
   thrs_ets_mean = thrs_ets_mean.astype(float)
   count_nan_ets = np.count_nonzero(np.isnan(thrs_ets_mean))
   thrs_bias = data_array_bias[:,0].astype(float)
   thrs_bias_mean = data_array_bias[:,1]
   for x in range(len(thrs_bias_mean)):
       if thrs_bias_mean[x] == '--':
          thrs_bias_mean[x] = np.nan
   thrs_bias_mean = thrs_bias_mean.astype(float)
   count_nan_bias = np.count_nonzero(np.isnan(thrs_bias_mean))
   #plot
   thrs_ticks = np.arange(0,len(thrs_ets),1)
   if n == 1:
      fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2,figsize=(15,15), sharex=True)
      #ets mean
      if count_nan_ets != len(thrs_ets_mean):
         print n, model_fcst[n-1]
         ax1.plot(thrs_ticks,thrs_ets_mean, color='k', ls='-', linewidth=2.0, marker='o', markersize='8', label=model_fcst[n-1])
      thrs_ets_mean_exp1 = thrs_ets_mean
      ax1.set_ylabel('ETS')
      ax1.tick_params(axis='y', pad=15)
      ax1.grid(True)
      #bias mean
      if count_nan_bias != len(thrs_biass_mean):
         ax2.plot(thrs_ticks,thrs_bias_mean, color='k', ls='-', linewidth=2.0, marker='o', markersize='5')
      thrs_bias_mean_exp1 = thrs_bias_mean
      ax2.set_ylabel('Bias')
      ax2.tick_params(axis='y', pad=15)
      ax2.grid(True)
      #ets differrnce
      ax3.plot(thrs_ticks, np.zeros_like(thrs_ets), color='k')
      ax3.text(0, -0.2, 'Differences outside the outline bars are significant at the 95% confidence interval', fontsize=12, bbox={'facecolor':'white', 'alpha':0, 'pad':5}, transform=ax3.transAxes)
      ax3.set_xticklabels(thrs_ets)
      ax3.set_xlim([0,thrs_ticks[len(thrs_ticks)-1]])
      ax3.set_xlabel('Threshold (mm/24hr)')
      ax3.tick_params(axis='x', pad=10)
      ax3.tick_params(axis='y', pad=15)
      ax3.set_title('Difference with Respect to '+str(model_fcst[0]))
      ax3.grid(True)
      #bias difference
      ax4.plot(thrs_ticks, np.zeros_like(thrs_bias), color='k')
      ax4.set_xlim([0,thrs_ticks[len(thrs_ticks)-1]])
      ax4.set_xlabel('Threshold (mm/24hr)')
      ax4.tick_params(axis='x', pad=10)
      ax4.tick_params(axis='y', pad=15)
      ax4.set_title('Difference with Respect to '+str(model_fcst[0]))
      ax4.grid(True)
      if reg == 'FULL':
         fig.suptitle(str(varname)+' Skill Scores\n'+str(grid)+' Cycle '+str(cyc)+'Z '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' f'+str(fcsthr_s)+'-'+str(fcsthr_e)+'\n\n', fontsize=14, fontweight='bold')
      else:
         fig.suptitle(str(varname)+' Skill Scores\n'+str(grid)+': '+str(reg)+' Cycle '+str(cyc)+'Z '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' f'+str(fcsthr_s)+'-'+str(fcsthr_e)+'\n\n', fontsize=14, fontweight='bold')
   else:
      if count_nan_ets != len(thrs_ets_mean):
         print n, model_fcst[n-1]
         #ets mean
         ax1.plot(thrs_ticks,thrs_ets_mean, ls='--', marker='o', markersize=5, label=model_fcst[n-1])
         #ets difference
         ax3.plot(thrs_ticks, thrs_ets_mean - thrs_ets_mean_exp1, ls='--', marker='o', markersize=5)
      if count_bias_ets != len(thrs_bias_mean):
         #bias mean
         ax2.plot(thrs_ticks,thrs_bias_mean, ls='--', marker='o', markersize=5)
         #bias difference
         ax4.plot(thrs_ticks, thrs_bias_mean - thrs_bias_mean_exp1, ls='--', marker='o', markersize=5)
   if n == nexp:
      ax1.legend(bbox_to_anchor=(0.025, 1.02, 0.95, .102), loc=3, ncol=nexp, fontsize='13', mode="expand", borderaxespad=0.)
      plt.savefig(str(DATA_OUTimgs_now)+'/etsbias_f'+str(fcsthr_s)+'-'+str(fcsthr_e)+'.png', bbox_inches='tight')
   n+=1
exit()
#################################################################
#################################################################
#################################################################
#################################################################
#################################################################
#individual stats time series
s=1
while s <= nstats: #loop over statistics
   stat_now_name = plot_stats[s-1]
   print '--- '+str(stat_now_name)
   n=1
   while n <= nexp: #loop over experiments
      print n, model_fcst[n-1]
      #get file name
      if fcsthr_e < 10:
         precip_file = str(DATA_OUTmodel)+'/'+str(model_fcst[n-1])+'/'+str(cyc)+'Z/'+str(reg)+'/precip_f0'+str(fcsthr_e)+'_thrs'+str(thrs)+'.txt'
      else:
         precip_file = str(DATA_OUTmodel)+'/'+str(model_fcst[n-1])+'/'+str(cyc)+'Z/'+str(reg)+'/precip_f'+str(fcsthr_e)+'_thrs'+str(thrs)+'.txt' 
      #get number of rows
      nrow = sum(1 for line in open(precip_file))
      #get number of columns
      with file(precip_file) as f:
         line_header = f.readline()
         line = f.readline()
         ncol = len(line.split())
      #read data file and put in array
      data = list()
      l = 0
      with open(precip_file) as f:
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
      for d in range(len(dates)):
          modeldate = datetime.datetime.strptime(valid_dates[d], dateformat)
          dates_list.append(int(md.date2num(modeldate)))
      modeldates = np.asarray(dates_list)
      #set contingency table count variables
      ctc = data_array[:,22:].astype(float)
      tot_mp = ctc[:,0]
      a = ctc[:,1]
      b = ctc[:,2]
      c = ctc[:,3]
      d = ctc[:,4]
      if stat_now_name == 'bias':
          stat_now = (a + b)/(a + c)
      if stat_now_name == 'ets':
          Ra = ((a + b)*(a + c))/(a + b + c + d)
          stat_now = (a - Ra)/(a + b + c - Ra) 
      #write forecast hour mean to file
      save_meanvar_file = str(DATA_OUTmodel)+'/'+str(model_fcst[n-1])+'/'+str(cyc)+'Z/'+str(reg)+'/'+str(stat_now_name)+'_mean_'+str(thrs)+'.txt'
      if os.path.exists(save_meanvar_file):
         append_write = 'a' # append if already exists
      else:
         append_write = 'w' # make a new file if not
      save_meanvar = open(save_meanvar_file,append_write)
      save_meanvar.write(str(fcsthr_e)+' '+str(np.nanmean(stat_now))+ '\n')
      save_meanvar.close()
      #plot
      if n == 1:
         fig, ax = plt.subplots(1,1,figsize=(10,6))
         ax.plot_date(dates,np.ones_like(dates)*np.nan)
         ax.plot_date(modeldates,stat_now, color='k', ls='-', linewidth=2.0, marker='None', label=model_fcst[n-1]+' '+str(round(np.mean(stat_now),3))+' '+str(nrow-1))
         ax.grid(True)
         ax.set_xlabel('Verification Date')
         ax.set_xlim([dates[0],dates[-1]])
         ax.xaxis.set_major_locator(md.MonthLocator())
         ax.xaxis.set_major_formatter(md.DateFormatter('%b %Y'))
         ax.xaxis.set_minor_locator(md.DayLocator())
         ax.tick_params(axis='x', pad=15)
         ax.tick_params(axis='y', pad=15)
         if reg == 'FULL':
            ax.set_title(str(varname)+' >='+str(thrs)+': '+str(stat_now_name)+'\n'+str(grid)+' valid '+str(cyc)+'Z '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' f'+str(fcsthr_s)+'-'+str(fcsthr_e)+'\n\n', fontsize=14, fontweight='bold')
         else:
            ax.set_title(str(varname)+' >='+str(thrs)+': '+str(stat_now_name)+'\n'+str(grid)+':'+str(reg)+' valid '+str(cyc)+'Z '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' f'+str(fcsthr_s)+'-'+str(fcsthr_e)+'\n\n', fontsize=14, fontweight='bold')
      else:
         ax.plot_date(modeldates,stat_now, ls='--', marker='^', markersize=10, label=model_fcst[n-1]+' '+str(round(np.mean(stat_now),3))+' '+str(nrow-1))
      if n == nexp:
         plt.legend(bbox_to_anchor=(0.025, 1.02, 0.95, .102), loc=3, ncol=nexp, fontsize='13', mode="expand", borderaxespad=0.)
         if reg == 'FULL':
               plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_f'+str(fcsthr_s)+'-'+str(fcsthr_e)+'_thrs'+str(thrs)+'_'+str(grid)+'.png', bbox_inches='tight')
         else:
              plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_f'+str(fcsthr_s)+'-'+str(fcsthr_e)+'_thrs'+str(thrs)+'_'+str(grid)+str(reg)+'.png', bbox_inches='tight')
      n+=1
   s+=1  
