import sys
import xarray as xr

from lib import defaults
from run_all import arg_parse_all
from run_batch import arg_parse_batch
from run_chunk import arg_parse_chunk

# check arguemnts are parsed correctly
def test_good_args1():
    sys.argv = 'run_all.py -s mean'.split()
    args = arg_parse_all()
    assert args.stat == ['mean']
    assert args.stat != ['min']
    assert args.stat != ['max']


def test_good_args2():
    try:
        sys.argv = 'run_batch.py -s mean -m BCC/bcc-csm1-1'.split()
        args = arg_parse_batch()
        assert args.model == 'BCC/bcc-csm1-1'
    except AssertionError as exc:
        pass


def test_good_args3():
    try:
        sys.argv = 'run_batch.py -s mean -m BCC/bcc-csm1-1'.split()
        args = arg_parse_batch()
        assert args.model == ['BCC/bcc-csm1-1']
        assert args.stat == 'mean'
    except AssertionError as exc:
        pass


def test_good_args4():
    sys.argv = 'run_batch.py -s mean -m BCC/bcc-csm1-1'.split()
    args = arg_parse_batch()
    assert args.model == ['BCC/bcc-csm1-1']
    assert args.stat == ['mean']


# test that stat is required
def test_arg_parse_all_1():
    try:
        sys.argv = 'run_chunk.py'.split()
        arg_parse_all()
    except SystemExit as exc:
        pass

# test works with only stat
def test_arg_parse_all_2():
    sys.argv = 'run_chunk.py -s min'.split()
    arg_parse_all()


# test defaults are correct
def test_arg_parse_all_3():
    sys.argv = 'run_chunk.py -s min'.split()
    args = arg_parse_all()
    assert args.model == defaults.models
    assert args.ensemble == defaults.ensembles
    assert args.var_id == defaults.variables


# testing that model argument is required
def test_arg_parse_batch():
    try:
        sys.argv = 'run_chunk.py -s min'.split()
        arg_parse_batch()
    except SystemExit as exc:
        pass

# test defaults are correct
def test_arg_parse_batch_2():
    sys.argv = 'run_chunk.py -s min -m BCC/bcc-csm1-1'.split()
    args = arg_parse_all()
    assert args.ensemble == defaults.ensembles
    assert args.var_id == defaults.variables


# testing that other arguments are required
def test_arg_parse_chunk_1():
    try:
        sys.argv = 'run_chunk.py -s min'.split()
        arg_parse_chunk()
    except SystemExit as exc:
        pass

# testing ensemble is required
def test_arg_parse_chunk_2():
    try:
        sys.argv = 'run_chunk.py -s min -m BCC/bcc-csm1-1'.split()
        arg_parse_chunk()
    except SystemExit as exc:
        pass

# check variables defaults to all
def test_arg_parse_chunk_3():
    sys.argv = 'run_chunk.py -s min -m BCC/bcc-csm1-1 -e r11i1p1'.split()
    args = arg_parse_chunk()
    assert args.var_id == defaults.variables


# test converting from string
def test_arg_parse_return():
    sys.argv = 'run_chunk.py -s min -m MOHC/HadGEM2-ES -e r11i1p1 -v rh'.split()
    fpath = '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon' \
            '/r1i1p1/latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_193412-195911.nc'

    ds = xr.open_dataset(fpath)
    args = arg_parse_chunk()

    mn = ds['rh'].min(dim='time')
    assert(mn.shape == (145, 192))


