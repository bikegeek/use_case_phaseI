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
plt.rcParams['contour.negative_linestyle'] = 'solid'
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
DATA_OUTimgs = os.environ['DATA_OUTimgs_model2model']
DATA_OUTmodel = os.environ['DATA_OUTmodel_model2model']
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
cyc = os.environ['cycle']
fday = os.environ['fday']
fhr_list = os.environ['fhr_list']
nexp = int(os.environ['nexp'])
model_fcst_list = os.environ['modellist'].split(' ')
model_obs = os.environ['model_obs']
#variable info
varname = os.environ['var_name_now']
varGRIBlvltyp = os.environ['var_GRIBlvltyp_now']
varlevel = os.environ['var_level_now']
#############################################################################
##### Plotting
#plot settings
pltcm_diff = plt.cm.bwr
vardes, savename, levels, levels_diff, pltcm, varscale = pd.plot_settings(varname, varGRIBlvltyp, varlevel)
#plot data
if nexp == 2:
   fig = plt.figure(figsize=(10,12))
   gs = gridspec.GridSpec(2,1)
   gs.update(wspace=0.1, hspace=0.1)
elif nexp > 2 and nexp <= 4:
   fig = plt.figure(figsize=(15,10))
   gs = gridspec.GridSpec(2,2)
   gs.update(wspace=0.12, hspace=0.1)
elif nexp > 4 and nexp <= 6:
   fig = plt.figure(figsize=(18,10))
   gs = gridspec.GridSpec(2,3)
   gs.update(wspace=0.15, hspace=0.15)
elif nexp > 6:
   fig = plt.figure(figsize=(21,12))
   gs = gridspec.GridSpec(3,3)
   gs.update(wspace=0.15, hspace=0.05)
ax_obs = plt.subplot(gs[0])
nn = 2
while nn <= nexp:
   fname = str(DATA_OUTmodel)+'/'+str(model_fcst_list[nn-1])+'/'+str(cyc)+'Z/'+str(fday)+'/seriesanalysis_'+str(varname)+'_'+str(varGRIBlvltyp)+str(varlevel)+'.nc'
   print(fname)
   f = netcdf.Dataset(fname)
   lat = f.variables['lat'][:]
   dlat = 181/len(lat)
   lon = f.variables['lon'][:]
   var_OBAR = f.variables['series_cnt_OBAR'][:]
   var_OBAR_cyc, lon_cyc = addcyclic(var_OBAR, lon)
   var_FBAR = f.variables['series_cnt_FBAR'][:]
   var_FBAR_cyc, lon_cyc = addcyclic(var_FBAR, lon)
   #plot obs
   if nn == 2:
      m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,llcrnrlon=0,urcrnrlon=360,resolution='c', ax=ax_obs)
      m.drawcoastlines(linewidth=1.5, color='k', zorder=6)
      m.drawmapboundary
      x,y = np.meshgrid(lon_cyc, lat)
      xx,yy = m(x, y)
      m.drawmeridians(np.arange(0,361,60), labels=[False,False,False,True],fontsize=15)
      m.drawparallels(np.arange(-90,91,30), labels=[True,False,False,False],fontsize=15)
      CF = m.contourf(xx, yy, var_OBAR_cyc*varscale, levels=levels, cmap=pltcm, extend='both')
      C = m.contour(xx, yy, var_OBAR_cyc*varscale, levels=levels, colors='k', linewidths=1.0)
      ax_obs.clabel(C,levels, fmt='%g', inline=True, fontsize=12.5)
      ax_obs.set_title(str(model_obs), loc='left', fontsize=18)
      ax_obs.set_title(round(area_average(np.ma.filled(var_OBAR),lat,lon,dlat)*varscale,3), loc='right', fontsize=18)
   #plot difference 
   ax_fcst = plt.subplot(gs[nn-1])
   m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,llcrnrlon=0,urcrnrlon=360,resolution='c', ax=ax_fcst)
   m.drawcoastlines(linewidth=1.5, color='k', zorder=6)
   m.drawmapboundary
   x,y = np.meshgrid(lon_cyc,lat)
   xx,yy = m(x, y)
   m.drawmeridians(np.arange(0,361,60), labels=[False,False,False,True],fontsize=15)
   m.drawparallels(np.arange(-90,91,30), labels=[True,False,False,False],fontsize=15)
   CF = m.contourf(xx, yy, (var_FBAR_cyc - var_OBAR_cyc)*varscale, levels=levels_diff, cmap=pltcm_diff, extend='both')
   if nn == nexp:
      cax = fig.add_axes([0.1, 0.05, 0.8, 0.05])
      fig.colorbar(CF, cax=cax, orientation='horizontal')
   ax_fcst.set_title(str(model_fcst_list[nn-1])+'-'+(model_obs), loc='left', fontsize=18)
   ax_fcst.set_title(round(area_average(np.ma.filled((var_FBAR - var_OBAR)*varscale),lat,lon,dlat),3), loc='right', fontsize=18)
   nn += 1
plt.suptitle(str(vardes)+'\n'+str(cyc)+'Z-Cyc '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' Mean\n('+str(fhr_list)+') Fcst-Hour Average', fontsize=18, fontweight='bold')
plt.savefig(str(DATA_OUTimgs)+'/'+str(cyc)+'Z/'+str(fday)+'/'+str(savename)+'.png', bbox_inches='tight')
