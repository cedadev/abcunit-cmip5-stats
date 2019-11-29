import xarray as xr


def test_xarry_opens_file():
    fpath = '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/r1i1p1/latest/rh/rh_Lmon_-190911.nc'
    ds = xr.open_dataset(fpath)



