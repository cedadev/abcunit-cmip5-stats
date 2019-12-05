"""This script takes arguments from the command line and runs the function
run_unit for each of the variables provided as an argument or for
all variables if none were provided."""

import glob
import argparse
import xarray as xr

from lib import defaults

#parse command line and check all arguments are valid
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
                             f'{variable_choices}. Default is all variables.', metavar='')
    return parser.parse_args()


def loop_over_variables(args):
    """Runs the function run_unit for each of the variables listed"""
    #iterate over variables
    for i in args.var:
        arg_list = argparse.Namespace(ensemble=[args.ensemble], model=[args.model],
                                      stat=[args.stat], var=[i])
        run_unit(arg_list)


#def run_unit(args):
    """Calculates the required statistic for each variable for each ensemble and model requested.
    Keeps track of whether the job was successful or not and writes the result to an output
    file."""
    #define paths as absolute paths
    #output_file_path =
    #success_file_path =
    #failure_file_path =


def main():
    """Runs script if called on command line"""
    args = arg_parse_chunk()
    loop_over_variables(args)



if __name__ == '__main__':
    main()
