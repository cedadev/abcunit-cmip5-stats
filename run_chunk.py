from lib import defaults
import glob
import xarray as xr
import argparse


def arg_parse_chunk():
    parser = argparse.ArgumentParser()
    stat_choices = ['min', 'max', 'mean']
    model_choices = defaults.models
    ensemble_choices = defaults.ensembles
    variable_choices = defaults.variables
    parser.add_argument('-s', '--stat', nargs=1, type=str, choices=stat_choices,
                        required=True, help=f'Type of statistic, must be one of: {stat_choices}', metavar='')
    parser.add_argument('-m', '--model', nargs=1, type=str, choices=model_choices, required=True, help=f'Institue and model combination to run statistic on, must be one of: {model_choices}', metavar='')
    parser.add_argument('-e', '--ensemble', nargs=1, type=str, choices=ensemble_choices, required=True, help=f'Ensemble to run statistic on, must be one of: {ensemble_choices}', metavar='')
    parser.add_argument('-v', '--var', choices=variable_choices, default=variable_choices, help=f'Variable to run statistic on, can be one or many of: {variable_choices}. Default is all variables.', metavar='')
    return parser.parse_args()



def main():
    args = arg_parse_chunk()
    

if __name__ == '__main__':
    main()
