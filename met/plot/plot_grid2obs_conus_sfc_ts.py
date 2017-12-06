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
sd = datetime.datetime(syear, smon, sday)+datetime.timedelta(hours=fcsthr_in)
ed = datetime.datetime(eyear, emon, eday)+datetime.timedelta(hours=fcsthr_in)+datetime.timedelta(days=1)
tdelta = datetime.timedelta(days=1)
dates = md.drange(sd, ed, tdelta)
#model info
model_fcst = os.environ['modellist'].split(' ')
cyc = os.environ['cycle']
nexp = int(os.environ['nexp'])
grid = os.environ['conus_sfc_grid']
reg = os.environ['reg']
DATA_OUTmodel = os.environ['DATA_OUTmodel']
grid2obs_dir_lookin = os.environ['grid2obs_dir_lookin']
#output info
DATA_OUTimgs_now = os.environ['DATA_OUTimgs_now']
plot_stats = os.environ['stats'].split(' ')
nstats = int(os.environ['nstats'])
varname = os.environ['varname']
varlevel = os.environ['varlevel']
#etc
colors = ['k','g', 'r', 'b', 'darkorange', 'darkorchid', 'palevioletred', 'dodgerblue', 'dimgrey', 'mediumseagreen']
#############################################################################
##### Read data in data, compute statistics, and plot
#read in data
s=1
while s <= nstats: #loop over statistics
   stat_now_name = plot_stats[s-1]
   print '--- '+str(stat_now_name)
   n=1
   while n <= nexp: #loop over experiments
     print n, model_fcst[n-1]
     #get file name
     if fcsthr_in < 10:
        fcsthr = '0'+str(fcsthr_in)
     else:
        fcsthr = str(fcsthr_in)
     grid2obs_file = str(DATA_OUTmodel)+'/'+str(model_fcst[n-1])+'/conus_sfc/'+str(cyc)+'Z/'+str(reg)+'/grid2obs_f'+str(fcsthr)+'_'+str(varname)+str(varlevel)+'.txt'
     #get number of rows
     nrow = sum(1 for line in open(grid2obs_file))
     #get number of columns
     with file(grid2obs_file) as f:
         line_header = f.readline()
         line = f.readline()
         ncol = len(line.split())
     if nrow == 0: #file blank if stat analysis filters were not all met
        rms = np.ones_like(dates)*np.nan
        obar = np.ones_like(dates)*np.nan 
        fbar = np.ones_like(dates)*np.nan
        modeldates = dates
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
            dates_list.append(md.date2num(modeldate))
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
           rms = np.ma.masked_invalid(np.sqrt(uvffbar + uvoobar - (2*uvfobar)))
        else: 
            fbar = parsum[:,0]
            obar = parsum[:,1]
            fobar = parsum[:,2]
            ffbar = parsum[:,3]
            oobar = parsum[:,4]
            rms = np.ma.masked_invalid(np.sqrt(ffbar + oobar - (2*fobar)))
     #account for missing data
     fbar_dates = np.zeros_like(dates)
     obar_dates = np.zeros_like(dates)
     rms_dates = np.zeros_like(dates) 
     for d in range(len(dates)):
         dd = np.where(modeldates == dates[d])[0]
         if len(dd) != 0:
             fbar_dates[d] = fbar[dd[0]]
             obar_dates[d] = obar[dd[0]]
             rms_dates[d] = rms[dd[0]]
         else:
             fbar_dates[d] = np.nan
             obar_dates[d] = np.nan
             rms_dates[d] = np.nan
     if stat_now_name == 'bias':
        if ((varname == 'TMP') or (varname == 'DPT')):
            fbar = fbar - 273.15
            obar = obar - 273.15
            fbar_dates = fbar_dates - 273.15
            obar_dates = obar_dates - 273.15
        if varname == 'SLP':
            fbar = fbar/100.
            obar = obar/100.
            fbar_dates = fbar_dates/100.
            obar_dates = obar_dates/100.
        fig, (ax1) = plt.subplots(1,1,figsize=(10,6), sharex=True)
        #write forecast hour mean to file
        save_meanvar_file = str(DATA_OUTmodel)+'/'+str(model_fcst[n-1])+'/conus_sfc/'+str(cyc)+'Z/'+str(reg)+'/fbar_mean_'+str(varname)+str(varlevel)+'.txt'
        if os.path.exists(save_meanvar_file):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not
        save_meanvar = open(save_meanvar_file,append_write)
        save_meanvar.write(str(fcsthr_in)+' '+str(np.mean(fbar))+ '\n')
        save_meanvar.close()
        #write observation forecast hour mean to file
        if n == 1:
           save_meanvar_file = str(DATA_OUTmodel)+'/'+str(model_fcst[n-1])+'/conus_sfc/'+str(cyc)+'Z/'+str(reg)+'/obar_mean_'+str(varname)+str(varlevel)+'.txt'
           if os.path.exists(save_meanvar_file):
               append_write = 'a' # append if already exists
           else:
               append_write = 'w' # make a new file if not
           save_meanvar = open(save_meanvar_file,append_write)
           save_meanvar.write(str(fcsthr_in)+' '+str(np.mean(obar))+ '\n')
           save_meanvar.close()
        #plot individual statistic time series
        if n == 1:
           fig, (ax1, ax2) = plt.subplots(2,1,figsize=(10,10), sharex=True)
           #fbar/obar
           ax1.plot_date(dates, np.ones_like(dates)*np.nan)
           if nrow > 0:
              ax1.plot_date(dates, obar_dates, color=colors[n-1], ls='-', linewidth=2.0, marker='None', label='obs '+str(round(np.mean(obar),2))+' '+str(nrow-1))
              ax1.plot_date(dates, fbar_dates, color=colors[n], ls='-', linewidth=1.0, marker='None', label=model_fcst[n-1]+' '+str(round(np.mean(fbar),2))+' '+str(nrow-1))
              #ax1.plot_date(modeldates, obar, color=colors[n-1], ls='-', linewidth=2.0, marker='None', label='obs '+str(round(np.mean(obar),2))+' '+str(nrow-1))
              #ax1.plot_date(modeldates, fbar, color=colors[n], ls='-', linewidth=1.0, marker='None', label=model_fcst[n-1]+' '+str(round(np.mean(fbar),2))+' '+str(nrow-1))
           ax1.grid(True)
           ax1.tick_params(axis='x', pad=10)
           ax1.tick_params(axis='y', pad=15)
           #difference from obs
           ax2.plot_date(dates,np.zeros_like(dates))
           if nrow > 0:
              ax2.plot_date(dates, fbar_dates-obar_dates, color=colors[n], ls='-', linewidth=1.0, marker='None',  label=model_fcst[n-1]+'-obs '+str(round(np.mean(fbar-obar),2)))
              #ax2.plot_date(modeldates, fbar-obar, color=colors[n], ls='-', linewidth=1.0, marker='None',  label=model_fcst[n-1]+'-obs '+str(round(np.mean(fbar-obar),2)))
           ax2.grid(True)
           ax2.set_xlabel('Verification Date')
           ax2.set_xlim([dates[0],dates[-1]])
           if len(dates) <= 31:
                ax2.xaxis.set_major_locator(md.DayLocator(interval=7))
                ax2.xaxis.set_major_formatter(md.DateFormatter('%d%b\n%Y'))
                ax2.xaxis.set_minor_locator(md.DayLocator())
           else:
                ax2.xaxis.set_major_locator(md.MonthLocator())
                ax2.xaxis.set_major_formatter(md.DateFormatter('%b%Y'))
                ax2.xaxis.set_minor_locator(md.DayLocator())
           ax2.tick_params(axis='x', pad=10)
           ax2.tick_params(axis='y', pad=15)
           if reg == 'FULL':
              ax1.set_title(str(varname)+' '+str(varlevel)+': '+str(stat_now_name)+'\n'+str(grid)+' initialized '+str(cyc)+'Z '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' f'+str(fcsthr)+'\n\n', fontsize=14, fontweight='bold')
           else:
              ax1.set_title(str(varname)+' '+str(varlevel)+': '+str(stat_now_name)+'\n'+str(grid)+':'+str(reg)+' initialized '+str(cyc)+'Z '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' f'+str(fcsthr)+'\n\n', fontsize=14, fontweight='bold')
        else:
           if nrow > 0:
              ax1.plot_date(dates, fbar_dates, color=colors[n], ls='-', linewidth=1.0, marker='None', label=model_fcst[n-1]+' '+str(round(np.mean(obar),2))+' '+str(nrow-1))
              ax2.plot_date(dates, fbar_dates-obar_dates, color=colors[n], ls='-', linewidth=1.0, marker='None', label=model_fcst[n-1]+'-obs '+str(round(np.mean(fbar-obar),2)))
              #ax1.plot_date(modeldates, fbar, color=colors[n], ls='-', linewidth=1.0, marker='None', label=model_fcst[n-1]+' '+str(round(np.mean(obar),2))+' '+str(nrow-1))
              #ax2.plot_date(modeldates, fbar-obar, color=colors[n], ls='-', linewidth=1.0, marker='None', label=model_fcst[n-1]+'-obs '+str(round(np.mean(fbar-obar),2)))
        if n == nexp:
           ax1.legend(bbox_to_anchor=(1.025, 1.0, 0.25, 0.0), loc='upper right', ncol=1, fontsize='13', mode="expand", borderaxespad=0.)
           ax2.legend(bbox_to_anchor=(1.025, 1.0, 0.25, 0.0), loc='upper right', ncol=1, fontsize='13', mode="expand", borderaxespad=0.)
           #if reg == 'FULL':
           #   if fcsthr_in % 24 == 0:
           #       plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_day'+str(fcstday)+'_'+str(varname)+'_SFC_'+str(grid)+'.png', bbox_inches='tight')
           #   else:
           #       plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_f'+str(fcsthr)+'_'+str(varname)+'_SFC_'+str(grid)+'.png', bbox_inches='tight')
           #else:
           #   if fcsthr_in % 24 == 0:
           #      plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_day'+str(fcstday)+'_'+str(varname)+'_SFC_'+str(grid)+str(reg)+'.png', bbox_inches='tight')
           #   else:
           #      plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_f'+str(fcsthr)+'_'+str(varname)+'_SFC_'+str(grid)+str(reg)+'.png', bbox_inches='tight')
           if reg == 'FULL':
              plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_f'+str(fcsthr)+'_'+str(varname)+'_SFC_'+str(grid)+'.png', bbox_inches='tight')
           else:
              plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_f'+str(fcsthr)+'_'+str(varname)+'_SFC_'+str(grid)+str(reg)+'.png', bbox_inches='tight')
     elif stat_now_name == 'rms':
        #write forecast hour mean to file
        save_meanvar_file = str(DATA_OUTmodel)+'/'+str(model_fcst[n-1])+'/conus_sfc/'+str(cyc)+'Z/'+str(reg)+'/rms_mean_'+str(varname)+str(varlevel)+'.txt'
        if os.path.exists(save_meanvar_file):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not
        save_meanvar = open(save_meanvar_file,append_write)
        save_meanvar.write(str(fcsthr_in)+' '+str(np.mean(rms))+ '\n')
        save_meanvar.close()
        #plot individual statistic time series
        if n == 1:
           fig, ax1 = plt.subplots(1,1,figsize=(10,6), sharex=True)
           #rmse
           ax1.plot_date(dates, np.ones_like(dates)*np.nan)
           if nrow > 0:
              ax1.plot_date(dates, rms_dates, color=colors[n-1], ls='-', linewidth=2.0, marker='None', label=model_fcst[n-1]+' '+str(round(np.mean(rms),2))+' '+str(nrow-1))
              #ax1.plot_date(modeldates, rms, color=colors[n-1], ls='-', linewidth=2.0, marker='None', label=model_fcst[n-1]+' '+str(round(np.mean(rms),2))+' '+str(nrow-1))
           ax1.grid(True)
           ax1.set_xlabel('Verification Date')
           ax1.set_xlim([dates[0],dates[-1]])
           if len(dates) <= 31:
                ax1.xaxis.set_major_locator(md.DayLocator(interval=7))
                ax1.xaxis.set_major_formatter(md.DateFormatter('%d%b%Y'))
                ax1.xaxis.set_minor_locator(md.DayLocator())
           else:
                ax1.xaxis.set_major_locator(md.MonthLocator())
                ax1.xaxis.set_major_formatter(md.DateFormatter('%b%Y'))
                ax1.xaxis.set_minor_locator(md.DayLocator())
           ax1.tick_params(axis='x', pad=10)
           ax1.tick_params(axis='y', pad=15)
           if reg == 'FULL':
              ax1.set_title(str(varname)+' '+str(varlevel)+': '+str(stat_now_name)+'\n'+str(grid)+' initialized '+str(cyc)+'Z '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' f'+str(fcsthr)+'\n\n', fontsize=14, fontweight='bold')
           else:
              ax1.set_title(str(varname)+' '+str(varlevel)+': '+str(stat_now_name)+'\n'+str(grid)+':'+str(reg)+' initialized '+str(cyc)+'Z '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' f'+str(fcsthr)+'\n\n', fontsize=14, fontweight='bold')
        else:
           if nrow > 0:
              ax1.plot_date(dates, rms_dates, color=colors[n-1], ls='-', linewidth='1.5', marker='None', label=model_fcst[n-1]+' '+str(round(np.mean(rms),2))+' '+str(nrow-1))
              #ax1.plot_date(modeldates, rms, color=colors[n-1], ls='-', linewidth='1.5', marker='None', label=model_fcst[n-1]+' '+str(round(np.mean(rms),2))+' '+str(nrow-1))
        if n == nexp:
           ax1.legend(bbox_to_anchor=(1.025, 1.0, 0.25, 0.0), loc='upper right', ncol=1, fontsize='13', mode="expand", borderaxespad=0.)
           #if reg == 'FULL':
           #   if fcsthr_in % 24 == 0:
           #       plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_day'+str(fcstday)+'_'+str(varname)+'_SFC_'+str(grid)+'.png', bbox_inches='tight')
           #   else:
           #       plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_f'+str(fcsthr)+'_'+str(varname)+'_SFC_'+str(grid)+'.png', bbox_inches='tight')
           #else:
           #   if fcsthr_in % 24 == 0:
           #      plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_day'+str(fcstday)+'_'+str(varname)+'_SFC_'+str(grid)+str(reg)+'.png', bbox_inches='tight')
           #   else:
           #      plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_f'+str(fcsthr)+'_'+str(varname)+'_SFC_'+str(grid)+str(reg)+'.png', bbox_inches='tight')
           if reg == 'FULL':
             plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_f'+str(fcsthr)+'_'+str(varname)+'_SFC_'+str(grid)+'.png', bbox_inches='tight')
           else:
             plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_f'+str(fcsthr)+'_'+str(varname)+'_SFC_'+str(grid)+str(reg)+'.png', bbox_inches='tight')
     n+=1
   s+=1  
