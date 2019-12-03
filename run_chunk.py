
from lib import defaults
import glob
import xarray as xr
import argparse


def arg_parse_chunk():
        parser = argparse.ArgumentParser()

        parser.add_argument('-s', '--stat', nargs=1)
        parser.add_argument('-m', '--model', nargs='*', default=defaults.models)
        parser.add_argument('-e', '--ensemble', nargs='*', default = defaults.ensembles)
        parser.add_argument('-v', '--var', default = defaults.variables)
        return parser.parse_args()


def are_valid_arguments(args):

        if args.stat in ['mean', 'max', 'min']:
                print('statistic is valid')


def main():
        args = arg_parse_chunk()


if __name__ == '__main__':
        main()
