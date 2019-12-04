import sys

from lib import defaults
import glob
import xarray as xr
import argparse
import run_batch


def arg_parse_all():
    parser = argparse.ArgumentParser()
    stat_choices = ['min', 'max', 'mean']
    model_choices = defaults.models
    ensemble_choices = defaults.ensembles
    variable_choices = defaults.variables
    parser.add_argument('-s', '--stat', nargs=1, type=str, choices=stat_choices, required=True,
                        help=f'Type of statistic, must be one of: {stat_choices}', metavar='')
    parser.add_argument('-m', '--model', type=str, default=model_choices, help=f'Institue and model combination to run statistic on, can be one or many of: {model_choices}. Default is all models.', metavar='')
    parser.add_argument('-e', '--ensemble', type=str, default=ensemble_choices, help=f'Ensemble to run statistic on, can be one or many of: {ensemble_choices}. Default is all ensembles.', metavar='')
    parser.add_argument('-v', '--var', choices=variable_choices, default=variable_choices, help=f'Variable to run statistic on, can be one or many of: {variable_choices}. Default is all variables.', metavar='')
    return parser.parse_args()


#run run_batch for each of the models listed
def loop_over_models(args):
    #iterate over models 
    for i in args.model:
        print(f"Running for {i}")
        arg_list = argparse.Namespace(ensemble=[args.ensemble], model=[i], stat=[args.stat], var=[args.var])
        run_batch.get_arguments(arg_list)


def main():
    args = arg_parse_all()
    print(f"Finding {args.stat} of {args.var} for {args.model}, {args.ensemble}.")
    loop_over_arguments(args)



if __name__ == '__main__':
    main()