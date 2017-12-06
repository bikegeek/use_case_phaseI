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
sd = datetime.datetime(syear, smon, sday)
ed = datetime.datetime(eyear, emon, eday)+datetime.timedelta(days=1)
tdelta = datetime.timedelta(days=1)
dates = md.drange(sd, ed, tdelta)
#model info
model_fcst = os.environ['modellist'].split(' ')
cyc = os.environ['cycle']
nexp = int(os.environ['nexp'])
grid = os.environ['grid']
reg = os.environ['reg']
thrs = os.environ['thrs']
save_thrs_now = float(thrs) * 10
if save_thrs_now < 10:
   save_thrs='00'+str(int(save_thrs_now))
elif save_thrs_now < 100:
   save_thrs = '0'+str(int(save_thrs_now))
elif save_thrs_now >= 100:
   save_thrs = str(int(save_thrs_now))
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
#ets, bias, and matched pair count time series
n=1
while n <= nexp: #loop over experiments
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
   if nrow == 0:
      bias_now = np.ones_like(dates) * np.nan
      ets_now = np.ones_like(dates) * np.nan
      modeldates = dates
   else:
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
      for d in range(len(valid_dates)):
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
      #bias
      bias_now = np.ma.masked_invalid((a + b)/(a + c))
      #ets
      Ra = ((a + b)*(a + c))/(a + b + c + d)
      ets_now = np.ma.masked_invalid((a - Ra)/(a + b + c - Ra))
   #write threshold mean for forecast hour to file
   #bias
   if fcsthr_e < 10:
      save_meanvar_file = str(DATA_OUTmodel)+'/'+str(model_fcst[n-1])+'/'+str(cyc)+'Z/'+str(reg)+'/bias_mean_f0'+str(fcsthr_e)+'.txt' 
   else:
      save_meanvar_file = str(DATA_OUTmodel)+'/'+str(model_fcst[n-1])+'/'+str(cyc)+'Z/'+str(reg)+'/bias_mean_f'+str(fcsthr_e)+'.txt'
   if os.path.exists(save_meanvar_file):
       append_write = 'a' # append if already exists
   else:
       append_write = 'w' # make a new file if not
   save_meanvar = open(save_meanvar_file,append_write)
   save_meanvar.write(str(thrs)+' '+str(np.mean(bias_now))+ '\n')
   save_meanvar.close()
   #ets
   if fcsthr_e < 10:
      save_meanvar_file = str(DATA_OUTmodel)+'/'+str(model_fcst[n-1])+'/'+str(cyc)+'Z/'+str(reg)+'/ets_mean_f0'+str(fcsthr_e)+'.txt'
   else:
      save_meanvar_file = str(DATA_OUTmodel)+'/'+str(model_fcst[n-1])+'/'+str(cyc)+'Z/'+str(reg)+'/ets_mean_f'+str(fcsthr_e)+'.txt'
   if os.path.exists(save_meanvar_file):
       append_write = 'a' # append if already exists
   else:
       append_write = 'w' # make a new file if not
   save_meanvar = open(save_meanvar_file,append_write)
   save_meanvar.write(str(thrs)+' '+str(np.mean(ets_now))+ '\n')
   save_meanvar.close()
   #plot
   if n == 1:
      fig, (ax1, ax2, ax3) = plt.subplots(3,1,figsize=(10,15), sharex=True)
      #ets
      ax1.plot_date(dates,np.ones_like(dates)*np.nan)
      i nrow > 0:
          print n, model_fcst[n-1]
          ax1.plot_date(modeldates,ets_now, color='k', ls='-', linewidth=2.0, marker='o', markersize='8', label=model_fcst[n-1])
      ax1.set_ylabel('ETS')
      ax1.tick_params(axis='y', pad=15)
      ax1.grid(True)
      #bias
      ax2.plot_date(dates,np.ones_like(dates)*np.nan)
      if nrow > 0:
         ax2.plot_date(modeldates,bias_now, color='k', ls='-', linewidth=2.0, marker='o', markersize='8')
      ax2.set_ylabel('Bias')
      ax2.tick_params(axis='y', pad=15)
      ax2.grid(True)
      #matched pairs
      ax3.plot_date(dates,np.ones_like(dates)*np.nan)
      if nrow > 0:
         ax3.plot_date(modeldates,tot_mp, color='k', ls='-', linewidth=2.0, marker='o', markersize='5')
      ax3.set_ylabel('Matched Pairs')
      ax3.grid(True)
      ax3.set_xlabel('Verification Date')
      ax3.set_xlim([dates[0],dates[-1]])
      if len(dates) <= 31:
         ax3.xaxis.set_major_locator(md.DayLocator(interval=7))
         ax3.xaxis.set_major_formatter(md.DateFormatter('%d%b\n%Y'))
         ax3.xaxis.set_minor_locator(md.DayLocator())
      else:
         ax3.xaxis.set_major_locator(md.MonthLocator())
         ax3.xaxis.set_major_formatter(md.DateFormatter('%b%Y'))
         ax3.xaxis.set_minor_locator(md.DayLocator())
      ax3.tick_params(axis='x', pad=10)
      ax3.tick_params(axis='y', pad=15)
      if reg == 'FULL':
         ax1.set_title(str(varname)+' >='+str(thrs)+'mm/24hr Skill Scores\n'+str(grid)+' Cycle '+str(cyc)+'Z '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' f'+str(fcsthr_s)+'-'+str(fcsthr_e)+'\n\n', fontsize=14, fontweight='bold')
      else:
         ax1.set_title(str(varname)+' >='+str(thrs)+'mm/24hr Skill Scores\n'+str(grid)+': '+str(reg)+' Cycle '+str(cyc)+'Z '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' f'+str(fcsthr_s)+'-'+str(fcsthr_e)+'\n\n', fontsize=14, fontweight='bold')
   else:
      if nrow > 0:
         print n, model_fcst[n-1] 
         ax1.plot_date(modeldates,ets_now, ls='--', marker='o', markersize=5, label=model_fcst[n-1])
         ax2.plot_date(modeldates,bias_now, ls='--', marker='o', markersize=5)
         ax3.plot_date(modeldates,tot_mp, ls='--', marker='o', markersize=5)
   if n == nexp:
      ax1.legend(bbox_to_anchor=(0.025, 1.02, 0.95, .102), loc=3, ncol=nexp, fontsize='13', mode="expand", borderaxespad=0.)
      plt.savefig(str(DATA_OUTimgs_now)+'/etsbias_thrs'+str(save_thrs)+'_f'+str(fcsthr_s)+'-'+str(fcsthr_e)+'.png', bbox_inches='tight')
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
