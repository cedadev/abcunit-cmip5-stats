#!/usr/bin/env python

"""This script takes arguments from the command line and runs the function
run_unit for each of the variables provided as an argument or for
all variables if none were provided."""

import sys
import os
import glob
import argparse
import xarray as xr

from lib import defaults
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

    # define output file paths
    current_directory = os.getcwd()  # get current working directory

    output_path = SETTINGS.OUTPUT_PATH_TMPL.format(
        current_directory=current_directory, stat=stat, model=model, ensemble=ensemble)
    success_path = SETTINGS.SUCCESS_PATH_TMPL.format(
        current_directory=current_directory, stat=stat, model=model, ensemble=ensemble)
    bad_data_path = SETTINGS.BAD_DATA_PATH_TMPL.format(
        current_directory=current_directory, stat=stat, model=model, ensemble=ensemble)
    bad_num_path = SETTINGS.BAD_DATA_PATH_TMPL.format(
        current_directory=current_directory, stat=stat, model=model, ensemble=ensemble)
    no_output_path = SETTINGS.NO_OUTPUT_PATH_TMPL.format(
        current_directory=current_directory, stat=stat, model=model, ensemble=ensemble)

    # check for success file - if exists - continue
    success_file = f'{success_path}/{var_id}.nc.txt'

    if os.path.exists(success_file):
        print(f'[INFO] Already ran for {stat}, {model}, {ensemble}, {var_id}.'
              ' Success file found.')
        return 

    # delete previous failure files
    bad_data_file = f'{bad_data_path}/{var_id}.nc.txt'
    if os.path.exists(bad_data_file):
        os.unlink(bad_data_file)

    bad_num_file = f'{bad_num_path}/{var_id}.nc.txt'
    if os.path.exists(bad_num_file):
        os.unlink(bad_num_file)

    no_output_file = f'{no_output_path}/{var_id}.nc.txt'
    if os.path.exists(no_output_file):
        os.unlink(no_output_file)

    # find files
    nc_files = find_files(model, ensemble, var_id)

    # check data is valid
    if not nc_files:

        if not os.path.exists(bad_data_path):
            os.makedirs(bad_data_path)

        open(os.path.join(bad_data_path, f'{var_id}.nc.txt'), 'w')  # creates empty file

        print(f'[ERROR] No valid files for {var_id}')
        return False

    # check date range is valid
    validity = is_valid_range(nc_files)
    if not validity:

        if not os.path.exists(bad_num_path):
            os.makedirs(bad_num_path)

        open(os.path.join(bad_num_path, f'{var_id}.nc.txt'), 'w')
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

        if not os.path.exists(no_output_path):
            os.makedirs(no_output_path)

        open(os.path.join(no_output_path, f'{var_id}.nc.txt'), 'w')

        print(f'[ERROR] Failed to generate output file: {output_path}/{var_id}.nc')
        return False

    # create success file
    if not os.path.exists(success_path):
        os.makedirs(success_path)

    open(os.path.join(success_path, f'{var_id}.nc.txt'), 'w')


def main():
    """Runs script if called on command line"""

    args = arg_parse_chunk()
    run_chunk(args)


if __name__ == '__main__':
    main()
