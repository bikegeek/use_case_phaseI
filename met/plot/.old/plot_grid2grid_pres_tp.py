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
   models_tp_stat_array = np.empty([nexp, len(dates), len(var_level)])
   models_dates_array = np.empty([nexp, len(dates)])
   if stat_now_name == 'ac':
      s+=1
   else:
      print '--- '+str(stat_now_name)
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
               pres_file = str(DATA_OUTmodel)+'/'+str(model_fcst[n-1])+'/pres/'+str(cyc)+'Z/'+str(reg)+'/parsum_f'+str(fcsthr)+'_'+str(varname)+str(varlevel)+'.txt'
               #get number of rows
               nrow = sum(1 for line in open(pres_file))
               #get number of columns
               with file(pres_file) as f:
                 line_header = f.readline()
                 line = f.readline()
                 ncol = len(line.split())
               if nrow == 0: #file blank if stat analysis filters were not all met
                  stat_now = np.ones_like(dates)*np.nan
                  modeldates=dates
                  models_dates_array[n-1,:] = modeldates
                  model_stat_array[n-1,:,v-1] = stat_now
               else:
                  #read data file and put in array
                  data = list()
                  l = 0
                  with open(pres_file) as f:
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
                      if stat_now_name == 'msess':
                         mse = uvffbar + uvoobar - (2*uvfobar)
                         var_o = uvoobar - (uobar**2) - (vobar**2)
                         stat_now = np.ma.masked_invalid(1 - (mse/var_o))
                      if stat_now_name == 'rsd':
                         var_f = uvffbar - (ufbar**2) - (vfbar**2)
                         var_o = uvoobar - (uobar**2) - (vobar**2)
                         stat_now = np.ma.masked_invalid((np.sqrt(var_f))/(np.sqrt(var_o)))
                      if stat_now_name == 'emd':
                         stat_now = np.ma.masked_invalid(np.sqrt((ufbar - uobar)**2 + (vfbar - vobar)**2))
                      if stat_now_name == 'epv':
                         var_f = uvffbar - (ufbar**2) - (vfbar**2)
                         var_o = uvoobar - (uobar**2) - (vobar**2)
                         R = (uvfobar -  (ufbar*uobar) - (vfbar*vobar))/np.sqrt(var_f*var_o)
                         stat_now = np.ma.masked_invalid(np.sqrt(var_f + var_o - (2*np.sqrt(var_f*var_o)*R)))
                      if stat_now_name == 'pcor':
                         var_f = uvffbar - (ufbar**2) - (vfbar**2)
                         var_o = uvoobar - (uobar**2) - (vobar**2)
                         stat_now = np.ma.masked_invalid((uvfobar -  (ufbar*uobar) - (vfbar*vobar))/np.sqrt(var_f*var_o))
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
                      if stat_now_name == 'msess':
                         mse = ffbar + oobar - (2*fobar)
                         var_o = oobar - (obar**2)
                         stat_now = np.ma.masked_invalid(1 - (mse/var_o))
                      if stat_now_name == 'rsd':
                         var_f = ffbar - (fbar**2)
                         var_o = oobar - (obar**2)
                         stat_now = np.ma.masked_invalid((np.sqrt(var_f))/(np.sqrt(var_o)))
                      if stat_now_name == 'emd':
                         stat_now = np.ma.masked_invalid(np.sqrt((fbar - obar)**2))
                      if stat_now_name == 'epv':
                         var_f = ffbar - (fbar**2)
                         var_o = oobar - (obar**2)
                         R = (fobar - (fbar*obar))/np.sqrt(var_f*var_o)
                         stat_now = np.ma.masked_invalid(np.sqrt(var_f + var_o - (2*np.sqrt(var_f*var_o)*R)))
                      if stat_now_name == 'pcor':
                         var_f = ffbar - (fbar**2)
                         var_o = oobar - (obar**2)
                         stat_now = np.ma.masked_invalid((fobar - (fbar*obar))/np.sqrt(var_f*var_o))
                      #account for missing data
                      for d in range(len(dates)):
                         dd = np.where(modeldates == dates[d])[0]
                         if len(dd) != 0:
                             models_dates_array[n-1,d] = modeldates[dd[0]]
                             models_tp_stat_array[n-1,d,v-1] = stat_now[dd[0]]
                         else:
                             models_dates_array[n-1,d] = dates[d]
                             models_tp_stat_array[n-1,d,v-1] = np.nan
               v+=1
         n+=1
      yyv,xxv = np.meshgrid(var_level, dates)
      a = 0
      if nexp == 1:
         fig, (ax1) = plt.subplots(1,1,figsize=(20,15), sharex=True, sharey=True)
         for ax in [ax1]:
              ax.contourf(xxv, yyv, np.ones_like(xxv)*np.nan)
              yy,xx = np.meshgrid(var_level, models_dates_array[a,:])
              C0 = ax.contourf(xx, yy, models_tp_stat_array[a,:,:], cmap=plt.cm.RdYlGn, extend='both')
              ax.grid(True)
              ax.set_xlabel('Verification Date')
              if len(dates) <= 31:
                 ax.xaxis.set_major_locator(md.DayLocator(interval=7))
                 ax.xaxis.set_major_formatter(md.DateFormatter('%d%b%Y'))
                 ax.xaxis.set_minor_locator(md.DayLocator())
              else:
                 ax.xaxis.set_major_locator(md.MonthLocator())
                 ax.xaxis.set_major_formatter(md.DateFormatter('%b%Y'))
                 ax.xaxis.set_minor_locator(md.DayLocator())
              ax.set_xlim([dates[0],dates[-1]])
              ax.set_yscale("log")
              ax.set_yticks(var_level)
              ax.set_yticklabels(var_level)
              ax.set_ylim([var_level[0],var_level[-1]])
              ax.tick_params(axis='x', pad=10)
              ax.tick_params(axis='y', pad=15)
              ax.set_title(str(model_fcst[a]), loc='left')
              a+=1
      if nexp == 2:
         fig, (ax1, ax2) = plt.subplots(1,2,figsize=(20,15), sharex=True, sharey=True)
         for ax in [ax1, ax2]:
              ax.contourf(xxv, yyv, np.ones_like(xxv)*np.nan)
              yy,xx = np.meshgrid(var_level, models_dates_array[a,:])
              if a == 0:
                 C0 = ax.contourf(xx, yy, models_tp_stat_array[a,:,:], cmap=plt.cm.RdYlGn, extend='both')
              else:
                 ax.contourf(xx, yy, models_tp_stat_array[a,:,:], levels=C0.levels, cmap=plt.cm.RdYlGn, extend='both')
              ax.grid(True)
              ax.set_xlabel('Verification Date')
              if len(dates) <= 31:
                 ax.xaxis.set_major_locator(md.DayLocator(interval=7))
                 ax.xaxis.set_major_formatter(md.DateFormatter('%d%b%Y'))
                 ax.xaxis.set_minor_locator(md.DayLocator())
              else:
                 ax.xaxis.set_major_locator(md.MonthLocator())
                 ax.xaxis.set_major_formatter(md.DateFormatter('%b%Y'))
                 ax.xaxis.set_minor_locator(md.DayLocator())
              ax.set_xlim([dates[0],dates[-1]])
              ax.set_yscale("log")
              ax.set_yticks(var_level)
              ax.set_yticklabels(var_level)
              ax.set_ylim([var_level[0],var_level[-1]])
              ax.tick_params(axis='x', pad=10)
              ax.tick_params(axis='y', pad=15)
              ax.set_title(str(model_fcst[a]), loc='left')
              a+=1
      if nexp == 3:
         fig, ((ax1, ax2), (ax3)) = plt.subplots(2,2,figsize=(20,15), sharex=True, sharey=True)
         for ax in [ax1, ax2, ax3]:
              ax.contourf(xxv, yyv, np.ones_like(xxv)*np.nan)
              yy,xx = np.meshgrid(var_level, models_dates_array[a,:])
              if a == 0:
                 C0 = ax.contourf(xx, yy, models_tp_stat_array[a,:,:], cmap=plt.cm.RdYlGn, extend='both')
              else:
                 ax.contourf(xx, yy, models_tp_stat_array[a,:,:], levels=C0.levels, cmap=plt.cm.RdYlGn, extend='both')
              ax.grid(True) 
              ax.set_xlabel('Verification Date')
              if len(dates) <= 31:
                 ax.xaxis.set_major_locator(md.DayLocator(interval=7))
                 ax.xaxis.set_major_formatter(md.DateFormatter('%d%b%Y'))
                 ax.xaxis.set_minor_locator(md.DayLocator())
              else:
                 ax.xaxis.set_major_locator(md.MonthLocator())
                 ax.xaxis.set_major_formatter(md.DateFormatter('%b%Y'))
                 ax.xaxis.set_minor_locator(md.DayLocator())
              ax.set_xlim([dates[0],dates[-1]])
              ax.set_yscale("log")
              ax.set_yticks(var_level)
              ax.set_yticklabels(var_level)
              ax.set_ylim([var_level[0],var_level[-1]])
              ax.tick_params(axis='x', pad=10)
              ax.tick_params(axis='y', pad=15)
              ax.set_title(str(model_fcst[a]), loc='left')
              a+=1
      if nexp == 4:
         fig, ((ax1, ax2), (ax3,ax4)) = plt.subplots(2,2,figsize=(20,15), sharex=True, sharey=True)
         for ax in [ax1, ax2, ax3, ax4]:
              ax.contourf(xxv, yyv, np.ones_like(xxv)*np.nan)
              yy,xx = np.meshgrid(var_level, models_dates_array[a,:])
              if a == 0:
                 C0 = ax.contourf(xx, yy, models_tp_stat_array[a,:,:], cmap=plt.cm.RdYlGn, extend='both')
              else:
                 ax.contourf(xx, yy, models_tp_stat_array[a,:,:], levels=C0.levels, cmap=plt.cm.RdYlGn, extend='both')
              ax.grid(True) 
              ax.set_xlabel('Verification Date')
              if len(dates) <= 31:
                 ax.xaxis.set_major_locator(md.DayLocator(interval=7))
                 ax.xaxis.set_major_formatter(md.DateFormatter('%d%b%Y'))
                 ax.xaxis.set_minor_locator(md.DayLocator())
              else:
                 ax.xaxis.set_major_locator(md.MonthLocator())
                 ax.xaxis.set_major_formatter(md.DateFormatter('%b%Y'))
                 ax.xaxis.set_minor_locator(md.DayLocator())
              ax.set_xlim([dates[0],dates[-1]])
              ax.set_yscale("log")
              ax.set_yticks(var_level)
              ax.set_yticklabels(var_level)
              ax.set_ylim([var_level[0],var_level[-1]])
              ax.tick_params(axis='x', pad=10)
              ax.tick_params(axis='y', pad=15)
              ax.set_title(str(model_fcst[a]), loc='left')
              a+=1
      if nexp == 5: 
         fig, ((ax1, ax2), (ax3,ax4), (ax5)) = plt.subplots(3,2,figsize=(20,15), sharex=True, sharey=True)
         for ax in [ax1, ax2, ax3, ax4, ax5]:
              ax.contourf(xxv, yyv, np.ones_like(xxv)*np.nan)
              yy,xx = np.meshgrid(var_level, models_dates_array[a,:])
              if a == 0:
                 C0 = ax.contourf(xx, yy, models_tp_stat_array[a,:,:], cmap=plt.cm.RdYlGn, extend='both')
              else:
                 ax.contourf(xx, yy, models_tp_stat_array[a,:,:], levels=C0.levels, cmap=plt.cm.RdYlGn, extend='both')
              ax.grid(True)
              ax.set_xlabel('Verification Date')
              if len(dates) <= 31:
                 ax.xaxis.set_major_locator(md.DayLocator(interval=7))
                 ax.xaxis.set_major_formatter(md.DateFormatter('%d%b%Y'))
                 ax.xaxis.set_minor_locator(md.DayLocator())
              else:
                 ax.xaxis.set_major_locator(md.MonthLocator())
                 ax.xaxis.set_major_formatter(md.DateFormatter('%b%Y'))
                 ax.xaxis.set_minor_locator(md.DayLocator())
              ax.set_xlim([dates[0],dates[-1]])
              ax.set_yscale("log")
              ax.set_yticks(var_level)
              ax.set_yticklabels(var_level)
              ax.set_ylim([var_level[0],var_level[-1]])
              ax.tick_params(axis='x', pad=10)
              ax.tick_params(axis='y', pad=15)
              ax.set_title(str(model_fcst[a]), loc='left')
              a+=1
      if nexp == 6: 
         fig, ((ax1, ax2), (ax3,ax4), (ax5,ax6)) = plt.subplots(3,2,figsize=(20,15), sharex=True, sharey=True)
         for ax in [ax1, ax2, ax3, ax4, ax5, ax6]:
              ax.contourf(xxv, yyv, np.ones_like(xxv)*np.nan)
              yy,xx = np.meshgrid(var_level, models_dates_array[a,:])
              if a == 0:
                 C0 = ax.contourf(xx, yy, models_tp_stat_array[a,:,:], cmap=plt.cm.RdYlGn, extend='both')
              else:
                 ax.contourf(xx, yy, models_tp_stat_array[a,:,:], levels=C0.levels, cmap=plt.cm.RdYlGn, extend='both')
              ax.grid(True)
              ax.set_xlabel('Verification Date')
              if len(dates) <= 31:
                 ax.xaxis.set_major_locator(md.DayLocator(interval=7))
                 ax.xaxis.set_major_formatter(md.DateFormatter('%d%b%Y'))
                 ax.xaxis.set_minor_locator(md.DayLocator())
              else:
                 ax.xaxis.set_major_locator(md.MonthLocator())
                 ax.xaxis.set_major_formatter(md.DateFormatter('%b%Y'))
                 ax.xaxis.set_minor_locator(md.DayLocator())
              ax.set_xlim([dates[0],dates[-1]])
              ax.set_yscale("log")
              ax.set_yticks(var_level)
              ax.set_yticklabels(var_level)
              ax.set_ylim([var_level[0],var_level[-1]])
              ax.tick_params(axis='x', pad=10)
              ax.tick_params(axis='y', pad=15)
              ax.set_title(str(model_fcst[a]), loc='left')
              a+=1
      if nexp == 7:
         fig, ((ax1, ax2), (ax3,ax4), (ax5,ax6), (ax7)) = plt.subplots(4,2,figsize=(20,15), sharex=True, sharey=True)
         for ax in [ax1, ax2, ax3, ax4, ax5, ax6, ax7]:
              ax.contourf(xxv, yyv, np.ones_like(xxv)*np.nan)
              yy,xx = np.meshgrid(var_level, models_dates_array[a,:])
              if a == 0:
                 C0 = ax.contourf(xx, yy, models_tp_stat_array[a,:,:], cmap=plt.cm.RdYlGn, extend='both')
              else:
                 ax.contourf(xx, yy, models_tp_stat_array[a,:,:], levels=C0.levels, cmap=plt.cm.RdYlGn, extend='both')
              ax.grid(True)
              ax.set_xlabel('Verification Date')
              if len(dates) <= 31:
                 ax.xaxis.set_major_locator(md.DayLocator(interval=7))
                 ax.xaxis.set_major_formatter(md.DateFormatter('%d%b%Y'))
                 ax.xaxis.set_minor_locator(md.DayLocator())
              else:
                 ax.xaxis.set_major_locator(md.MonthLocator())
                 ax.xaxis.set_major_formatter(md.DateFormatter('%b%Y'))
                 ax.xaxis.set_minor_locator(md.DayLocator())
              ax.set_xlim([dates[0],dates[-1]])
              ax.set_yscale("log")
              ax.set_yticks(var_level)
              ax.set_yticklabels(var_level)
              ax.set_ylim([var_level[0],var_level[-1]])
              ax.tick_params(axis='x', pad=10)
              ax.tick_params(axis='y', pad=15)
              ax.set_title(str(model_fcst[a]), loc='left')
              a+=1
      if nexp == 8:       
         fig, ((ax1, ax2), (ax3,ax4), (ax5,ax6), (ax7,ax8)) = plt.subplots(4,2,figsize=(20,15), sharex=True, sharey=True)
         for ax in [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]:
              ax.contourf(xxv, yyv, np.ones_like(xxv)*np.nan)
              yy,xx = np.meshgrid(var_level, models_dates_array[a,:])
              if a == 0:
                 C0 = ax.contourf(xx, yy, models_tp_stat_array[a,:,:], cmap=plt.cm.RdYlGn, extend='both')
              else:
                 ax.contourf(xx, yy, models_tp_stat_array[a,:,:], levels=C0.levels, cmap=plt.cm.RdYlGn, extend='both')
              ax.grid(True)
              ax.set_xlabel('Verification Date')
              if len(dates) <= 31:
                 ax.xaxis.set_major_locator(md.DayLocator(interval=7))
                 ax.xaxis.set_major_formatter(md.DateFormatter('%d%b%Y'))
                 ax.xaxis.set_minor_locator(md.DayLocator())
              else:
                 ax.xaxis.set_major_locator(md.MonthLocator())
                 ax.xaxis.set_major_formatter(md.DateFormatter('%b%Y'))
                 ax.xaxis.set_minor_locator(md.DayLocator())
              ax.set_xlim([dates[0],dates[-1]])
              ax.set_yscale("log")
              ax.set_yticks(var_level)
              ax.set_yticklabels(var_level) 
              ax.set_ylim([var_level[0],var_level[-1]])
              ax.tick_params(axis='x', pad=10)
              ax.tick_params(axis='y', pad=15)
              ax.set_title(str(model_fcst[a]), loc='left')
              a+=1
      fig.subplots_adjust(right=0.8)
      cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
      fig.colorbar(C0, cax=cbar_ax)
      if reg == 'FULL':
         fig.suptitle(str(varname)+': '+str(stat_now_name)+'\n'+str(grid)+' valid '+str(cyc)+'Z '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' f'+str(fcsthr)+'\n\n', fontsize=14, fontweight='bold')
         if fcsthr_in % 24 == 0:
             plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'p_day'+str(fcstday)+'_'+str(varname)+'_'+str(grid)+'.png', bbox_inches='tight')
         else:
             plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'p_f'+str(fcsthr)+'_'+str(varname)+'_'+str(grid)+'.png', bbox_inches='tight')
      else:
         fig.suptitle(str(varname)+': '+str(stat_now_name)+'\n'+str(grid)+':'+str(reg)+' valid '+str(cyc)+'Z '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' f'+str(fcsthr)+'\n\n', fontsize=14, fontweight='bold')
         if fcsthr_in % 24 == 0:
             plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'p_day'+str(fcstday)+'_'+str(varname)+'_'+str(grid)+str(reg)+'.png', bbox_inches='tight')
         else:
             plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'p_f'+str(fcsthr)+'_'+str(varname)+'_'+str(grid)+str(reg)+'.png', bbox_inches='tight')
      s+=1
