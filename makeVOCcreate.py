import os, sys, glob
import numpy as np
import xarray as xr
xr.set_options(keep_attrs=True)
#from matplotlib import pyplot as plt
#import matplotlib
#matplotlib.use('TkAgg')
#import cartopy
#import cartopy.crs as ccrs
#from cartopy.io.shapereader import Reader
#from cartopy.feature import ShapelyFeature

vocmw = {'voc1': 32, 'voc2': 30, 'voc3': 44, 'voc4': 58, 'voc5': 72, 'voc6': 86, 'voc7': 28, 'voc8': 40, 'voc9': 26, 'voc10': 68, 'voc11': 136, 'voc12': 56, 'voc13': 78, 'voc14': 92, 'voc15': 106, 'voc16': 120, 'voc17': 126, 'voc18': 184, 'voc19': 81, 'voc20': 138, 'voc21': 30, 'voc22': 44, 'voc23': 72, 'voc24': 59, 'voc25': 68}

nmvoc2010 = xr.open_dataset('/home//New_emission/NMVOC_species/npl/result/EDGARv432_AP-NMVOCemi_tot-2010-.0.1x0.1.nc')
nmvoc2015 = xr.open_dataset('/home//NMVOC_species/npl/EDVARV5N/EDGARvEDGARv5P-NMVOC-emi_tot-2015-.0.1x0.1.nc')

for sno in range(1,26):
   voc2010 = xr.open_dataset('/home/NMVOC_species/npl/result/EDGARVOC-voc' + str(sno) + '-emi_tot-2010-.0.1x0.1.nc')
   voc2015 = ((voc2010/nmvoc2010) * nmvoc2015)
   voc2015['date'] = nmvoc2015.date
   voc2015.attrs = voc2010.attrs
   #voc2015.emis_tot.attrs.update({'molecular_weight' : 'SATEESH'})
   voc2015.emis_tot.attrs.update({'molecular_weight' : np.float(vocmw['voc' + str(sno)])})
   #sat = xr.Dataset(
   #              {"date":("time",voc2015.date.data),
   #               "datesec":("time",datesecdata),
   #               "emis_tot": (("time","lat","lon"), emis_totdata)},
   #          coords={"lat": latdata, "lon": londata},
   #          attrs = attrs
   #          )
   voc2015.datesec.data = voc2010.datesec.data
   voc2015.to_netcdf('/home/New_emission/NMVOC_species/npl/EDVARV5N/EDGAR_V5_emis_voc' + str(sno) + '_2015.0.1x0.1.nc')
"""   
  
"""   
