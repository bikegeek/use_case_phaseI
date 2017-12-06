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
DATA_OUTimgs = os.environ['DATA_OUTimgs_model2obs']
DATA_OUTmodel = os.environ['DATA_OUTmodel_model2obs']
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
obs = os.environ['data_source']
climo = os.environ['climo']
#variable info
varname = os.environ['var_name_now']
varGRIBlvltyp = os.environ['var_GRIBlvltyp_now']
varlevel = os.environ['var_level_now']
#############################################################################
##### Plotting
#plot settings
pltcm_diff = plt.cm.coolwarm
if varname == "TCDC":
   levels = np.array([10,20,30,40,50,60,70,80,90])
   pltcm = plt.cm.Blues
   levels_diff = np.array([-60,-40,-30,-20,-10,-5,5,10,20,30,40,60])
   varunits='%'
   if varGRIBlvltyp == "200":
      vardes = "Total Cloud "
      savename = "TCDCclm"
   elif varGRIBlvltyp == "214":
      vardes = "Low Cloud "
      savename = "TCDClcl"
   elif varGRIBlvltyp == "224":
      vardes = "Middle Cloud "
      savename = "TCDCmcl"
   elif varGRIBlvltyp == "234":
      vardes = "High Cloud "
      savename = "TCDChcl"
elif varname == "DSWRF":
   levels = np.array([10,50,100,150,200,250,300,350])
   pltcm = plt.cm.RdYlBu_r
   levels_diff = np.array([-60,-40,-30,-20,-10,10,20,30,40,60])
   varunits = 'W 'r'$\mathregular{m^{-2}}$'''
   vardes = "Downwelling Surface SW "
   savename='DSWRFsfc'
elif varname == "USWRF":
   levels = np.array([10,40,80,120,160,200,240,280])
   pltcm = plt.cm.RdYlBu_r
   levels_diff = np.array([-60,-40,-30,-20,-10,10,20,30,40,60])
   varunits = 'W 'r'$\mathregular{m^{-2}}$'''
   if varGRIBlvltyp == "01":
      vardes = "Upwelling Surface SW "
      savename = "USWRFsfc"
   elif varGRIBlvltyp == "08":
      vardes = "Upwelling TOA SW "
      savename = "USWRFtoa"
elif varname == "DLWRF":
   levels = np.array([50,100,150,200,250,300,350,400])
   pltcm = plt.cm.RdYlBu_r
   levels_diff = np.array([-60,-40,-30,-20,-10,10,20,30,40,60])
   varunits = 'W 'r'$\mathregular{m^{-2}}$'''
   vardes = "Downwelling Surface LW "
   savename = "DLWRFsfc"
elif varname == "ULWRF":
   if varGRIBlvltyp == "01":
      levels = np.array([50,100,150,200,250,300,350,400])
      pltcm = plt.cm.RdYlBu_r
      levels_diff = np.array([-60,-40,-30,-20,-10,10,20,30,40,60])
      varunits = 'W 'r'$\mathregular{m^{-2}}$'''
      vardes = "Upwelling Surface LW "
      savename = "ULWRFsfc"
   elif varGRIBlvltyp == "08":
      levels = np.array([140,160,180,200,220,240,260,280,300])
      pltcm = plt.cm.RdYlBu_r
      levels_diff = np.array([-60,-40,-30,-20,-10,10,20,30,40,60])
      varunits = 'W 'r'$\mathregular{m^{-2}}$'''
      vardes = "Upwelling TOA LW "
      savename = "ULWRFtoa"
elif varname == "PWAT":
     levels = np.array([1,5,10,15,20,25,30,35,40,45,50,55,60,65])
     pltcm = plt.cm.GnBu
     levels_diff = np.array([-6,-4,-3,-2,-1,1,2,3,4,6])
     varunits = 'kg 'r'$\mathregular{m^{-2}}$'''
     vardes = "Column Water Vapor "
     savename = "PWATclm"
elif varname == "APCP":
     levels = np.array([0.1,0.5,1,2,3,4,5,6,7,8,9,10,12,15])
     pltcm = plt.cm.terrain_r
     levels_diff = np.array([-6,-4,-2,-1,-0.5,-0.1,0.1,0.5,1,2,4,6])
     varunits = 'mm 'r'$\mathregular{day^{-1}}$'''
     vardes = "Total Precip "
     savename = "APCPsfc"
elif varname == "ALBDO":
     levels = np.array([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9])
     pltcm = plt.cm.Pastel1_r
     levels_diff = np.array([-0.06,-0.04,-0.03,-0.02,-0.01,0.01,0.02,0.03,0.04,0.06])
     var_units = ' '
     vardes = "Surface SW Albedo "
     savename = "SWALBsfc"
elif varname == "TMP":
     levels = np.array([233,238,243,248,253,258,263,268,273,278,283,288,293,298,303,308,313])
     cmap = plt.cm.Spectral_r
     clevels_diff = np.array([-15,-10,-8,-6,-4,-2,-1,1,2,4,6,8,10,15])
     var_units = 'K'
     vardes = "2m Temperature "
     savename = "TMP2m"
elif varname == "CWAT":
     levels = np.array([0,10,30,50,70,90,110,130])
     pltcm = plt.cm.GnBu
     levels_diff = np.array([-70,-50,-30,-20,-10,10,20,30,50,70])
     varunits = 'g 'r'$\mathregular{m^{-2}}$'''
     vardes = "Column Water and Ice "
     savename = "CWATclm"
if climo == 'no':
     time_frq = "Mon. Mean"
else:
     time_frq = "Climo"
vardes, savename, levels, levels_diff, pltcm, varscale = pd.plot_settings(varname, varGRIBlvltyp, varlevel)
#plot data
if nexp == 1:
   fig = plt.figure(figsize=(10,12))
   gs = gridspec.GridSpec(2,1)
   gs.update(wspace=0.1, hspace=0.1)
elif nexp >= 2 and nexp < 4:
   fig = plt.figure(figsize=(15,10))
   gs = gridspec.GridSpec(2,2)
   gs.update(wspace=0.12, hspace=0.1)
elif nexp >= 4 and nexp < 6:
   fig = plt.figure(figsize=(18,10))
   gs = gridspec.GridSpec(2,3)
   gs.update(wspace=0.15, hspace=0.15)
elif nexp > 6:
   fig = plt.figure(figsize=(21,12))
   gs = gridspec.GridSpec(3,3)
   gs.update(wspace=0.15, hspace=0.05)
ax_obs = plt.subplot(gs[0])
nn = 1
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
   if nn == 1:
      m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,llcrnrlon=0,urcrnrlon=360,resolution='c', ax=ax_obs)
      m.drawcoastlines(linewidth=1.5, color='k', zorder=6)
      m.drawmapboundary
      x,y = np.meshgrid(lon_cyc, lat)
      xx,yy = m(x, y)
      m.drawmeridians(np.arange(0,361,60), labels=[False,False,False,True],fontsize=15)
      m.drawparallels(np.arange(-90,91,30), labels=[True,False,False,False],fontsize=15)
      CF = m.contourf(xx, yy, var_OBAR_cyc, levels=levels, cmap=pltcm, extend='both')
      C = m.contour(xx, yy, var_OBAR_cyc, levels=levels, colors='k', linewidths=1.0)
      ax_obs.clabel(C,levels, fmt='%g', inline=True, fontsize=12.5)
      ax_obs.set_title(str(obs)+' '+str(time_frq), loc='left', fontsize=18)
      ax_obs.set_title(round(area_average(np.ma.filled(var_OBAR),lat,lon,dlat),3), loc='right', fontsize=18)
   #plot difference 
   ax_fcst = plt.subplot(gs[nn])
   m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,llcrnrlon=0,urcrnrlon=360,resolution='c', ax=ax_fcst)
   m.drawcoastlines(linewidth=1.5, color='k', zorder=6)
   m.drawmapboundary
   x,y = np.meshgrid(lon_cyc,lat)
   xx,yy = m(x, y)
   m.drawmeridians(np.arange(0,361,60), labels=[False,False,False,True],fontsize=15)
   m.drawparallels(np.arange(-90,91,30), labels=[True,False,False,False],fontsize=15)
   CF = m.contourf(xx, yy, (var_FBAR_cyc - var_OBAR_cyc), levels=levels_diff, cmap=pltcm_diff, extend='both')
   if nn == nexp:
      cax = fig.add_axes([0.1, 0.05, 0.8, 0.05])
      fig.colorbar(CF, cax=cax, orientation='horizontal')
   ax_fcst.set_title(str(model_fcst_list[nn-1])+'-'+(obs)+' '+str(time_frq), loc='left', fontsize=18)
   ax_fcst.set_title(round(area_average(np.ma.filled((var_FBAR - var_OBAR)),lat,lon,dlat),3), loc='right', fontsize=18)
   nn += 1
plt.suptitle(str(vardes)+'\n'+str(cyc)+'Z-Cyc '+str(sday)+str(smonth)+str(syear)+'-'+str(eday)+str(emonth)+str(eyear)+' Mean\n('+str(fhr_list)+') Fcst-Hour Average', fontsize=18, fontweight='bold')
plt.savefig(str(DATA_OUTimgs)+'/'+str(cyc)+'Z/'+str(fday)+'/'+str(savename)+'obs_gb.png', bbox_inches='tight')
