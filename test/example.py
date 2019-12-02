import xarray as xr

fpath = '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/r1i1p1/latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_193412-195911.nc'
ds = xr.open_dataset(fpath)
time_slice = ds.time.loc['1900-01-01':'2000-01-01']
print(time_slice)
