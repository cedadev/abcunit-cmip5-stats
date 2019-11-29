import xarray as xr


def test_xarray_open_bad_path_fail():
    fpath = '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/r1i1p1/latest/rh/rh_Lmon_-190911.nc'

    try:
        ds = xr.open_dataset(fpath)
    except FileNotFoundError as exc:
        pass


def test_xarray_open_good_path_success():
    fpath = '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/r1i1p1/latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_193412-195911.nc'
    ds = xr.open_dataset(fpath)

