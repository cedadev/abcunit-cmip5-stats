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
    """Parses arguments given at the command line"""
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
    parser.add_argument('-v', '--var', choices=variable_choices, default=variable_choices,
                        help=f'Variable to run statistic on, can be one or many of: '
                             f'{variable_choices}. Default is all variables.', metavar='',
                        nargs='*')
    return parser.parse_args()


def define_file_paths(stat, model, ensemble, var):
    """Defines output, success and failure file paths"""
    # define paths as absolute paths
    current_directory = os.getcwd()
    arguments = f"{stat}/{model}/{ensemble}"
    output_file_path = f"{current_directory}/outputs/{arguments}"
    success_file_path = f"{current_directory}/success/{arguments}"
    bad_data_file_path = f"{current_directory}/bad_data/{arguments}"
    bad_num_file_path = f"{current_directory}/bad_num/{arguments}"
    no_output_file_path = f"{current_directory}/no_output/{arguments}"
    return (output_file_path, success_file_path, bad_data_file_path,
            bad_num_file_path, no_output_file_path)


def find_files(model, ensemble, var):
    """Finds files that correspond to the given arguments"""
    pattern = '/badc/cmip5/data/cmip5/output1/{model}/historical/mon/land' \
              '/Lmon/{ensemble}/latest/{var}/*.nc'
    glob_pattern = pattern.format(model=model,
                                  ensemble=ensemble, var=var)
    nc_files = glob.glob(glob_pattern)
    print(f'[INFO] found files: {nc_files}')
    return nc_files


def is_valid_range(nc_files, start=SETTINGS.start_date, end=SETTINGS.end_date):
    """Checks the date range is valid for the given NetCDF files"""
    try:
        ds = xr.open_mfdataset(nc_files)
        times_in_range = ds.time.loc[start:end]

        n_req_times = 100 * 12  # yrs * months
        assert len(times_in_range) == n_req_times

        print('[INFO] Range is valid')
        return True

    except Exception as err:
        print('[ERROR] Range is invalid')
        return False


def calculate_statistic(nc_files, var, stat):
    """Calculates the required statistic for each variable for each ensemble
    and model requested."""
    dataset = xr.open_mfdataset(nc_files)
    stat = str(stat)
    if stat == 'mean':
        mean = dataset[var].mean(dim='time')
        return mean
    if stat == 'max':
        maximum = dataset[var].max(dim='time')
        return maximum
    if stat == 'min':
        minimum = dataset[var].max(dim='time')
        return minimum


def run_unit(args, failure_count):
    """Loops over each variable listed to calculate the statistic.
    Keeps track of whether the job was successful or not and writes the
    result of the statistic to an output file."""

    # turn arguments into string

    ensemble = str(args.ensemble).strip("[] \' ")
    model = str(args.model).strip("[] \'")
    stat = str(args.stat).strip("[] \'")


    for var in args.var:
        # exit if too many failures

        if failure_count >= SETTINGS.exit_after_n_failures:
            print('[ERROR] Maximum failure count met')
            sys.exit(1)

        # get file paths
        file_paths = define_file_paths(stat, model, ensemble, var)

        # check for success file - if exists - continue
        success_path = f'{file_paths[1]}/{var}.nc.txt'
        if os.path.exists(success_path):
            print(f'[INFO] Already ran for {stat}, {model}, {ensemble}, {var}.'
                  ' Success file found')
            continue

        # delete previous failure files
        bad_data_path = f'{file_paths[2]}/{var}.nc.txt'
        if os.path.exists(bad_data_path):
            os.unlink(bad_data_path)

        bad_num_path = f'{file_paths[3]}/{var}.nc.txt'
        if os.path.exists(bad_num_path):
            os.unlink(bad_num_path)

        no_output_path = f'{file_paths[4]}/{var}.nc.txt'
        if os.path.exists(no_output_path):
            os.unlink(no_output_path)

        # find files
        nc_files = find_files(model, ensemble, var)

        # check data is valid
        if not nc_files:
            if not os.path.exists(file_paths[2]):
                os.makedirs(file_paths[2])
            f = open(os.path.join(file_paths[2], f'{var}.nc.txt'), 'w') # creates empty file
            print(f'[ERROR] No valid files for {var}')
            failure_count += 1
            continue

        # check date range is valid
        validity = is_valid_range(nc_files)
        if not validity:
            if not os.path.exists(file_paths[3]):
                os.makedirs(file_paths[3])
            open(os.path.join(file_paths[3], f'{var}.nc.txt'), 'w')
            failure_count += 1
            continue

        # calculate the statistic
        statistic = calculate_statistic(nc_files, var, stat)
        if not os.path.exists(file_paths[0]):
            os.makedirs(file_paths[0])
        statistic.to_netcdf(f'{file_paths[0]}/{var}.nc')
        output_path = f'{file_paths[0]}/{var}.nc'
        print(f'[INFO] Output file generated: {file_paths[0]}/{var}.nc')
        if not os.path.exists(output_path):
            os.rmdir(file_paths[0])
            if not os.path.exists(file_paths[4]):
                os.makedirs(file_paths[4])
            open(os.path.join(file_paths[4], f'{var}.nc.txt'), 'w')
            failure_count += 1
            print(f'[ERROR] Failed to generate output file: {file_paths[0]}/{var}.nc')
            continue

        # create success file
        if not os.path.exists(file_paths[1]):
            os.makedirs(file_paths[1])
        open(os.path.join(file_paths[1], f'{var}.nc.txt'), 'w')

    print(f"Completed job")


def main():
    """Runs script if called on command line"""

    # define global variables

    # keep track of failures. Many failures expected for this example so the
    # limit is set high
    # good practice to include this
    failure_count = 0

    args = arg_parse_chunk()
    run_unit(args, failure_count)


if __name__ == '__main__':
    main()
