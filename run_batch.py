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
    parser.add_argument('-m', '--model', nargs=1, type=str, default=model_choices,
                        required=True, help=f'Institue and model combination to run statistic on, '
                                            f'must be one of: {model_choices}', metavar='')
    parser.add_argument('-e', '--ensemble', type=str, default=ensemble_choices,
                        help=f'Ensemble to run statistic on, can be one or many of: '
                             f'{ensemble_choices}. Default is all ensembles.', metavar='',
                        nargs='*')
    parser.add_argument('-v', '--var_id', choices=variable_choices, default=variable_choices,
                        help=f'Variable to run statistic on, can be one or many of: '
                             f'{variable_choices}. Default is all variables', metavar='',
                        nargs='*')
    return parser.parse_args()


def loop_over_ensembles(args):
    """
    Submits run_chunk to lotus for each of the ensembles listed.

    :param args: (namespace) Namespace object built from attributes parsed from command line
    """

    # turn arguments into string
    model = ' '.join(args.model)
    stat = ' '.join(args.stat)
    variables = ' '.join(args.var_id)

    # iterate over each ensemble
    for ensemble in args.ensemble:
        print(f"Running for {ensemble}")

        # define lotus output file path
        current_directory = os.getcwd()  # get current working directory

        # define lotus output file path
        lotus_output_path = SETTINGS.LOTUS_OUTPUT_PATH_TMPL.format(
            current_directory=current_directory, stat=stat, model=model)

        # make output directory
        if not os.path.exists(lotus_output_path):
            os.makedirs(lotus_output_path)

        output_base = f"{lotus_output_path}/{ensemble}"

        # submit to lotus
        slurm_command = f"sbatch -p {SETTINGS.QUEUE} -t {SETTINGS.WALLCLOCK} -o " \
                       f"{output_base}.out -e {output_base}.err {current_directory}" \
                       f"/run_chunk.py -s {stat} -m {model} -e {ensemble} -v {variables}"
        subprocess.call(slurm_command, shell=True, env=os.environ)

        print(f"running {slurm_command}")


def main():
    """Runs script if called on command line"""

    args = arg_parse_batch()
    loop_over_ensembles(args)


if __name__ == '__main__':
    main()
