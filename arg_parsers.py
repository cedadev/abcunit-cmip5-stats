import argparse
from lib import defaults


def parse_args_stat():
    parser = argparse.ArgumentParser()
    stat_choices = ['min', 'mean', 'max']
    parser.add_argument('-s', '--stat', type=str, choices=stat_choices, required=True,
                        help=f'Type of statistic, one of: {stat_choices}')
    return parser.parse_args()

def parse_args_two():
    parser = argparse.ArgumentParser()
    stat_choices = ['min', 'max', 'mean']
    model_choices = defaults.models
    parser.add_argument('-s', '--stat', nargs=1, type=str, choices=stat_choices,
                        required=True, help=f'Type of statistic, one of: {stat_choices}')
    parser.add_argument('-m', '--model', nargs=1, type=str, choices=model_choices, required=True, help=f'Institue and model combination to run statistic on, one of: {model_choices}')
    return parser.parse_args()


if __name__ == '__main__':
    parse_args_stat()
    parse_args_two()