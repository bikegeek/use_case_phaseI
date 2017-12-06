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
   if fcsthr_in < 10:
      fcsthr = '0'+str(fcsthr_in)
   else:
      fcsthr = str(fcsthr_in)
   sfc_file = str(DATA_OUTmodel)+'/'+str(model_fcst[n-1])+'/sfc/'+str(cyc)+'Z/'+str(reg)+'/parsum_f'+str(fcsthr)+'_'+str(varname)+str(varlevel)+'.txt'
   #get number of rows
   nrow = sum(1 for line in open(sfc_file))
   #get number of columns
   with file(sfc_file) as f:
        line_header = f.readline()
        line = f.readline()
        ncol = len(line.split())
   if nrow == 0: #file blank if stat analysis filters were not all met
        stat_now = np.ones_like(dates)*np.nan
        modeldates=dates
   else:
        #read data file and put in array
        data = list()
        l = 0
        with open(sfc_file) as f:
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
        parsum = data_array[:,23:].astype(float)
        fbar = parsum[:,0]
        stat_now = fbar
        stat_now_name = 'fbar'
        #write forecast hour mean to file
        save_meanvar_file = str(DATA_OUTmodel)+'/'+str(model_fcst[n-1])+'/sfc/'+str(cyc)+'Z/'+str(reg)+'/fbar_mean_'+str(varname)+str(varlevel)+'.txt'
        if os.path.exists(save_meanvar_file):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not
        save_meanvar = open(save_meanvar_file,append_write)
        save_meanvar.write(str(fcsthr_in)+' '+str(np.mean(stat_now))+ '\n')
        save_meanvar.close()
        #plot individual statistic time series
        if n == 1:
            fig, ax = plt.subplots(1,1,figsize=(10,6))
            ax.plot_date(dates,np.ones_like(dates)*np.nan)
            if nrow > 0:
               print n, model_fcst[n-1]
               ax.plot_date(modeldates,stat_now, color=colors[n-1], ls='-', linewidth=2.0, marker='o', markersize='7', label=model_fcst[n-1]+' '+str(round(np.mean(stat_now),3))+' '+str(nrow-1))
            ax.grid(True)
            ax.set_xlabel('Verification Date')
            ax.set_xlim([dates[0],dates[-1]])
            ax.xaxis.set_major_locator(md.MonthLocator())
            ax.xaxis.set_major_formatter(md.DateFormatter('%b %Y'))
            ax.xaxis.set_minor_locator(md.DayLocator())
            ax.tick_params(axis='x', pad=10)
            ax.tick_params(axis='y', pad=15)
            if reg == 'FULL':
               ax.set_title(str(varname)+' '+str(varlevel)+': '+str(stat_now_name)+'\n'+str(grid)+' valid '+str(cyc)+'Z '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' f'+str(fcsthr)+'\n', fontsize=14, fontweight='bold')
            else:
               ax.set_title(str(varname)+' '+str(varlevel)+': '+str(stat_now_name)+'\n'+str(grid)+':'+str(reg)+' valid '+str(cyc)+'Z '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' f'+str(fcsthr)+'\n', fontsize=14, fontweight='bold')
        else:
            if nrow > 0:
               print n, model_fcst[n-1]
               ax.plot_date(modeldates,stat_now, color=colors[n-1], ls='--', marker='o', markersize='7', label=model_fcst[n-1]+' '+str(round(np.mean(stat_now),3))+' '+str(nrow-1))
        if n == nexp:
            ax.legend(bbox_to_anchor=(1.025, 1.0, 0.25, 0.0), loc='upper right', ncol=1, fontsize='13', mode="expand", borderaxespad=0.)
            if reg == 'FULL':
              if fcsthr_in % 24 == 0:
                  plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_day'+str(fcstday)+'_'+str(varname)+'_'+str(varlevel)+'_'+str(grid)+'.png', bbox_inches='tight')
              else: 
                  plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_f'+str(fcsthr)+'_'+str(varname)+'_'+str(varlevel)+'_'+str(grid)+'.png', bbox_inches='tight')
            else:
              if fcsthr_in % 24 == 0:
                 plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_day'+str(fcstday)+'_'+str(varname)+'_'+str(varlevel)+'_'+str(grid)+str(reg)+'.png', bbox_inches='tight')
              else:
                 plt.savefig(str(DATA_OUTimgs_now)+'/'+str(stat_now_name)+'_f'+str(fcsthr)+'_'+str(varname)+'_'+str(varlevel)+'_'+str(grid)+str(reg)+'.png', bbox_inches='tight')
   n+=1
