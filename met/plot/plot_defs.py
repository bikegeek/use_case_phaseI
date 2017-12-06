import numpy as np
import matplotlib.pyplot as plt

__all__ = ['plot_settings', 'get_clevels']

def get_clevels(data):
   if np.abs(np.nanmin(data)) > np.nanmax(data):
      cmax = np.abs(np.nanmin(data))
      cmin = np.nanmin(data)
   else:
      cmax = np.nanmax(data)
      cmin = -1 * np.nanmax(data)
   if cmax > 1:
      cmin = round(cmin-1,0)
      cmax = round(cmax+1,0)
   else:
      cmin = round(cmin-0.1,1)
      cmax = round(cmax+0.1,1)
   clevels = np.linspace(cmin,cmax,11, endpoint=True)
   print(clevel)
   return clevels

def plot_settings(varname, varGRIBlvltyp, varlevel):
    if ((varname == '4LFTX') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #surface best lifted index
         vardes = 'Surface Best (4-Layer )Lifted Index (K)'
         savename = '4LFTXsfc'
         varscale = 1
         levels = np.array([-20,-15,-10,-8,-6,-4,-2,-1,1,2,4,6,8,10,15,20])
         pltcm = plt.cm.RdYlBu_r
         levels_diff = np.array([-3,-2,-1.5,-1,-0.5,-0.1,0.1,0.5,1,1.5,2,3])
    elif ((varname == 'ALBDO') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #surface albedo
         vardes = 'Surface Albedo (%)'
         savename = 'ALBDOsfc'
         varscale = 1
         levels = np.array([5,10,15,20,25,30,35,40,45,50])
         pltcm = plt.cm.Pastel1_r
         levels_diff = np.array([-3,-2,-1.5,-1,-0.5,-0.1,0.1,0.5,1,1.5,2,3])
    elif ((varname == 'APCP') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #surface convective precip
         vardes = 'Surface Total Precipitation (kg 'r'$\mathregular{m^{-2}}$'')'
         savename = 'APCPsfc'
         varscale = 1
         levels = np.array([0.1,0.2,0.4,0.6,0.8,1,1.5,2,2.5,3])
         pltcm = plt.cm.terrain_r
         levels_diff = np.array([-1.5,-1.2,-0.9,-0.6,-0.3,-0.1,0.1,0.3,0.6,0.9,1.2,1.5])
    elif ((varname == 'ACPCP') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #surface convective precip
         vardes = 'Surface Convective Precipitation (kg 'r'$\mathregular{m^{-2}}$'')'
         savename = 'ACPCPsfc'
         varscale = 1
         levels = np.array([0.1,0.2,0.4,0.6,0.8,1,1.5,2,2.5,3])
         pltcm = plt.cm.terrain_r
         levels_diff = np.array([-1.5,-1.2,-0.9,-0.6,-0.3,-0.1,0.1,0.3,0.6,0.9,1.2,1.5])
    elif ((varname == 'CAPE') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #surface CAPE
         vardes = 'Surface Convective Avail Potential Energy (J 'r'$\mathregular{kg^{-1}}$'')'
         savename = 'CAPEsfc'
         varscale = 1
         levels =  np.array([100,300,500,700,900,1000,1200,1300,1400,1500,1600,1700,1800])
         pltcm = plt.cm.pink_r
         levels_diff = np.array([-300,-200,-100,-50,-30,-10,10,30,50,100,200,300])
    elif ((varname == 'CAPE') and (varGRIBlvltyp == '116') and (varlevel == 'L255-0')): #255-0 hPa CAPE
         vardes = '255-0 hPa Above Ground Convective Avail Potential Energy (J 'r'$\mathregular{kg^{-1}}$'')'
         savename = 'CAPE255_0mb'
         varscale = 1
         levels =  np.array([100,300,500,700,900,1000,1200,1300,1400,1500,1600,1700,1800])
         pltcm = plt.cm.pink_r
         levels_diff = np.array([-300,-200,-100,-50,-30,-10,10,30,50,100,200,300])
    elif ((varname == 'CAPE') and (varGRIBlvltyp == '116') and (varlevel == 'L180-0')): #180-0 hPa CAPE
         vardes = '180-0 hPa Above Ground Convective Avail Potential Energy (J 'r'$\mathregular{kg^{-1}}$'')'
         savename = 'CAPE180_0mb'
         varscale = 1
         levels =  np.array([100,300,500,700,900,1000,1200,1300,1400,1500,1600,1700,1800])
         pltcm = plt.cm.pink_r
         levels_diff = np.array([-300,-200,-100,-50,-30,-10,10,30,50,100,200,300])
    elif ((varname == 'CFRZR') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #surface categorical freezing rain
         vardes = 'Surface Categorical Freezing Rain (yes=1;no=0)'
         savename = 'CFRZRsfc'
         varscale = 1
         levels = np.array([0.01,0.02,0.04,0.06,0.08,0.1,0.2,0.4,0.6,0.8,1]) 
         pltcm = plt.cm.Pastel1_r
         levels_diff = np.array([-1,-0.5,-0.1,-0.05,-0.01,-0.001,0.001,0.01,0.05,0.1,0.5,1])
    elif ((varname == 'CICEP') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #surface categorical ice pellets
         vardes = 'Surface Categorical Ice Pellets (yes=1;no=0)'
         savename = 'CICEPsfc'
         varscale = 1
         levels = np.array([0.01,0.02,0.04,0.06,0.08,0.1,0.2,0.4,0.6,0.8,1]) 
         pltcm = plt.cm.Pastel1_r
         levels_diff = np.array([-1,-0.5,-0.1,-0.05,-0.01,-0.001,0.001,0.01,0.05,0.1,0.5,1]) 
    elif ((varname == 'CIN') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #surface CIN
         vardes = 'Surface Convective Inhibition (J 'r'$\mathregular{kg^{-1}}$'')'
         savename = 'CINsfc'
         varscale = 1
         levels = np.array([-160,-140,-120,-100,-80,-60,-40,-20,-10,10,20,40,60,80])
         pltcm = plt.cm.PuOr
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'CIN') and (varGRIBlvltyp == '116') and (varlevel == 'L255-0')): #255-0 CIN
         vardes = '255-0 hPa Above Ground Convective Inhibition (J 'r'$\mathregular{kg^{-1}}$'')'
         savename = 'CIN255_0mb'
         varscale = 1
         levels = np.array([-100,-80,-60,-40,-20,-10,10,20,40,60,80,100])
         pltcm = plt.cm.PuOr
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'CIN') and (varGRIBlvltyp == '116') and (varlevel == 'L180-0')): #180-0 CIN
         vardes = '180-0 hPa Above Ground Convective Inhibition (J 'r'$\mathregular{kg^{-1}}$'')'
         savename = 'CIN180_0mb'
         varscale = 1
         levels = np.array([-100,-80,-60,-40,-20,-10,10,20,40,60,80,100])
         pltcm = plt.cm.PuOr
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'CPRAT') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #surface convective precip rate
         vardes = 'Surface Convective Precip Rate (mm 'r'$\mathregular{day^{-1}}$'')'
         savename = 'CPRATsfc'
         varscale = 24*3600
         levels = np.array([0.1,0.2,0.4,0.6,0.8,1,1.5,2,2.5,3]) 
         pltcm = plt.cm.terrain_r
         levels_diff = np.array([-6,-4,-2,-1,-0.5,-0.1,0.1,0.5,1,2,4,6])
    elif ((varname == 'CRAIN') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #surface categorical rain
         vardes = 'Surface Categorical Rain (yes=1;no=0)'
         savename = 'CRAINsfc'
         varscale = 1
         levels = np.array([0.01,0.02,0.04,0.06,0.08,0.1,0.2,0.4,0.6,0.8,1]) 
         pltcm = plt.cm.Pastel1_r
         levels_diff = np.array([-1,-0.5,-0.1,-0.05,-0.01,-0.001,0.001,0.01,0.05,0.1,0.5,1])
    elif ((varname == 'CSNOW') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #surface categorical snow
         vardes = 'Surface Categorical Snow (yes=1;no=0)'
         savename = 'CSNOWsfc'
         varscale = 1
         levels = np.array([0.01,0.02,0.04,0.06,0.08,0.1,0.2,0.4,0.6,0.8,1]) 
         pltcm = plt.cm.Pastel1_r
         levels_diff = np.array([-1,-0.5,-0.1,-0.05,-0.01,-0.001,0.001,0.01,0.05,0.1,0.5,1])
    elif ((varname == 'CWAT') and (varGRIBlvltyp == '200') and (varlevel == 'L0')): #cloud water
         vardes = 'Atmos Column Cloud Water (g 'r'$\mathregular{m^{-2}}$'')'
         savename = 'CWATclm'
         varscale = 1000
         levels = np.array([20,40,60,80,100,120,140,160,180,200])
         pltcm = plt.cm.Blues
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'CWORK') and (varGRIBlvltyp == '200') and (varlevel == 'L0')): #cloud work
         vardes = 'Atmos Column Cloud Work Function (J 'r'$\mathregular{kg^{-1}}$'')'
         savename = 'CWORKclm'
         varscale = 1
         levels = np.array([10,20,40,60,80,100,120,140,160,180]) 
         pltcm = plt.cm.Blues
         levels_diff = np.array([-30,-25,-20,-15,-10,-5,5,10,15,20,25,30])
    elif ((varname == 'DPT') and (varGRIBlvltyp == '105') and (varlevel == 'Z2')): #2m dewpoint
         vardes = '2m Above Ground Dewpoint Temperature (K)'
         savename = 'DPT2m'
         varscale = 1
         levels = np.array([240,245,250,255,260,265,270,275,280,285,290,295,300]) 
         pltcm = plt.cm.BrBG
         levels_diff = np.array([-5,-4,-3,-2,-1,-0.5,0.5,1,2,3,4,5])
    elif ((varname == 'DLWRF') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #downwelling longwave sfc
         vardes = 'Surface Downward Longwave Flux (W 'r'$\mathregular{m^{-2}}$'')'
         savename = 'DLWRFsfc'
         varscale = 1
         levels = np.array([5,10,50,100,150,200,250,300,350,400,450,500])
         pltcm = plt.cm.RdYlBu_r
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'DSWRF') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #downwelling shortwave sfc
         vardes = 'Surface Downward Shortwave Flux (W 'r'$\mathregular{m^{-2}}$'')'
         savename = 'DSWRFsfc'
         varscale = 1
         levels = np.array([5,10,50,100,150,200,250,300,350,400,450,500])
         pltcm = plt.cm.RdYlBu_r
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'FLDCP') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #surface field capacity
         vardes = 'Surface Field Capacity (fraction)'
         savename = 'FLDCPsfc'
         varscale = 1
         levels = np.array([0.01,0.01,0.02,0.04,0.06,0.08,0.1,0.2,0.4,0.6,0.8,1])
         pltcm = plt.cm.summer_r
         levels_diff = np.array([-1,-0.5,-0.1,-0.05,-0.01,-0.001,0.001,0.01,0.05,0.1,0.5,1])
    elif ((varname == 'GUST') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #surface wind gust
         vardes = 'Surface Wind Gust (m 'r'$\mathregular{s^{-1}}$'')'
         savename = 'GUSTsfc'
         varscale = 1
         levels = np.array([0.5,1,2,4,6,8,10,12,14,16,18,20]) 
         pltcm = plt.cm.RdPu
         levels_diff = np.array([-3,-2,-1,-0.5,-0.2,0.2,0.5,1,2,3])
    elif ((varname == 'GFLUX') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #ground flux
         vardes = 'Surface Ground Heat Flux (W 'r'$\mathregular{m^{-2}}$'')'
         savename = 'GFLUXsfc'
         varscale = 1
         levels = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
         pltcm = plt.cm.RdYlGn
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'HGT') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #surface height
         vardes = 'Surface Geopotential Height (gpm)'
         savename = 'HGTsfc'
         varscale = 1
         levels = np.array([100,500,1000,1500,2000,2500,3000,3500,4000,4500,5000,6000,7000,8000]) 
         pltcm = plt.cm.coolwarm
         levels_diff = np.array([-400,-200,-100,-50,-20,-10,10,20,50,100,200,400])  
    elif ((varname == 'HGT') and (varGRIBlvltyp == '204') and (varlevel == 'L0')): #highest trop. freezing level height
         vardes = 'Highest Trop Freezing Level Geopotential Height (gpm)'
         savename = 'HGThftl'
         varscale = 1
         levels = np.array([100,500,1000,1500,2000,2500,3000,3500,4000,4500,5000,6000,7000,8000])
         pltcm = plt.cm.coolwarm
         levels_diff = np.array([-400,-200,-100,-50,-20,-10,10,20,50,100,200,400])  
    elif ((varname == 'HGT') and (varGRIBlvltyp == '07') and (varlevel == 'L0')): #tropopause geopotential height
         vardes = 'Tropopause Geopotential Height (km)'
         savename = 'HGTtrp'
         varscale = 0.001
         levels = np.array([1,2,3,4,5,6,7,8,9,10,12,14,16,18])
         pltcm = plt.cm.coolwarm
         levels_diff = np.array([-1,-0.8,-0.6,-0.4,-0.2,-0.1,0.1,0.2,0.4,0.6,0.8,1.0])
    elif ((varname == 'HGT') and (varGRIBlvltyp == '06') and (varlevel == 'L0')): #max wind level geopotential height
         vardes = 'Max Wind Level Geopotential Height (km)'
         savename = 'HGTmwl'
         varscale = 0.001
         levels = np.array([1,2,3,4,5,6,7,8,9,10,12,14,16,18])
         pltcm = plt.cm.coolwarm
         levels_diff = np.array([-1,-0.8,-0.6,-0.4,-0.2,-0.1,0.1,0.2,0.4,0.6,0.8,1.0])
    elif ((varname == 'HGT') and (varGRIBlvltyp == '04') and (varlevel == 'L0')): #0C isotherm level geopotential height
         vardes = '0C Isotherm Level Geopotential Height (gpm)'
         savename = 'HGT0C'
         varscale = 1
         levels = np.array([100,500,1000,1500,2000,2500,3000,3500,4000,4500,5000,6000,7000,8000])
         pltcm = plt.cm.coolwarm
         levels_diff = np.array([-400,-200,-100,-50,-20,-10,10,20,50,100,200,400]) 
    elif ((varname == 'HINDEX') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #surface Haines index
         vardes = 'Surface Haines Index'
         savename = 'HINDEXsfc'
         varscale = 1
         levels = np.array([1,2,3,4,5,6,7,8,9])
         pltcm = plt.cm.Spectral_r
         levels_diff = np.array([-3,-2,-1,-0.5,-0.1,-0.01,0.01,0.1,0.5,1,2,3])
    elif ((varname == 'HLCY') and (varGRIBlvltyp == '106') and (varlevel == 'Z30_0')): #0-3000m AGL storm relative helicity
         vardes = '0-3000m Above Ground Storm Relative Helicity ('r'$\mathregular{m^{2}}$'' 'r'$\mathregular{s^{-2}}$'')'
         savename = 'HLCY0_3000m'
         varscale = 1
         levels = np.array([300,400,500,600,700,800,900,1000,1100,1200,1400,1600,1800])
         pltcm = plt.cm.Spectral_r
         levels_diff = np.array([-400,-200,-100,-50,-20,-10,10,20,50,100,200,400]) 
    elif ((varname == 'HPBL') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #PBL height
         vardes = 'Planetary Boundary Layer Height (m)'
         savename = 'HPBLsfc'
         varscale = 1
         levels = np.array([300,400,500,600,700,800,900,1000,1100,1200,1400,1600,1800]) 
         pltcm = plt.cm.coolwarm
         levels_diff = np.array([-600,-400,-200,-100,-50,-20,20,50,100,200,400,600])
    elif ((varname == 'ICAHT') and (varGRIBlvltyp == '07') and (varlevel == 'L0')): #ICAO std. atmos. tropopause
         vardes = 'Tropopause ICAO Standard Atmosphere Reference Height (km)'
         savename = 'ICAHTtrp'
         varscale = 0.001
         levels = np.array([1,2,3,4,5,6,7,8,9,10,12,14,16,18])
         pltcm = plt.cm.Spectral_r
         levels_diff = np.array([-1,-0.8,-0.6,-0.4,-0.2,-0.1,0.1,0.2,0.4,0.6,0.8,1.0])
    elif ((varname == 'ICAHT') and (varGRIBlvltyp == '06') and (varlevel == 'L0')): #ICAO std. atmos. max wind level
         vardes = 'Max Wind Level ICAO Standard Atmosphere Reference Height (km)'
         savename = 'ICAHTmwl'
         varscale = 0.001
         levels = np.array([1,2,3,4,5,6,7,8,9,10,12,14,16,18])
         pltcm = plt.cm.Spectral_r
         levels_diff = np.array([-1,-0.8,-0.6,-0.4,-0.2,-0.1,0.1,0.2,0.4,0.6,0.8,1.0])
    elif ((varname == 'ICEC') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #ice concentration
         vardes = 'Surface Ice Concentration (ice=1;no ice=0) (fraction)'
         savename = 'ICECsfc'
         varscale = 1
         levels = np.array([0.01,0.02,0.04,0.06,0.08,0.1,0.2,0.4,0.6,0.8,1])
         pltcm = plt.cm.winter_r
         levels_diff = np.array([-1,-0.5,-0.1,-0.05,-0.01,-0.001,0.001,0.01,0.05,0.1,0.5,1])
    elif ((varname == 'LAND') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #land cover
         vardes = 'Surface Land Cover (ice=1;no ice=0) (fraction)'
         savename = 'LANDsfc'
         varscale = 1
         levels = np.array([0.001,0.01,0.02,0.04,0.06,0.08,0.1,0.2,0.4,0.6,0.8,1]) 
         pltcm = plt.cm.terrain
         levels_diff = np.array([-1,-0.5,-0.1,-0.05,-0.01,-0.001,0.001,0.01,0.05,0.1,0.5,1]) 
    elif ((varname == 'LFTX') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #surface lifted index
         vardes = 'Surface Lifted Index (K)'
         savename = 'LFTXsfc'
         varscale = 1
         levels = np.array([-20,-15,-10,-8,-6,-4,-2,-1,1,2,4,6,8,10,15,20]) 
         pltcm = plt.cm.RdYlBu_r
         levels_diff = np.array([-3,-2,-1.5,-1,-0.5,-0.1,0.1,0.5,1,1.5,2,3])
    elif ((varname == 'LHTFL') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #latent heat flux
         vardes = 'Surface Latent Heat Flux (W 'r'$\mathregular{m^{-2}}$'')'
         savename = 'LHTFLsfc'
         varscale = 1
         levels = np.array([5,10,20,40,60,80,100,120,140,160,180,200])
         pltcm = plt.cm.RdYlGn
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'MSLET') and (varGRIBlvltyp == '102') and (varlevel == 'L0')): #membrane mean sea level pressure
         vardes = 'Membrane Mean Sea Level Pressure (hPa)'
         savename = 'MSLETmsl'
         varscale = 0.01
         levels = np.array([960,965,970,975,980,985,990,995,1000,1005,1010,1015,1020]) 
         pltcm = plt.cm.Spectral_r
         levels_diff = np.array([-10,-5,-4,-3,-2,-1,1,2,3,4,5,10])
    elif ((varname == 'PEVPR') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #surface pot. evap. rate
         vardes = 'Surface Potential Evaporation Rate (W 'r'$\mathregular{m^{-2}}$'')'
         savename = 'PEVPRsfc'
         varscale = 1
         levels = np.array([5,10,50,100,150,200,250,300,350,400,450,500])
         pltcm = plt.cm.YlOrBr
         levels_diff = np.array([-50,-30,-20,-15,-10,-5,5,10,15,20,30,50])
    elif ((varname == 'PLPL') and (varGRIBlvltyp == '116') and (varlevel == 'L255-0')): #250-0 hPa level parcel lifted
         vardes = '255-0hPa Above Ground Pressure from Which Parcel Was Lifted (hPa)'
         savename = 'PLPL255_0mb'
         varscale = 0.01
         levels = np.array([400,500,550,600,650,700,750,800,850,900,950,1000,1010])
         pltcm = plt.cm.Spectral_r
         levels_diff = np.array([-20,-15,-10,-5,-2,-1,1,2,5,10,15,20])
    elif ((varname == 'POT') and (varGRIBlvltyp == '107') and (varlevel == 'L9950')): #.995 sigma potential temp
         vardes = 'Sigma=.995 Potential Temperature (K)'
         savename = 'POTsig995'
         varscale = 1
         levels = np.array([240,245,250,255,260,265,270,275,280,285,290,295,300])
         pltcm = plt.cm.Spectral_r
         levels_diff = np.array([-5,-3,-2,-1,-0.5,-0.1,0.1,0.5,1,2,3,5]) 
    elif ((varname == 'PRATE') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #surface precip rate
         vardes = 'Surface Precipitation Rate (mm 'r'$\mathregular{day^{-1}}$'')'
         savename = 'PRATEsfc'
         varscale = 24*3600
         levels = np.array([0.1,0.2,0.4,0.6,0.8,1,1.5,2,2.5,3])
         pltcm = plt.cm.terrain_r
         levels_diff = np.array([-3,-2,-1.5,-1,-0.5,-0.1,0.1,0.5,1,1.5,2,3])
    elif ((varname == 'PRES') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #surface pressure
         vardes = 'Surface Pressure (hPa)'
         savename = 'PRESsfc'
         varscale = 0.01
         levels = np.array([400,500,550,600,650,700,750,800,850,900,950,1000,1010]) 
         pltcm = plt.cm.Spectral_r
         levels_diff = np.array([-10,-5,-4,-3,-2,-1,1,2,3,4,5,10])
    elif ((varname == 'PRES') and (varGRIBlvltyp == '105') and (varlevel == 'Z80')): #80m AGL pressure
         vardes = '80m Above Ground Pressure (hPa)'
         savename = 'PRES80m'
         varscale = 0.01
         levels = np.array([960,965,970,975,980,985,990,995,1000,1005,1010,1015,1020])
         pltcm = plt.cm.Spectral_r
         levels_diff = np.array([-20,-15,-10,-5,-2,-1,1,2,5,10,15,20])
    elif ((varname == 'PRES') and (varGRIBlvltyp == '212') and (varlevel == 'L0')): #low cloud base pressure
         vardes = 'Low Cloud Base Pressure (hPa)'
         savename = 'PRESlcb'
         varscale = 0.01
         levels = np.array([780,800,820,840,860,880,900,920,940,960,980,1000,1020])
         pltcm = plt.cm.Spectral_r
         levels_diff = np.array([-20,-15,-10,-5,-2,-1,1,2,5,10,15,20])
    elif ((varname == 'PRES') and (varGRIBlvltyp == '222') and (varlevel == 'L0')): #mid cloud base pressure
         vardes = 'Mid Cloud Base Pressure (hPa)'
         savename = 'PRESmcb'
         varscale = 0.01
         levels = np.array([460,480,500,520,540,560,580,600,620,640,660,680,700])
         pltcm = plt.cm.Spectral_r
         levels_diff = np.array([-20,-15,-10,-5,-2,-1,1,2,5,10,15,20])
    elif ((varname == 'PRES') and (varGRIBlvltyp == '232') and (varlevel == 'L0')): #high cloud base pressure
         vardes = 'High Cloud Base Pressure (hPa)'
         savename = 'PREShcb'
         varscale = 0.01
         levels = np.array([180,200,220,240,260,280,300,320,340,360,380,400,420])
         pltcm = plt.cm.Spectral_r
         levels_diff = np.array([-20,-15,-10,-5,-2,-1,1,2,5,10,15,20])
    elif ((varname == 'PRES') and (varGRIBlvltyp == '242') and (varlevel == 'L0')): #convective cloud base pressure
         vardes = 'Convective Cloud Base Pressure (hPa)'
         savename = 'PREScvb'
         varscale = 0.01
         levels = np.array([780,800,820,840,860,880,900,920,940,960,980,1000,1020])
         pltcm = plt.cm.Spectral_r
         levels_diff = np.array([-20,-15,-10,-5,-2,-1,1,2,5,10,15,20])
    elif ((varname == 'PRES') and (varGRIBlvltyp == '213') and (varlevel == 'L0')): #low cloud top pressure
         vardes = 'Low Cloud Top Pressure (hPa)'
         savename = 'PRESlct'
         varscale = 0.01
         levels = np.array([600,620,640,660,680,700,720,740,760,780,800,820,840])
         pltcm = plt.cm.Spectral_r
         levels_diff = np.array([-20,-15,-10,-5,-2,-1,1,2,5,10,15,20])
    elif ((varname == 'PRES') and (varGRIBlvltyp == '223') and (varlevel == 'L0')): #mid cloud top pressure
         vardes = 'Mid Cloud Top Pressure (hPa)'
         savename = 'PRESmct'
         varscale = 0.01
         levels = np.array([300,320,340,360,380,400,420,440,460,480,500,520,540])
         pltcm = plt.cm.Spectral_r
         levels_diff = np.array([-20,-15,-10,-5,-2,-1,1,2,5,10,15,20])
    elif ((varname == 'PRES') and (varGRIBlvltyp == '233') and (varlevel == 'L0')): #high cloud top pressure
         vardes = 'High Cloud Top Pressure (hPa)'
         savename = 'PREShct'
         varscale = 0.01
         levels = np.array([80,100,120,140,160,180,200,220,240,260,280,300,320])
         pltcm = plt.cm.Spectral_r
         levels_diff = np.array([-20,-15,-10,-5,-2,-1,1,2,5,10,15,20])
    elif ((varname == 'PRES') and (varGRIBlvltyp == '243') and (varlevel == 'L0')): #convective cloud top pressure
         vardes = 'Convective Cloud Top Pressure (hPa)'
         savename = 'PREScvt'
         varscale = 0.01
         levels = np.array([150,200,250,300,350,400,450,500,550,600,650,700,800,850])
         pltcm = plt.cm.Spectral_r
         levels_diff = np.array([-20,-15,-10,-5,-2,-1,1,2,5,10,15,20])
    elif ((varname == 'PRES') and (varGRIBlvltyp == '07') and (varlevel == 'L0')): #topopause pressure
         vardes = 'Tropopause Pressure (hPa)'
         savename = 'PREStrp'
         varscale = 0.01
         levels = np.array([100,120,140,160,180,200,220,240,260,280,300])
         pltcm = plt.cm.Spectral_r
         levels_diff = np.array([-20,-15,-10,-5,-2,-1,1,2,5,10,15,20])
    elif ((varname == 'PRES') and (varGRIBlvltyp == '06') and (varlevel == 'L0')): #max wind level pressure
         vardes = 'Max Wind Level Pressure (hPa)'
         savename = 'PRESmwl'
         varscale = 0.01
         levels = np.array([10,50,100,120,140,160,180,200,220,240,260,280,300])
         pltcm = plt.cm.Spectral_r
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'PRMSL') and (varGRIBlvltyp == '102') and (varlevel == 'L0')): #mean sea level pressure
         vardes = 'Mean Sea Level Pressure (hPa)'
         savename = 'PRMSLmsl'
         varscale = 0.01
         levels = np.array([960,965,970,975,980,985,990,995,1000,1005,1010,1015,1020]) 
         pltcm = plt.cm.Spectral_r
         levels_diff = np.array([-10,-5,-4,-3,-2,-1,1,2,3,4,5,10])
    elif ((varname == 'PWAT') and (varGRIBlvltyp == '200') and (varlevel == 'L0')): #precipitable water
         vardes = 'Atmos Column Precipitable Water (kg 'r'$\mathregular{m^{-2}}$'')'
         savename = 'PWATclm'
         varscale = 1
         levels = np.array([5,10,15,20,25,30,35,40,45,50])
         pltcm = plt.cm.GnBu
         levels_diff = np.array([-10,-5,-4,-3,-2,-1,1,2,3,4,5,10])
    elif ((varname == 'RH') and (varGRIBlvltyp == '105') and (varlevel == 'Z2')): #2m relative humidity
         vardes = '2m Above Ground Relative Humidity (%)'
         savename = 'RH2m'
         varscale = 1
         levels = np.array([10,20,30,40,50,60,70,80,90,100]) 
         pltcm = plt.cm.GnBu
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'RH') and (varGRIBlvltyp == '107') and (varlevel == 'L9950')): #.995 sigma relative humidity
         vardes = 'Sigma=.995 Relative Humidity (%)'
         savename = 'RHsig995'
         varscale = 1
         levels = np.array([10,20,30,40,50,60,70,80,90,100])
         pltcm = plt.cm.GnBu
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'RH') and (varGRIBlvltyp == '200') and (varlevel == 'L0')): #atmos column relative humidity
         vardes = 'Atmos Column Relative Humidity (%)'
         savename = 'RHclm'
         varscale = 1
         levels = np.array([10,20,30,40,50,60,70,80,90,100])
         pltcm = plt.cm.GnBu
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'RH') and (varGRIBlvltyp == '204') and (varlevel == 'L0')): #highest freezing level relative humidity
         vardes = 'Highest Trop Freezing Level Relative Humidity (%)'
         savename = 'RHhtfl'
         varscale = 1
         levels = np.array([10,20,30,40,50,60,70,80,90,100])
         pltcm = plt.cm.GnBu
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'RH') and (varGRIBlvltyp == '04') and (varlevel == 'L0')): #0C isotherm level relative humidity
         vardes = '0C Isotherm Level Relative Humidity (%)'
         savename = 'RH0C'
         varscale = 1
         levels = np.array([10,20,30,40,50,60,70,80,90,100])
         pltcm = plt.cm.GnBu
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'SHTFL') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #sensible heat flux
         vardes = 'Surface Sensible Heat Flux (W 'r'$\mathregular{m^{-2}}$'')'
         savename = 'SHTFLsfc'
         varscale = 1
         levels = np.array([5,10,20,40,60,80,100,120,140,160,180,200])
         pltcm = plt.cm.RdYlGn
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'SNOD') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #surface snow depth
         vardes = 'Surface Snow Depth (cm)'
         savename = 'SNODsfc'
         varscale = 100
         levels = np.array([1,5,10,20,40,60,80,100,150,200,250])
         pltcm = plt.cm.winter_r
         levels_diff = np.array([-40,-20,-10,-5,-1,-0.1,0.1,1,5,10,20,40])
    elif ((varname == 'SPFH') and (varGRIBlvltyp == '105') and (varlevel == 'Z2')): #2m specific humidity
         vardes = '2m Above Ground Specific Humidity (g 'r'$\mathregular{kg^{-1}}$'')'
         savename = 'SPFH2m'
         varscale = 1000
         levels = np.array([1,2,4,6,8,10,12,14,16,18]) 
         pltcm = plt.cm.PuBuGn
         levels_diff = np.array([-3,-2,-1,-0.6,-0.3,-0.1,0.1,0.3,0.6,1,2,3])
    elif ((varname == 'SPFH') and (varGRIBlvltyp == '105') and (varlevel == 'Z80')): #80m specific humidity
         vardes = '80m Above Ground Specific Humidity (g 'r'$\mathregular{kg^{-1}}$'')'
         savename = 'SPFH80m'
         varscale = 1000
         levels = np.array([1,2,4,6,8,10,12,14,16,18])
         pltcm = plt.cm.PuBuGn
         levels_diff = np.array([-3,-2,-1,-0.6,-0.3,-0.1,0.1,0.3,0.6,1,2,3])
    elif ((varname == 'SUNSD') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #sunshine duration
         vardes = 'Surface Sunshine Duration (hour)'
         savename = 'SUNSDsfc'
         varscale = 0.00027778
         levels = np.array([0.01,0.05,0.1,0.5,1,2,3,4,5,6])
         pltcm = plt.cm.YlOrBr
         levels_diff = np.array([-2,-1,-0.5,-0.1,-0.01,-0.001,0.001,0.01,0.1,0.5,1,2])
    elif ((varname == 'SOILW') and (varGRIBlvltyp == '112') and (varlevel == 'Z0-10')): #0-10cm underground volumetric soil mositure
         vardes = '0-10cm Underground Volumetric Soil Moisture (fraction)'
         savename = 'SOILW0_10cm'
         varscale = 100
         levels = np.array([10,20,30,40,50,60,70,80,90,100])
         pltcm = plt.cm.RdYlGn
         levels_diff = np.array([-20,-15,-10,-5,-3,-1,1,3,5,10,15,20])
    elif ((varname == 'SOILW') and (varGRIBlvltyp == '112') and (varlevel == 'Z10-40')): #10-40cm underground volumetric soil mositure
         vardes = '10-40cm Underground Volumetric Soil Moisture (fraction)'
         savename = 'SOILW10_40cm'
         varscale = 100
         levels = np.array([10,20,30,40,50,60,70,80,90,100])
         pltcm = plt.cm.RdYlGn
         levels_diff = np.array([-20,-15,-10,-5,-3,-1,1,3,5,10,15,20])
    elif ((varname == 'SOILW') and (varGRIBlvltyp == '112') and (varlevel == 'Z40-100')): #40-100cm underground volumetric soil mositure
         vardes = '40-100cm Underground Volumetric Soil Moisture (fraction)'
         savename = 'SOILW40_100cm'
         varscale = 100
         levels = np.array([10,20,30,40,50,60,70,80,90,100])
         pltcm = plt.cm.RdYlGn
         levels_diff = np.array([-20,-15,-10,-5,-3,-1,1,3,5,10,15,20])
    elif ((varname == 'SOILW') and (varGRIBlvltyp == '112') and (varlevel == 'Z100-200')): #100-200m underground volumetric soil mositure
         vardes = '100-200cm Underground Volumetric Soil Moisture (fraction)'
         savename = 'SOILW100_200cm'
         varscale = 100
         levels = np.array([10,20,30,40,50,60,70,80,90,100])
         pltcm = plt.cm.RdYlGn
         levels_diff = np.array([-20,-15,-10,-5,-3,-1,1,3,5,10,15,20])
    elif ((varname == 'TCDC') and (varGRIBlvltyp == '200') and (varlevel == 'L0')): #total cloud fraction
         vardes = 'Atmos Column Total Cloud Cover (%)'
         savename = 'TCDCclm'
         varscale = 1
         levels = np.array([0,10,20,30,40,50,60,80,100])
         pltcm = plt.cm.Blues
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'TCDC') and (varGRIBlvltyp == '211') and (varlevel == 'L0')): #pbl cloud fraction
         vardes = 'Boundary Layer Total Cloud Cover (%)'
         savename = 'TCDCbcl'
         varscale = 1
         levels = np.array([0,10,20,30,40,50,60,80,100])
         pltcm = plt.cm.Blues
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30]) 
    elif ((varname == 'TCDC') and (varGRIBlvltyp == '214') and (varlevel == 'L0')): #low cloud fraction
         vardes = 'Low Level Total Cloud Cover (%)'
         savename = 'TCDClcl'
         varscale = 1
         levels = np.array([0,10,20,30,40,50,60,80,100])
         pltcm = plt.cm.Blues
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'TCDC') and (varGRIBlvltyp == '224') and (varlevel == 'L0')): #mid cloud fraction
         vardes = 'Mid Level Total Cloud Cover (%)'
         savename = 'TCDCmcl'
         varscale = 1
         levels = np.array([0,10,20,30,40,50,60,80,100])
         pltcm = plt.cm.Blues
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'TCDC') and (varGRIBlvltyp == '234') and (varlevel == 'L0')): #high cloud fraction
         vardes = 'High Level Total Cloud Cover (%)'
         savename = 'TCDChcl'
         varscale = 1
         levels = np.array([0,10,20,30,40,50,60,80,100])
         pltcm = plt.cm.Blues
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'TCDC') and (varGRIBlvltyp == '244') and (varlevel == 'L0')): #convective cloud fraction
         vardes = 'Convective Total Cloud Cover (%)'
         savename = 'TCDCcvl'
         varscale = 1
         levels = np.array([0,10,20,30,40,50,60,80,100])
         pltcm = plt.cm.Blues
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'TMAX') and (varGRIBlvltyp == '105') and (varlevel == 'Z2')): #2m max temp
         vardes = '2m Above Ground Maximum Temperature (K)'
         savename = 'TMAX2msfc'
         varscale = 1
         levels = np.array([240,245,250,255,260,265,270,275,280,285,290,295,300])
         pltcm = plt.cm.RdYlBu_r
         levels_diff = np.array([-5,-4,-3,-2,-1,-0.5,-0.1,0.1,0.5,1,2,3,4,5])
    elif ((varname == 'TMIN') and (varGRIBlvltyp == '105') and (varlevel == 'Z2')): #2m min temp
         vardes = '2m Above Ground Minimum Temperature (K)'
         savename = 'TMIN2msfc'
         varscale = 1
         levels = np.array([240,245,250,255,260,265,270,275,280,285,290,295,300])
         pltcm = plt.cm.RdYlBu_r
         levels_diff = np.array([-5,-4,-3,-2,-1,-0.5,-0.1,0.1,0.5,1,2,3,4,5])
    elif ((varname == 'TMP') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #skin temp
         vardes = 'Surface Skin Temperature (K)'
         savename = 'TMPsfc'
         varscale = 1
         levels = np.array([240,245,250,255,260,265,270,275,280,285,290,295,300])
         pltcm = plt.cm.RdYlBu_r
         levels_diff = np.array([-5,-4,-3,-2,-1,-0.5,-0.1,0.1,0.5,1,2,3,4,5]) 
    elif ((varname == 'TMP') and (varGRIBlvltyp == '105') and (varlevel == 'Z2')): #2m temp
         vardes = '2m Above Ground Temperature (K)'
         savename = 'TMP2m'
         varscale = 1
         levels = np.array([240,245,250,255,260,265,270,275,280,285,290,295,300])
         pltcm = plt.cm.RdYlBu_r
         levels_diff = np.array([-5,-4,-3,-2,-1,-0.5,-0.1,0.1,0.5,1,2,3,4,5])
    elif ((varname == 'TMP') and (varGRIBlvltyp == '213') and (varlevel == 'L0')): #low cloud top temp
         vardes = 'Low Cloud Top Temperature (K)'
         savename = 'TMPlct'
         varscale = 1
         levels = np.array([220,225,230,235,240,245,250,255,260,265,270,275,280])
         pltcm = plt.cm.RdYlBu_r
         levels_diff = np.array([-5,-3,-2,-1,-0.5,-0.1,0.1,0.5,1,2,3,5])
    elif ((varname == 'TMP') and (varGRIBlvltyp == '223') and (varlevel == 'L0')): #mid cloud top temp
         vardes = 'Mid Cloud Top Temperature (K)'
         savename = 'TMPmct'
         varscale = 1
         levels = np.array([200,205,210,215,220,225,230,235,240,245,250,255,260])
         pltcm = plt.cm.RdYlBu_r
         levels_diff = np.array([-5,-3,-2,-1,-0.5,-0.1,0.1,0.5,1,2,3,5])
    elif ((varname == 'TMP') and (varGRIBlvltyp == '233') and (varlevel == 'L0')): #high cloud top temp
         vardes = 'High Cloud Top Temperature (K)'
         savename = 'TMPhct'
         varscale = 1
         levels = np.array([180,185,190,195,200,205,210,215,220,225,230,235,240])
         pltcm = plt.cm.RdYlBu_r
         levels_diff = np.array([-5,-3,-2,-1,-0.5,-0.1,0.1,0.5,1,2,3,5])
    elif ((varname == 'TMP') and (varGRIBlvltyp == '07') and (varlevel == 'L0')): #topopause temp
         vardes = 'Tropopause Temperature (K)'
         savename = 'TMPtrp'
         varscale = 1
         levels = np.array([160,180,185,190,195,200,205,210,215,220,225,230,235,240])
         pltcm = plt.cm.RdYlBu_r
         levels_diff = np.array([-5,-3,-2,-1,-0.5,-0.1,0.1,0.5,1,2,3,5])
    elif ((varname == 'TMP') and (varGRIBlvltyp == '107') and (varlevel == 'L9950')): #sigma=.995 temperature
         vardes = 'Sigma=.995 Temperature (K)'
         savename = 'TMPsig995'
         varscale = 1
         levels = np.array([240,245,250,255,260,265,270,275,280,285,290,295,300])
         pltcm = plt.cm.RdYlBu_r
         levels_diff = np.array([-5,-3,-2,-1,-0.5,-0.1,0.1,0.5,1,2,3,5])
    elif ((varname == 'TMP') and (varGRIBlvltyp == '06') and (varlevel == 'L0')): #temperature max wind level
         vardes = 'Max Wind Level Temperature (K)'
         savename = 'TMPmwl'
         varscale = 1
         levels = np.array([160,180,185,190,195,200,205,210,215,220,225,230,235,240])
         pltcm = plt.cm.RdYlBu_r
         levels_diff = np.array([-5,-3,-2,-1,-0.5,-0.1,0.1,0.5,1,2,3,5])
    elif ((varname == 'TOZNE') and (varGRIBlvltyp == '200') and (varlevel == 'L0')): #col ozone
         vardes = 'Atmos Column Total Ozone (Dobson)'
         savename = 'TOZNEclm'
         varscale = 1
         levels = np.array([160,180,200,220,240,260,280,300,320,340,360,380]) 
         pltcm = plt.cm.RdYlGn
         levels_diff = np.array([-10,-5,-4,-3,-2,-1,1,2,3,4,5,10])
    elif ((varname == 'TSOIL') and (varGRIBlvltyp == '112') and (varlevel == 'Z0-10')): #0-10cm underground soil temp
         vardes = '0-10cm Underground Soil Temperature (K)'
         savename = 'TSOIL0_10cm'
         varscale = 1
         levels = np.array([240,245,250,255,260,265,270,275,280,285,290,295,300])
         pltcm = plt.cm.RdYlBu_r
         levels_diff = np.array([-5,-3,-2,-1,-0.5,-0.1,0.1,0.5,1,2,3,5])
    elif ((varname == 'TSOIL') and (varGRIBlvltyp == '112') and (varlevel == 'Z10-40')): #10-40cm underground soil temp
         vardes = '10-40cm Underground Soil Temperature (K)'
         savename = 'TSOIL10_40cm'
         varscale = 1
         levels = np.array([240,245,250,255,260,265,270,275,280,285,290,295,300])
         pltcm = plt.cm.RdYlBu_r
         levels_diff = np.array([-5,-3,-2,-1,-0.5,-0.1,0.1,0.5,1,2,3,5])
    elif ((varname == 'TSOIL') and (varGRIBlvltyp == '112') and (varlevel == 'Z40-100')): #40-100cm underground soil temp
         vardes = '40-100cm Underground Soil Temperature (K)'
         savename = 'TSOIL40_100cm'
         varscale = 1
         levels = np.array([240,245,250,255,260,265,270,275,280,285,290,295,300])
         pltcm = plt.cm.RdYlBu_r
         levels_diff = np.array([-5,-3,-2,-1,-0.5,-0.1,0.1,0.5,1,2,3,5])
    elif ((varname == 'TSOIL') and (varGRIBlvltyp == '112') and (varlevel == 'Z100-200')): #100-200cm underground soil temp
         vardes = '100-200cm Underground Soil Temperature (K)'
         savename = 'TSOIL100_200cm'
         varscale = 1
         levels = np.array([240,245,250,255,260,265,270,275,280,285,290,295,300])
         pltcm = plt.cm.RdYlBu_r
         levels_diff = np.array([-5,-3,-2,-1,-0.5,-0.1,0.1,0.5,1,2,3,5])
    elif ((varname == 'UFLX') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #zonal momentum flux
         vardes = 'Surface Zonal Momentum Flux (0.01 * N 'r'$\mathregular{kg^{-2}}$'')'
         savename = 'UFLXsfc'
         varscale = 1000
         levels = np.array([-200,-160,-120,-80,-40,-10,10,40,80,120,160,200]) 
         pltcm = plt.cm.RdYlBu_r
         levels_diff = np.array([-100,-50,-30,-20,-10,-5,5,10,20,30,50,100])
    elif ((varname == 'UGRD') and (varGRIBlvltyp == '105') and (varlevel == 'Z10')): #10m zonal wind
         vardes = '10m Above Ground Zonal Wind (m 'r'$\mathregular{s^{-1}}$'')'
         savename = 'UGRD10m'
         varscale = 1
         levels = np.array([-50,-40,-30,-20,-10,-5,-3,-1,1,3,5,10,20,30,40,50])
         pltcm = plt.cm.PiYG
         levels_diff = np.array([-10,-5,-3,-2,-1,-0.5,0.5,1,2,3,5,10])
    elif ((varname == 'UGRD') and (varGRIBlvltyp == '07') and (varlevel == 'L0')): #tropopause zonal wind
         vardes = 'Tropopause Zonal Wind (m 'r'$\mathregular{s^{-1}}$'')'
         savename = 'UGRDtrp'
         varscale = 1
         levels = np.array([-50,-40,-30,-20,-10,-5,-3,-1,1,3,5,10,20,30,40,50])
         pltcm = plt.cm.PiYG
         levels_diff = np.array([-10,-5,-3,-2,-1,-0.5,0.5,1,2,3,5,10])
    elif ((varname == 'UGRD') and (varGRIBlvltyp == '06') and (varlevel == 'L0')): #max wind level zonal wind
         vardes = 'Max Wind Level Zonal Wind (m 'r'$\mathregular{s^{-1}}$'')'
         savename = 'UGRDmwl'
         varscale = 1
         levels = np.array([-50,-40,-30,-20,-10,-5,-3,-1,1,3,5,10,20,30,40,50])
         pltcm = plt.cm.PiYG
         levels_diff = np.array([-20,-10,-5,-3,-2,-1,1,2,3,5,10,20])
    elif ((varname == 'UGRD') and (varGRIBlvltyp == '220') and (varlevel == 'L0')): #PBL zonal wind
         vardes = 'PBL Level Zonal Wind (m 'r'$\mathregular{s^{-1}}$'')'
         savename = 'UGRDpbl'
         varscale = 1
         levels = np.array([-50,-40,-30,-20,-10,-5,-3,-1,1,3,5,10,20,30,40,50]) 
         pltcm = plt.cm.PiYG
         levels_diff = np.array([-10,-5,-3,-2,-1,-0.5,0.5,1,2,3,5,10])
    elif ((varname == 'UGRD') and (varGRIBlvltyp == '107') and (varlevel == 'L9950')): #sigma=.995 zonal wind
         vardes = 'Sigma=.995 Zonal Wind (m 'r'$\mathregular{s^{-1}}$'')'
         savename = 'UGRDsig995'
         varscale = 1
         levels = np.array([-50,-40,-30,-20,-10,-5,-3,-1,1,3,5,10,20,30,40,50])
         pltcm = plt.cm.PiYG
         levels_diff = np.array([-10,-5,-3,-2,-1,-0.5,0.5,1,2,3,5,10])
    elif ((varname == 'U-GWD') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #zonal gravity wave stress
         vardes = 'Surface Zonal Gravity Wave Stress (0.01 * N 'r'$\mathregular{kg^{-2}}$'')'
         savename = 'UGWDsfc'
         varscale = 1000
         levels = np.array([5,10,20,40,60,80,100,120,140,160,180]) 
         pltcm = plt.cm.gnuplot2_r
         levels_diff = np.array([-50,-30,-20,-10,-5,-2,2,5,10,20,30,50])
    elif ((varname == 'ULWRF') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #upwelling longwave sfc
         vardes = 'Surface Upward Longwave Flux (W 'r'$\mathregular{m^{-2}}$'')'
         savename = 'ULWRFsfc'
         varscale = 1
         levels = np.array([5,10,50,100,150,200,250,300,350,400,450,500])
         pltcm = plt.cm.RdYlBu_r
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'ULWRF') and (varGRIBlvltyp == '08') and (varlevel == 'L0')): #upwelling longwave toa
         vardes = 'Top of Atmos Upward Longwave Flux (W 'r'$\mathregular{m^{-2}}$'')'
         savename = 'ULWRFtoa'
         varscale = 1
         levels = np.array([5,10,50,100,150,200,250,300,350,400,450,500])
         pltcm = plt.cm.RdYlBu_r
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'USTM') and (varGRIBlvltyp == '106') and (varlevel == 'Z60-0')): #0-6000m AGL u storm motion
         vardes = '0-6000m Above Ground u-Component of Storm Motion (m 'r'$\mathregular{s^{-1}}$'')'
         savename = 'USTM0_6000m'
         varscale = 1
         levels = np.array([-50,-40,-30,-20,-10,-5,-3,-1,1,3,5,10,20,30,40,50])
         pltcm = plt.cm.PiYG
         levels_diff = np.array([-10,-5,-3,-2,-1,-0.5,0.5,1,2,3,5,10])
    elif ((varname == 'USWRF') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #upwelling shortwave sfc
         vardes = 'Surface Upward Shortwave Flux (W 'r'$\mathregular{m^{-2}}$'')'
         savename = 'USWRFsfc'
         varscale = 1
         levels = np.array([5,10,20,40,60,80,100,120,140,160,180,200,300])
         pltcm = plt.cm.RdYlBu_r
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'USWRF') and (varGRIBlvltyp == '08') and (varlevel == 'L0')): #upwelling shortwave toa
         vardes = 'Top of Atmos Upward Shortwave Flux (W 'r'$\mathregular{m^{-2}}$)'')'
         savename = 'USWRFtoa'
         varscale = 1
         levels = np.array([5,10,20,40,60,80,100,120,140,160,180,200,300])
         pltcm = plt.cm.RdYlBu_r
         levels_diff = np.array([-30,-20,-15,-10,-5,-2,2,5,10,15,20,30])
    elif ((varname == 'VFLX') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #meridional momentum flux
         vardes = 'Surface Meridional Momentum Flux (0.01 * N 'r'$\mathregular{kg^{-2}}$'')'
         savename = 'VFLXsfc'
         varscale = 1000
         levels = np.array([-200,-160,-120,-80,-40,-10,10,40,80,120,160,200])
         pltcm = plt.cm.RdYlBu_r 
         levels_diff = np.array([-100,-50,-30,-20,-10,-5,5,10,20,30,50,100])
    elif ((varname == 'VGRD') and (varGRIBlvltyp == '105') and (varlevel == 'Z10')): #10m meridional wind
         vardes = '10m Above Ground Meridional Wind (m 'r'$\mathregular{s^{-1}}$'')'
         savename = 'VGRD10m'
         varscale = 1
         levels = np.array([-50,-40,-30,-20,-10,-5,-3,-1,1,3,5,10,20,30,40,50])
         pltcm = plt.cm.PiYG
         levels_diff = np.array([-10,-5,-3,-2,-1,-0.5,0.5,1,2,3,5,10])
    elif ((varname == 'VGRD') and (varGRIBlvltyp == '07') and (varlevel == 'L0')): #tropopause meridional wind
         vardes = 'Tropopause Meridional Wind (m 'r'$\mathregular{s^{-1}}$'')'
         savename = 'VGRDtrp'
         varscale = 1
         levels = np.array([-50,-40,-30,-20,-10,-5,-3,-1,1,3,5,10,20,30,40,50])
         pltcm = plt.cm.PiYG
         levels_diff = np.array([-10,-5,-3,-2,-1,-0.5,0.5,1,2,3,5,10])
    elif ((varname == 'VGRD') and (varGRIBlvltyp == '06') and (varlevel == 'L0')): #max wind level meridional wind
         vardes = 'Max Wind Level Meridional Wind (m 'r'$\mathregular{s^{-1}}$'')'
         savename = 'VGRDmwl'
         varscale = 1
         levels = np.array([-50,-40,-30,-20,-10,-5,-3,-1,1,3,5,10,20,30,40,50])
         pltcm = plt.cm.PiYG
         levels_diff = np.array([-20,-10,-5,-3,-2,-1,1,2,3,5,10,20])
    elif ((varname == 'VGRD') and (varGRIBlvltyp == '220') and (varlevel == 'L0')): #PBL meridional wind
         vardes = 'PBL Level Meridional Wind (m 'r'$\mathregular{s^{-1}}$'')'
         savename = 'VGRDpbl'
         varscale = 1
         levels = np.array([-50,-40,-30,-20,-10,-5,-3,-1,1,3,5,10,20,30,40,50])
         pltcm = plt.cm.PiYG
         levels_diff = np.array([-10,-5,-3,-2,-1,-0.5,0.5,1,2,3,5,10])
    elif ((varname == 'VGRD') and (varGRIBlvltyp == '107') and (varlevel == 'L9950')): #sigma=.995 meridional wind
         vardes = 'Sigma=.995 Meridional Wind (m 'r'$\mathregular{s^{-1}}$'')'
         savename = 'VGRDsig995'
         varscale = 1
         levels = np.array([-50,-40,-30,-20,-10,-5,-3,-1,1,3,5,10,20,30,40,50])
         pltcm = plt.cm.PiYG
         levels_diff = np.array([-10,-5,-3,-2,-1,-0.5,0.5,1,2,3,5,10])
    elif ((varname == 'V-GWD') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #meridional gravity wave stress
         vardes = 'Surface Meridional Gravity Wave Stress (0.01 * N 'r'$\mathregular{kg^{-2}}$'')'
         savename = 'VGWDsfc'
         varscale = 1000
         levels = np.array([5,10,20,40,60,80,100,120,140,160,180])
         pltcm = plt.cm.gnuplot2_r
         levels_diff = np.array([-50,-30,-20,-10,-5,-2,2,5,10,20,30,50])
    elif ((varname == 'VRATE') and (varGRIBlvltyp == '220') and (varlevel == 'L0')): #PBL vent. rate
         vardes = 'PBL Level Ventilation Rate ('r'$\mathregular{km^{2}}$'' 'r'$\mathregular{s^{-1}}$'')'
         savename = 'VRATEpbl'
         varscale = 0.001
         levels = np.array([5,10,15,20,25,30,35,40,45]) 
         pltcm = plt.cm.YlGnBu
         levels_diff = np.array([-15,-12,-9,-6,-3,-1,1,3,6,9,12,15])
    elif ((varname == 'VSTM') and (varGRIBlvltyp == '106') and (varlevel == 'Z60-0')): #0-6000m AGL v storm motion
         vardes = '0-6000m Above Ground v-Component of Storm Motion (m 'r'$\mathregular{s^{-1}}$'')'
         savename = 'VSTM0_6000m'
         varscale = 1
         levels = np.array([-50,-40,-30,-20,-10,-5,-3,-1,1,3,5,10,20,30,40,50])
         pltcm = plt.cm.PiYG
         levels_diff = np.array([-10,-5,-3,-2,-1,-0.5,0.5,1,2,3,5,10])
    elif ((varname == 'VVEL') and (varGRIBlvltyp == '107') and (varlevel == 'L9950')): #.995 sigma vertical velocity
         vardes = 'Sigma=.995 Vertical Velocity (hPa 'r'$\mathregular{hour^{-1}}$'')'
         savename = 'VVELsig995'
         varscale = 36
         levels = np.array([-50,-40,-30,-20,-10,-5,-3,-1,1,3,5,10,20,30,40,50])
         pltcm = plt.cm.PiYG
         levels_diff = np.array([-10,-5,-4,-3,-2,-1,1,2,3,4,5,10])
    elif ((varname == 'VWSH') and (varGRIBlvltyp == '07') and (varlevel == 'L0')): #tropopause vertical speed shear
         vardes = 'Tropopause Vertical Speed Shear ('r'$\mathregular{hour^{-1}}$'')'
         savename = 'VWSHtrp'
         varscale = 3600
         levels = np.array([-100,-50,-40,-30,-20,-10,-5,-3,3,5,10,20,30,40,50,100])
         pltcm = plt.cm.PiYG
         levels_diff = np.array([-10,-5,-4,-3,-2,-1,1,2,3,4,5,10])
    elif ((varname == 'WATR') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #surface water runoff
         vardes = 'Surface Water Runoff (kg 'r'$\mathregular{m^{-2}}$'')'
         savename = 'WATRsfc'
         varscale = 1
         levels = np.array([0.001,0.01,0.02,0.04,0.06,0.08,0.1,0.2,0.4,0.6,0.8,1]) 
         pltcm = plt.cm.BuGn
         levels_diff = np.array([-1,-0.5,-0.1,-0.05,-0.01,-0.001,0.001,0.01,0.05,0.1,0.5,1])
    elif ((varname == 'WEASD') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #surface snow accumulation 
         vardes = 'Surface Accum Snow (kg 'r'$\mathregular{m^{-2}}$'')'
         savename = 'WEASDsfc'
         varscale = 1
         levels = np.array([0.1,0.5,1,3,6,10,20,30,40,50,70,90])
         pltcm = plt.cm.winter_r
         levels_diff = np.array([-8,-6,-4,-2,-1,-0.1,0.1,1,2,4,6,8])
    elif ((varname == 'WILT') and (varGRIBlvltyp == '01') and (varlevel == 'Z0')): #surface wilting point 
         vardes = 'Surface Wilting Point (fraction)'
         savename = 'WILTsfc'
         varscale = 1
         levels = np.array([0.01,0.02,0.04,0.06,0.08,0.1,0.2,0.4,0.6,0.8,1])
         pltcm = plt.cm.YlGnBu
         levels_diff = np.array([-1,-0.5,-0.1,-0.05,-0.01,-0.001,0.001,0.01,0.05,0.1,0.5,1])
 
    return vardes,savename,levels,levels_diff,pltcm,varscale
