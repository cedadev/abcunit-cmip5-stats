import xarray as xr
import subprocess


def test_output_shape():
    cmd = 'python /home/users/esmith88/abcunit/abcunit-cmip5-stats/run_chunk.py -s min -m MOHC/HadGEM2-ES -e r1i1p1 -v rh'
    subprocess.call(cmd, shell=True)
    
    fpath = '/home/users/esmith88/abcunit/abcunit-cmip5-stats/test/outputs/min/MOHC/HadGEM2-ES/r1i1p1/rh.nc'
    ds = xr.open_dataset(fpath)
    assert ds.rh.shape == (145, 192)

    cmd_delete = 'rm -r success outputs'
    subprocess.call(cmd_delete, shell=True)
