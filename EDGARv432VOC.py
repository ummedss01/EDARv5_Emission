import os, sys, glob, zipfile
import numpy as np
from datetime import datetime, timedelta
import xarray as xr
xr.set_options(keep_attrs=True)
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
#import cartopy
#import cartopy.crs as ccrs


sumdir = '/home/Emission/New_emission/NMVOC_species/npl/result/'

datadirs = sorted(glob.glob('/home/New_emission/NMVOC_species/npl/VOC432_without_BBAviation/VOC/*/')) 
for datadir in datadirs:
   emissectors = [list.split('_monthly_')[1][0:-7] for  list in glob.glob(datadir + '*/*.zip')] 
   workdir = '/home/New_emission/NMVOC_species/npl/process'
   print('Process Start for....', datadir)
   vtype = datadir.split('/')[-3]
   ptype = datadir.split('/')[-2]
   etype = datadir.split('/')[-1]
   #print('vtype:',vtype,'ptype:',ptype,'etype:',etype)
  # #os.system('rm -rf ' + workdir + '/' + ptype)
   workdir = workdir + '/' + ptype + '/'
   #workdir = workdir + '/' + ptype + '/'
   [zipfile.ZipFile(qfile ,"r").extractall(workdir) for qfile in glob.glob(datadir + '*/*.zip')]
   if len(glob.glob(workdir + '*.nc')) == 0:
      d = xr.concat([xr.open_mfdataset(sorted(glob.glob(workdirr + 'v432_*_2010_?_*.0.1x0.1.nc')) + sorted(glob.glob(workdirr + 'v432_*_2010_??_*.0.1x0.1.nc')), combine='nested', concat_dim='month', parallel=True) for workdirr in glob.glob(workdir + '*/')],dim='sectors').sum('sectors')
      #conc = [xr.open_mfdataset(sorted(glob.glob(workdirr + 'v50_*_2015_?_*.0.1x0.1.nc')) + sorted(glob.glob(workdirr + 'v50_*_2015_??_*.0.1x0.1.nc')), combine='nested', concat_dim='month', parallel=True)[list(d.keys())[-1]].attrs['total_' + list(d.keys())[-1]] for workdirr in glob.glob(workdir + '*/')]
   else:
      d = xr.concat([xr.open_mfdataset(sorted(glob.glob(workdir + 'v432_*_2010_?_' + emissector + '.0.1x0.1.nc')) + sorted(glob.glob(workdir + 'v432_*_2010_??_' + emissector + '.0.1x0.1.nc')), combine='nested', concat_dim='month', parallel=True) for emissector in emissectors],dim='sectors').sum('sectors')
      #conc = [xr.open_mfdataset(sorted(glob.glob(workdir + 'v50_*_2015_?_' + emissector + '.0.1x0.1.nc')) + sorted(glob.glob(workdir + 'v50_*_2015_??_' + emissector + '.0.1x0.1.nc')), combine='nested', concat_dim='month', parallel=True)[list(d.keys())[-1]].attrs['total_' + list(d.keys())[-1]] for emissector in emissectors]
   d = d.rename_vars({list(d.keys())[-1]:'emi_dummy'})
   dd = d
   londata = d.lon.data
   lonattrs = {'standard_name': 'longitude', 'long_name': 'longitude', 'units': 'degrees_east', 'comment': 'center_of_cell'}
   latdata = d.lat.data
   latattrs = {'standard_name': 'latitude', 'long_name': 'latitude', 'units': 'degrees_north', 'comment': 'center_of_cell'}
   datedata = np.array([(datetime.strptime('2010',"%Y").strftime("%Y") + str("%02d" % (i + 1))) + '01' for i in range(12)],dtype='int32')
   datesecdata = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype='int32')
   d = d.rename_dims({'month':'time'})
   emis_totdata = d.emi_dummy.data.compute()
   d.attrs.update({'history2' : "Adding all type of emissions; NPL"})
   d.attrs.update({'title' : ptype + " 2010 monthly mean"})
   attrs = d.attrs
   sat = xr.Dataset(
                 {"date":("time",datedata),
                  "datesec":("time",datesecdata),
                  "emis_tot": (("time","lat","lon"), emis_totdata)},
             coords={"lat": latdata, "lon": londata},
             attrs = attrs
             )
   #sat.emis_tot.attrs = sat.emis_tot.attrs['emis_tot'] = ''
   sat.emis_tot.attrs['sectors'] = emissectors
   sat.emis_tot.attrs.update({'Remark' : "Consider this variable as SUM of all sectors; NPL"})
   sat.to_netcdf(sumdir + 'EDGAR' + vtype + '-' + ptype + '-emi_tot-2010-.0.1x0.1.nc')
   
   
   
   
   

"""
