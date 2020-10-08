import xarray as xr
import subprocess
import glob
import sys
import pytest
import pwd
import os

import SETTINGS
import run_chunk

# test netCDF file produced has the expected dimensions
def test_output_shape():
    cmd = 'python run_chunk.py -s min -m MOHC/HadGEM2-ES -e r1i1p1 -v rh'
    subprocess.call(cmd, shell=True)

    user_name = pwd.getpwuid(os.getuid()).pw_name
    nc_output = SETTINGS.OUTPUT_PATH_TMPL.format(GWS='/gws/nopw/j04/cedaproc', USER=user_name)
    fpath = f'{nc_output}/rh.nc'

    ds = xr.open_dataset(fpath)
    assert ds.rh.shape == (145, 192)

    cmd_delete = 'rm -r logs'
    subprocess.call(cmd_delete, shell=True)

# test that valid data function fails if data is out of chosen range
@pytest.mark.xfail(raises=AssertionError)
def test_is_valid_range():
    # expect this to fail

    pattern = '/badc/cmip5/data/cmip5/output1/{model}/historical/mon/land/Lmon' \
              '/{ensemble}/latest/{var_id}/*.nc'
    model = 'MOHC/HadGEM2-ES'
    ensemble = 'r1i1p1'
    var_id = 'rh'
    glob_pattern = pattern.format(model=model, ensemble=ensemble, var_id=var_id)
    nc_files = glob.glob(glob_pattern)

    ds = xr.open_mfdataset(nc_files)
    times_in_range = ds.time.loc['1800-01-01':'1900-01-01']

    n_req_times = 100 * 12  # yrs * months
    assert len(times_in_range) == n_req_times

# test return acts as expected in run_unit
def test_no_valid_files():
    value = run_chunk.run_unit('min', 'MOHC/HadGEM2-ES', 'r12i1p1', 'rh')
    assert value is False

# testing failure count works
@pytest.mark.xfail(raises=SystemExit)
def test_failure_count():
    # expect system exit - expect 2 errors
    sys.argv = 'run_chunk.py -s min -m MOHC/HadGEM2-ES -e r12i1p1 -v rh ra'.split()
    args = run_chunk.arg_parse_chunk()
    SETTINGS.EXIT_AFTER_N_FAILURES = 1
    run_chunk.run_chunk(args)

# check nothing is returned when success file found
def test_success_file():
    cmd = 'python run_chunk.py -s min -m MOHC/HadGEM2-ES -e r1i1p1 -v rh'
    subprocess.call(cmd, shell=True)
    value = run_chunk.run_unit('min', 'MOHC/HadGEM2-ES', 'r1i1p1', 'rh')
    assert value is True
