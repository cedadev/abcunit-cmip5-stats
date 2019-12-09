# abcunit-cmip5-stats
Processing Framework for calculating temporal statistics from CMIP5 (using ABCUnit)

The statistics that can be calculated are the maximum, minimum and mean.

## Structure ##

1. Run all script = `run_all.py`
* Calculates given statistic for chosen models, ensembles and variables
* These are given as arguments on the command line
* Statistic must be specified as an argument at the command line
* Defaults to running for all models, ensembles and variables
* For each model it runs the batch script

2. Run batch script = `run_batch.py`
* Calculates the statistic over one chosen model and chosen ensembles and variables
* Defaults to all ensembles and variables
* Statistic and model must be specified when run at the command line 
* Calls each ensemble as an argument for the chunk script
* The chunk script is submitted to LOTUS via `bsub`

3. Run chunk script = `run_chunk.py`
* Typically run on lotus but can be run from the command line
* Calculates the statstic for the specified model, ensemble and variables
* Statistic, model and ensemble must all be specified if run from the command line
* For each variable it:
    * Ignores if already calculated
    * Finds the necessary files
    * Checks the date range specified is valid
    * Calculates the statistic and writes to output file
    * Checks output file exists
    * Checks the size of the output file is as expected
    
## Example usage ##

### Edit these files to match your setup: ###

* `SETTINGS.py`
* `setup-env.sh`

***First run the*** `setup-env.sh` ***script to setup up your environment.***

Options for models, ensembles and variables can be found in `lib/defaults.py`. Note that the model is defined by its <institute>/<model> combination.

Running the top level 'run all' script at the command line:

`python run_all.py -s mean` 

Running the 'run batch' script:

`python run_batch.py -s mean -m MOHC/HadGEM2-ES`

Running the 'run chunk' script locally, instead of using LOTUS, which is how it is invoked in the batch script:

`python run_chunk.py -s mean -m MOHC/HadGEM2-ES -e r1i1p1`

In each example, all other arguments are optional and can be included.

## Outputs ##

The outputs - success files, failure files and resulting netCDF file if the job is successful are stored in directories with the following structure:

`current-directory/output-type/stat/model/ensemble/var.nc(.txt)`
   
* current-directory is the directory containing the python scripts.
* output-type can be one of:
   * outputs - The netCDF file corresponding to the chosen statistic.
   * success - Empty file produced when the job is successful.
   * bad_data - Empty file produced when no netCDF files could be found for the chosen arguments.
   * bad_num - Empty file produced when the chosen date range is invalid for the chosen files.
   * no_output - Empty file produced when the output file could not be generated.
   
The lotus outputs follow a similar pattern:

`current-directory/output-type/stat/model/ensemble.out or ensemble.err`

   
   
