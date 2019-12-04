from lib import defaults
import glob
import xarray as xr
import argparse
import os

#parse command line
def arg_parse_batch():
    parser = argparse.ArgumentParser()
    stat_choices = ['min', 'max', 'mean']
    model_choices = defaults.models
    ensemble_choices = defaults.ensembles
    variable_choices = defaults.variables
    parser.add_argument('-s', '--stat', nargs=1, type=str, choices=stat_choices,
                        required=True, help=f'Type of statistic, must be one of: {stat_choices}', metavar='')
    parser.add_argument('-m', '--model', nargs=1, type=str, default=model_choices, required=True, help=f'Institue and model combination to run statistic on, must be one of: {model_choices}', metavar='')
    parser.add_argument('-e', '--ensemble', type=str, default=ensemble_choices, help=f'Ensemble to run statistic on, can be one or many of: {ensemble_choices}. Default is all ensembles.', metavar='')
    parser.add_argument('-v', '--var', choices=variable_choices, default=variable_choices, help=f'Variable to run statistic on, can be one or many of: {variable_choices}. Default is all variables', metavar='')
    return parser.parse_args()


#for each ensemble submit run_chunk to lotus
def loop_over_ensembles(args):
    current_directory = os.getcwd()
    #iterate over each ensemble
    for i in args.ensemble:
        print(f"Running for {i}")
        arg_list = argparse.Namespace(ensemble=[i], model=[args.model], stat=[args.stat], var=[args.var])
        run_batch.get_arguments(arg_list)
        
        #make output directory
        output_dir = f"{current_directory}/lotus_outputs/{args.stat}/{args.model}/"
        os.mkdir(output_dir)
        output_base = f"{output_dir}/{args.ensemble}"
        
        #submit to lotus
        bsub_command = f"bsub -q {defaults.queue} -W {defaults.wallclock} -o {output_base}.out -e {output_base}.err {current_directory}/run_chunk.py -s {arg.stat} -m {args.model} -e {i} -v {args.var}"
        os.system(bsub_command)
        print(f"running {bsub_command}")


#if run from run_all
def get_arguments(arg_list):
    loop_over_ensembles(arg_list)


def main():
    args = arg_parse_batch()
    loop_over_ensembles(args)



if __name__ == '__main__':
    main()