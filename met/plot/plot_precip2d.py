#############################################################################
##### Import python modules
import os
import numpy as np
import netCDF4 as netcdf
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
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
##### Definitions
def area_average(season_mean_var,lat,lon,dspace):
    #mx = season_mean_var
    mx = np.ma.masked_invalid(season_mean_var)
    latr = np.deg2rad(lat)
    weights = np.empty_like(season_mean_var)
    weightsum = 0
    arraysum = 0
    for y in range(len(lat)):
        if lat[y] == -90.0:
            weights[y,:] = 0
        elif lat[y] == 90.0:
            weights[y,:] = 0
        elif np.cos(latr[y]) != 0:
            weights[y,:] = (np.sin(np.deg2rad((lat[y] + lat[y+1])/2.)) - np.sin(np.deg2rad((lat[y] + lat[y-1])/2.))) * dspace
        for x in range(len(lon)):
            if mx[y,x] <= -9999.:
                arraysum = arraysum
                weightsum = weightsum
            else:
                arraysum = arraysum + (mx[y,x] * weights[y,x])
                weightsum = weightsum + weights[y,x]
    aa_mean = arraysum/weightsum
    return aa_mean
#############################################################################
##### Read in data
#date info
#DATA_OUTimgs = os.environ['DATA_OUTimgs']
#month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
#sdate = os.environ['sdate']
#syear = sdate[:4]
#smon = int(sdate[4:6])
#smonth = month_name[smon-1]
#sday = sdate[6:8]
#edate=os.environ['edate']
#eyear = edate[:4]
#emon = int(edate[4:6])
#emonth = month_name[emon-1]
#eday = edate[6:8]
#model infor
#cyc = edate[-2:]
#asub = os.environ['asub']
#model_fcst = os.environ['model_fcst_name']
#model_obs = os.environ['model_obs_name']
#fname = os.environ['datafile']
#read output file
f = netcdf.Dataset('/scratch4/NCEPDEV/global/save/Mallory.Row/VRFY/met/out_ccpa/precip/model/gfs/00Z/grid_stat_360000L_20170101_120000V_pairs.nc')
lat = f.variables['lat'][:]
dlat = 181/len(lat)
lon = f.variables['lon'][:]
var_F = f.variables['FCST_APCP_24_A24_CONUS'][:]
var_O = f.variables['OBS_APCP_00_L0_CONUS'][:] * 0.0393701
#############################################################################
##### Plotting
#plot settings
#pltcm_diff = plt.cm.bwr
#vardes, savename, levels, levels_diff, pltcm, varscale = pd.plot_settings(varname, varGRIBlvltyp, varlevel)
#plot data
levels = np.array([0.01,0.1,0.25,0.75,1,1.5,2,2.5,3,4,5,6,8,10])
#levels = np.array([0.1,2.0,5.0,15.0,20.0,25.0,35.0,50.0,75.0,100.0,125.0,150.0,175.0])
levels_diff = levels
#pltcm = plt.cm.bgr_r
pltcm = plt.cm.jet
pltcm_diff = pltcm
plt.figure(figsize=(15,17))
gs1 = gridspec.GridSpec(1,1)
ax0 = plt.subplot(gs1[0])
#ax1 = plt.subplot(gs1[1])
#gs1.update(wspace=0.05, hspace=0.05)
nn = 0
for ax in [ax0]:
          m = Basemap(llcrnrlon=-125.,llcrnrlat=20.,urcrnrlon=-57.,urcrnrlat=55.,
            projection='lcc',lat_1=15.,lat_2=25.,lon_0=-100.,
            resolution ='l',area_thresh=1000.)
          #m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,llcrnrlon=0,urcrnrlon=360,resolution='c', ax=ax)
          m.drawcoastlines(linewidth=1.5, color='k')
          m.drawcountries(linewidth=1.5, color='k')
          m.drawstates(linewidth=1.5, color='k')
          m.drawmapboundary
          xx,yy = m(lon, lat)
          if nn == 0:
             m.drawmeridians(np.arange(0,361,20), labels=[False,False,False,True],fontsize=15)
             m.drawparallels(np.arange(-90,91,10), labels=[True,False,False,False],fontsize=15)
             CF = m.contourf(xx, yy, var_O, levels=levels, cmap=pltcm, extend='both')
             box = ax0.get_position()
             axColor = plt.axes([box.x0, box.y0-0.035, box.width, box.height/11.])
             bar = plt.colorbar(CF, cax=axColor, orientation='horizontal',extend='both',ticks=levels)
             #C = m.contour(xx, yy, var_OBAR*varscale, levels=levels, colors='k', linewidths=1.0)
             #ax0.clabel(C,levels, fmt='%g', inline=True, fontsize=12.5)
             #ax0.set_title(str(model_obs), loc='left', fontsize=18)
             #ax0.set_title(round(area_average(np.ma.filled(var_OBAR),lat,lon,dlat)*varscale,3), loc='right', fontsize=18)
          if nn == 1:
             m.drawmeridians(np.arange(0,361,60), labels=[False,False,False,True],fontsize=15)
             m.drawparallels(np.arange(-90,91,30), labels=[True,False,False,False],fontsize=15)
             CF = m.contourf(xx, yy, var_F, levels=levels_diff, cmap=pltcm_diff, extend='both')
             box = ax1.get_position()
             axColor = plt.axes([box.x0, box.y0-0.05, box.width, box.height/11.])
             bar = plt.colorbar(CF, cax=axColor, orientation='horizontal',extend='both',ticks=levels_diff)
             #ax1.set_title(str(model_fcst)+'-'+(model_obs), loc='left', fontsize=18)
             #ax1.set_title(round(area_average(np.ma.filled(var_ME),lat,lon,dlat)*varscale,3), loc='right', fontsize=18)
          nn += 1
#plt.suptitle(str(vardes)+'\n'+str(cyc)+'Z-Cyc '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' Mean\n('+str(asub)+') Fcst-Hour Average', fontsize=18, fontweight='bold')
#plt.savefig(str(DATA_OUTimgs)+'/'+str(model_fcst)+'/'+str(savename)+'.png', bbox_inches='tight')
plt.savefig('precip_ccpa_20170101_in.png')
#print 'Done plotting plot_ME.py'
