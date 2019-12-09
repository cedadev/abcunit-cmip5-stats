#!/usr/bin/env python

"""This script takes arguments from the command line and submits the script
run_chunk to lotus for each of the ensembles provided as an argument or for
all ensembles if none were provided."""


import argparse
import os
#import xarray as xr
import subprocess

from lib import defaults
import SETTINGS


def arg_parse_batch():
    """Parses arguments given at the command line"""
    parser = argparse.ArgumentParser()
    stat_choices = ['min', 'max', 'mean']
    model_choices = defaults.models
    ensemble_choices = defaults.ensembles
    variable_choices = defaults.variables
    parser.add_argument('-s', '--stat', nargs=1, type=str, choices=stat_choices,
                        required=True, help=f'Type of statistic, must be one of: '
                                            f'{stat_choices}', metavar='')
    parser.add_argument('-m', '--model', nargs=1, type=str, default=model_choices,
                        required=True, help=f'Institue and model combination to run statistic on, '
                                            f'must be one of: {model_choices}', metavar='')
    parser.add_argument('-e', '--ensemble', type=str, default=ensemble_choices,
                        help=f'Ensemble to run statistic on, can be one or many of: '
                             f'{ensemble_choices}. Default is all ensembles.', metavar='',
                        nargs='*')
    parser.add_argument('-v', '--var', choices=variable_choices, default=variable_choices,
                        help=f'Variable to run statistic on, can be one or many of: '
                             f'{variable_choices}. Default is all variables', metavar='',
                        nargs='*')
    return parser.parse_args()



def loop_over_ensembles(args):
    """Submits run_chunk to lotus for each of the ensembles listed"""
    current_directory = os.getcwd()

    model = str(args.model).strip("[] \'")
    stat = str(args.stat).strip("[] \'")
    vars = str(args.var).strip("[]").replace(",", "")

    # iterate over each ensemble
    for ensemble in args.ensemble:
        print(f"Running for {ensemble}")

        # make output directory
        lotus_output_dir = f"{current_directory}/lotus_outputs/{stat}/{model}"
        if not os.path.exists(lotus_output_dir):
            os.makedirs(lotus_output_dir)
        output_base = f"{lotus_output_dir}/{ensemble}"

        # submit to lotus
        bsub_command = f"bsub -q {SETTINGS.queue} -W {SETTINGS.wallclock} -o " \
                       f"{output_base}.out -e {output_base}.err {current_directory}" \
                       f"/run_chunk.py -s {stat} -m {model} -e {ensemble} -v {vars}"
        subprocess.call(bsub_command, shell=True)
        print(f"running {bsub_command}")


def main():
    """Runs script if called on command line"""
    args = arg_parse_batch()
    loop_over_ensembles(args)


if __name__ == '__main__':
    main()
