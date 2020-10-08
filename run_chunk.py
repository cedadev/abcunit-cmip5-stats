#!/usr/bin/env python

"""This script takes arguments from the command line and runs the function
run_unit for each of the variables provided as an argument or for
all variables if none were provided."""

import sys
import os
import pwd
import glob
import argparse
import xarray as xr

from lib import defaults
from output_handler.database_handler import DataBaseHandler
from output_handler.file_system_handler import FileSystemHandler
import SETTINGS


def arg_parse_chunk():
    """
    Parses arguments given at the command line

    :return: Namespace object built from attributes parsed from command line.
    """

    parser = argparse.ArgumentParser()

    stat_choices = ['min', 'max', 'mean']
    model_choices = defaults.models
    ensemble_choices = defaults.ensembles
    variable_choices = defaults.variables

    parser.add_argument('-s', '--stat', nargs=1, type=str, choices=stat_choices,
                        required=True, help=f'Type of statistic, must be one of: '
                                            f'{stat_choices}', metavar='')
    parser.add_argument('-m', '--model', nargs=1, type=str, choices=model_choices,
                        required=True, help=f'Institue and model combination to run statistic on, '
                                            f'must be one of: {model_choices}', metavar='')
    parser.add_argument('-e', '--ensemble', nargs=1, type=str, choices=ensemble_choices,
                        required=True, help=f'Ensemble to run statistic on, must be one of: '
                                            f'{ensemble_choices}', metavar='')
    parser.add_argument('-v', '--var_id', choices=variable_choices, default=variable_choices,
                        help=f'Variable to run statistic on, can be one or many of: '
                             f'{variable_choices}. Default is all variables.', metavar='',
                        nargs='*')

    return parser.parse_args()


def find_files(model, ensemble, var_id):
    """
    Finds files that correspond to the given arguments.

    :param model: (string) Model chosen as argument at command line.
    :param ensemble: (string) Ensemble chosen as argument at command line.
    :param var_id: (string) Variable chosen as argument at command line.
    :return: The netCDF files that correspond to the arguments.
    """

    pattern = '/badc/cmip5/data/cmip5/output1/{model}/historical/mon/land' \
              '/Lmon/{ensemble}/latest/{var_id}/*.nc'
    glob_pattern = pattern.format(model=model,
                                  ensemble=ensemble, var_id=var_id)
    nc_files = glob.glob(glob_pattern)
    print(f'[INFO] found files: {nc_files}')

    return nc_files


def is_valid_range(nc_files, start=SETTINGS.START_DATE, end=SETTINGS.END_DATE):
    """
    Checks the date range is valid for the given NetCDF files

    :param nc_files: (netCDF) The netCDF files found from the command line arguments
    :param start: (string: format = YYYY-MM-DD) Date to start range the statistic is
           calculated over.
    :param end: (string: format = YYYY-MM-DD) Date to end range the statistic is
           calculated over.
    :return: Boolean: True if range is valid, False if not.
    """

    try:
        ds = xr.open_mfdataset(nc_files)
        times_in_range = ds.time.loc[start:end]

        n_req_times = 100 * 12  # yrs * months
        assert len(times_in_range) == n_req_times

        print('[INFO] Range is valid')
        return True

    except AssertionError as err:
        print('[ERROR] Range is invalid')
        return False


def calculate_statistic(nc_files, var_id, stat):
    """
    Calculates the required statistic for each variable for each ensemble
    and model requested.

    :param nc_files: (netCDF) The netCDF files found from the command line arguments
    :param var_id: (string) Variable chosen as argument at command line.
    :param stat: (string) Statistic to calculate as specified at the command line.
    :return: NetCDF file of the calculated statistic.
    """

    dataset = xr.open_mfdataset(nc_files)
    stat = str(stat)

    if stat == 'mean':
        result = dataset[var_id].mean(dim='time', keep_attrs=True)
    elif stat == 'max':
        result = dataset[var_id].max(dim='time', keep_attrs=True)
    elif stat == 'min':
        result = dataset[var_id].max(dim='time', keep_attrs=True)

    return result


def run_chunk(args):
    """
    Loops over each variable listed and calls run_unit.

    :param args: (namespace) Namespace object built from attributes parsed from command line
    """
    # set initial failure count
    # keep track of failures. Many failures expected for this example so the
    # limit is set high
    # good practice to include this
    failure_count = 0

    # turn arguments into string

    ensemble = ' '.join(args.ensemble)
    model = ' '.join(args.model)
    stat = ' '.join(args.stat)

    for var_id in args.var_id:
        print(f"Running for {var_id}")

        # exit if too many failures
        if failure_count >= SETTINGS.EXIT_AFTER_N_FAILURES:
            print('[ERROR] Maximum failure count met')
            sys.exit(1)

        unit = run_unit(stat, model, ensemble, var_id)
        if unit is False:
            failure_count += 1
            continue
        else:
            continue

    print(f"Completed job")

def _get_results_handler(n_facets, sep, error_types):
    """ 
    Returns a result handler which either uses a database or the file system
    depending on the SETTING.BACKEND.
    If using a database make sure there is an environment variable called 
    $ABCUNIT_DB_SETTINGS which is set to "dbname=<db_name> user=<user_name> host=<host_name> password=<password>".
    
    :param n_facets: (int) Number of facets used to define a unit.
    :param sep: (str) Delimeter for facet separation
    :param error_types: (list) List of the string names of the types of errors tat can occur.
    """

    if SETTINGS.BACKEND == 'db':
        constring = os.environ.get("ABCUNIT_DB_SETTINGS")
        if not constring:
            raise KeyError('Please create environment variable ABCUNI_DB_SETTINGS'
                            'in for format of "dbname=<db_name> user=<user_name>'
                            'host=<host_name> password=<password>"')
        return DataBaseHandler(constring, error_types)
    elif SETTINGS.BACKEND == 'file':
        return FileSystemHandler(n_facets, sep, error_types)
    else:
        raise ValueError('SETTINGS.BACKEND is not set properly')

def run_unit(stat, model, ensemble, var_id):
    """
    Calculates the chosen statistic for the arguments provided.
    Keeps track of whether the job was successful or not and writes the
    result of the statistic to an output file.

    :param stat: (string) Statistic to calculate as specified at the command line.
    :param model: (string) Model chosen as argument at command line.
    :param ensemble: (string) Ensemble chosen as argument at command line.
    :param var_id: (string) Variable chosen as argument at command line.
    :return: txt or NetCDF file depending on success/ failure of the job.
    """

    sep = '.'
    job_id = f'{stat}/{model}/{ensemble}/{var_id}'.replace(os.sep, sep) # Model names contain a / annoyingly
    n_facets = len(job_id.split(sep))
    rh = _get_results_handler(n_facets, sep, ['bad_data', 'bad_num', 'no_output'])
    
    current_directory = os.getcwd()  # get current working directory
    user_name = pwd.getpwuid(os.getuid()).pw_name # get username of user who ran this code

    #get path to send nc file results to
    output_path = SETTINGS.OUTPUT_PATH_TMPL.format(
        GWS='/gws/nopw/j04/cedaproc', USER=user_name)

    #check if job has already been run successfully 
    if rh.ran_succesfully(job_id):
        print(f'[INFO] Already ran for {stat}, {model}, {ensemble}, {var_id}.'
              ' Success file found.')
        return True

    #delete failed result
    rh.delete_result(job_id)

    # find files
    nc_files = find_files(model, ensemble, var_id)

    # check data is valid
    if not nc_files:
        rh.insert_failure(job_id, 'bad_data')

        print(f'[ERROR] No valid files for {var_id}')
        return False

    # check date range is valid
    validity = is_valid_range(nc_files)
    if not validity:
        rh.insert_failure(job_id, 'bad_num')

        print(f'[ERROR] File date range is invalid for {var_id}')
        return False

    # calculate the statistic
    statistic = calculate_statistic(nc_files, var_id, stat)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    statistic.to_netcdf(f'{output_path}/{var_id}.nc')
    output_file = f'{output_path}/{var_id}.nc'
    print(f'[INFO] Output file generated: {output_path}/{var_id}.nc')

    if not os.path.exists(output_file):
        os.rmdir(output_path)

        rh.insert_failure(job_id, 'no_output')

        print(f'[ERROR] Failed to generate output file: {output_path}/{var_id}.nc')
        return False

    # create success file
    rh.insert_success(job_id)

    rh.close()
    return True


def main():
    """Runs script if called on command line"""

    args = arg_parse_chunk()
    run_chunk(args)


if __name__ == '__main__':
    main()
