import glob
import xarray as xr
import numpy as np
import pandas as pd



def test_xarray_open_bad_path_fail():
    fpath = '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/r1i1p1/' \
            'latest/rh/rh_Lmon_-190911.nc'

    try:
        ds = xr.open_dataset(fpath)
    except IOError as exc:   #was FileNotFoundError
        pass


def test_xarray_open_good_path_success():
    fpath = '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/' \
            'r1i1p1/latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_193412-195911.nc'
    ds = xr.open_dataset(fpath)


def test_create_and_save_netcdf_file_bad_dimension_length(tmpdir):
    try:
        ds = xr.Dataset({'test': (('x', 'y'), np.random.rand(4, 4))},
                        coords={'x': [1, 2, 3, 4],
                                'y': [1, 2, 3, 4]})
        ds.to_netcdf(path=tmpdir.mkdir("test_dir").join("example_dataset.nc"))

    except ValueError as exc:
        pass


def test_create_and_save_netcdf_file_input_as_dates(tmpdir):
    try:
        tmpdir.mkdir("test_dir").join("example_dataset_1.nc")
        ds = xr.Dataset({'test': (('x', 'y', 't'), np.random.rand(4, 4, 5))},
                        coords={'x': [1, 2, 3, 4],
                                'y': [1, 2, 3, 4],
                                't': pd.date_range('1990-02-01', periods=5,
                                                    freq='M')})
        ds.to_netcdf(path="test_dir/example_dataset_1.nc")

    except PermissionError as exc:
        pass


def test_create_and_save_netcdf_file_input_as_dates_2(tmpdir):
    ds = xr.Dataset({'test': (('x', 'y', 't'), np.random.rand(4, 4, 5))},
                    coords={'x': [1, 2, 3, 4],
                            'y': [1, 2, 3, 4],
                            't': pd.date_range('1990-02-01', periods=5,
                                                freq='M')})
    ds.to_netcdf(path=tmpdir.mkdir("test_dir").join("example_dataset_1.nc"))



def test_create_and_save_netcdf_file_correct_dimension_length(tmpdir):
    ds = xr.Dataset({'test': (('x', 'y', 'z'), np.random.rand(4, 4, 5))},
                    coords={'x': [1, 2, 3, 4],
                            'y': [1, 2, 3, 4],
                            'z': [1, 2, 3, 4, 5]})

    ds.to_netcdf(path=tmpdir.mkdir("test_dir").join("example_dataset_2.nc"))


def test_xarray_open_time_dimension_fail():
    try:
        fpath = '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land' \
                '/Lmon/r1i1p1/latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_193412-195911.nc'
        ds = xr.open_dataset(fpath)
        time = ds.sel(time)
    except UnboundLocalError as exc:
        pass



def test_xarray_open_time_dimension_fail_dims_do_not_exist():
    try:
        fpath = '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon' \
                '/r1i1p1/latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_193412-195911.nc'
        ds = xr.open_dataset(fpath)
        time = ds.sel(dims='time')
    except ValueError as exc:
        pass


def test_xarray_open_time_dimension_fail_key_error():
    try:
        fpath = '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/' \
                'r1i1p1/latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_193412-195911.nc'
        ds = xr.open_dataset(fpath)
        time = ds.sel(lat=360, lon=90)
    except KeyError as exc:
        pass


def test_xarray_open_time_dimension():

    fpath = '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/r1i1p1/' \
            'latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_193412-195911.nc'
    ds = xr.open_dataset(fpath)
    time = ds.sel(lat=0, lon=0)


def test_slice_a_time_range_incorrect_shape():
    fpath = '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/r1i1p1/' \
            'latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_193412-195911.nc'
    ds = xr.open_dataset(fpath)
    time_slice = ds.time.loc['1900-01-01':'2000-01-01']
    #return time_slice
    print('time_slice_shape =', time_slice.shape)


def test_slice_a_time_range_correct_shape():
    fpath = '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/r1i1p1/' \
            'latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_193412-195911.nc'
    ds = xr.open_dataset(fpath)
    time_slice = ds.sel(time=slice('1934-12-01', '1939-12-01'))
    return time_slice
    #print('time_slice_shape_2 =', time_slice.rh.shape)


def test_find_temporal_max_incorrect_shape():
    try:
        fpath = '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/r1i1p1/' \
                'latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_193412-195911.nc'
        ds = xr.open_dataset(fpath)
        print('shape =', ds.shape)
        maximum = ds.max(dim='time')
        print('max =', maximum)
        print('max shape =', maximum.shape)

    except AttributeError as exc:
        pass

def test_find_temporal_max():
    fpath = '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/r1i1p1/' \
            'latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_193412-195911.nc'
    ds = xr.open_dataset(fpath)
    print('shape =', ds.rh.shape)
    maximum = ds.rh.max(dim='time')
    print('max =', maximum)
    print('max shape =', maximum.shape)


def test_find_temporal_min():
    fpath = '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/r1i1p1/' \
            'latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_193412-195911.nc'
    ds = xr.open_dataset(fpath)
    minimum = ds.rh.min(dim='time')
    print('min =', minimum)
    print('min shape =', minimum.shape)


def test_find_temporal_mean():
    fpath = '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/r1i1p1' \
            '/latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_193412-195911.nc'
    ds = xr.open_dataset(fpath)
    mean = ds.rh.mean(dim='time')
    print('mean =', mean)
    print('mean shape =', mean.shape)

"""def create_parser(args):
        parser = argparse.ArgumentParser(description='prints given arguments')
        parser.add_argument('-a', help='first argument to print')

        args = parser.parse_args(args)


def test_arg_parser():
        parser = create_parser('-a hi'.split())
        assertEqual(parser, 'a=hi')"""


def test_open_multiple_files():
    pattern = '/badc/cmip5/data/cmip5/output1/{model}/historical/mon/land/Lmon' \
              '/{ensemble}/latest/{var_id}/*.nc'
    model = 'MOHC/HadGEM2-ES'
    ensemble = 'r1i1p1'
    var_id = 'rh'
    glob_pattern = pattern.format(model=model, ensemble=ensemble, var_id=var_id)
    nc_files = glob.glob(glob_pattern)
    return xr.open_mfdataset(nc_files)


def test_max_multiple_files():
    ds = test_open_multiple_files()
    maximum = ds.rh.max(dim='time')
    print('max_multiple =', maximum)
    print('max_multiple shape =', maximum.shape)


def test_max_of_time_slice():
    time_slice = test_slice_a_time_range_correct_shape()
    print('time_slice_shape =', time_slice.rh.shape)
    maximum = time_slice.rh.max(dim='time')
    print('max =', maximum)
    print('max shape =', maximum.shape)

# do assert instead of print from now on
