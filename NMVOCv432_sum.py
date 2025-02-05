import os, sys, glob, zipfile
import numpy as np
from datetime import datetime, timedelta
import xarray as xr
xr.set_options(keep_attrs=True)
#from matplotlib import pyplot as plt
#import matplotlib
#matplotlib.use('TkAgg')
#import cartopy
#import cartopy.crs as ccrs
#from cartopy.io.shapereader import Reader
#from cartopy.feature import ShapelyFeature


sumdir = '/home/New_emission/NMVOC_species/npl/EDGARv432NMVOC/result/'

datadirs = sorted(glob.glob('/home/Emission/New_emission/NMVOC_species/npl/EDGARv432NMVOC/sector/v432_AP/NMVOC/'))

for datadir in datadirs:
   workdir = '/home/Emission/New_emission/NMVOC_species/npl/EDGARv432NMVOC/porcess'
   print('Process Start for....', datadir)
   vtype = datadir.split('/')[-3]
   ptype = datadir.split('/')[-2]
   etype = datadir.split('/')[-1]
   print('vtype:',vtype,'\n','ptype:',ptype,'\n','etype:',etype, 'Not needed for v432 data........!')
   os.system('rm -rf ' + workdir + '/' + ptype)
   workdir = workdir + '/' + ptype + '/'
   print('workdir: ', workdir)
   [zipfile.ZipFile(qfile ,"r").extractall(workdir) for qfile in glob.glob(datadir + '*/*.zip')]
   #/scratch/sateeshm/emis/BC/v432_BC_2010_1_IPCC_2B.0.1x0.1.nc
   #/scratch/sateeshm/emis/voc1/v432_VOC_spec_voc1_2010_1_IPCC_1A3a_LTO.0.1x0.1.nc
   if vtype == 'v432_VOC_spec':
      emissectors = [list.split('_1_')[1][0:-11] for  list in glob.glob(workdir + '/v432_VOC_spec_' + ptype + '_2010_1_*.nc')]
      print('emissectors:', emissectors)
      d = xr.concat([xr.open_mfdataset(sorted(glob.glob(workdir + 'v432_VOC_spec_' + ptype + '_2010_?_' + emissector + '.0.1x0.1.nc')) + sorted(glob.glob(workdir + 'v432_VOC_spec_' + ptype + '_2010_??_' + emissector + '.0.1x0.1.nc')), combine='nested', concat_dim='month', parallel=True) for emissector in emissectors],dim='sectors').sum('sectors')
   elif vtype == 'v432_AP':
      emissectors = [list.split('_1_')[1][0:-11] for  list in glob.glob(workdir + '/v432_' + ptype + '_2010_1_*.nc')]
      print('emissectors:', emissectors)
      d = xr.concat([xr.open_mfdataset(sorted(glob.glob(workdir + 'v432_' + ptype + '_2010_?_' + emissector + '.0.1x0.1.nc')) + sorted(glob.glob(workdir + 'v432_' + ptype + '_2010_??_' + emissector + '.0.1x0.1.nc')), combine='nested', concat_dim='month', parallel=True) for emissector in emissectors],dim='sectors').sum('sectors')
      #d = xr.concat([xr.open_mfdataset(sorted(glob.glob(workdir + 'v432_*_2010_?_' + emissector + '.0.1x0.1.nc')) + sorted(glob.glob(workdir + 'v432_*_2010_??_' + emissector + '.0.1x0.1.nc')), combine='nested', concat_dim='month', parallel=True) for emissector in emissectors],dim='sectors').sum('sectors')
   d = d.rename_vars({list(d.keys())[-1]:'emi_tot'})
   dd = d
   londata = d.lon.data
   lonattrs = {'standard_name': 'longitude', 'long_name': 'longitude', 'units': 'degrees_east', 'comment': 'center_of_cell'}
   latdata = d.lat.data
   latattrs = {'standard_name': 'latitude', 'long_name': 'latitude', 'units': 'degrees_north', 'comment': 'center_of_cell'}
   datedata = np.array([(datetime.strptime('2010',"%Y").strftime("%Y") + str("%02d" % (i + 1))) + '01' for i in range(12)],dtype='int32')
   datesecdata = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype='int32')
   d = d.rename_dims({'month':'time'})
   emis_totdata = d.emi_tot.data.compute()
   d.attrs.update({'history2' : "Adding all type of emissions; NPL"})
   attrs = d.attrs
   sat = xr.Dataset(
                 {"date":("time",datedata),
                  "datesec":("time",datesecdata),
                  "emis_tot": (("time","lat","lon"), emis_totdata)},
             coords={"lat": latdata, "lon": londata},
             attrs = attrs
             )
   sat.emis_tot.attrs = d.emi_tot.attrs
   sat.emis_tot.attrs['total_emi_conc'] = ''
   sat.emis_tot.attrs['sectors'] = emissectors
   sat.emis_tot.attrs.update({'Remark' : "Consider this variable as SUM of all sectors; U.S. NPL"})
   sat.to_netcdf(sumdir + 'EDGAR' + vtype + '-' + ptype + 'emi_tot-2010-.0.1x0.1.nc')
