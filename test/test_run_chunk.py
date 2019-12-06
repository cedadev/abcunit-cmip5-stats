import xarray as xr

def test_output_shape():
    fpath = '/home/users/esmith88/abcunit/abcunit-cmip5-stats/outputs/min/MOHC/HadGEM2-ES/r1i1p1/rh.nc'
    ds = xr.open_dataset(fpath)
    assert ds.rh.shape == (145, 192)