# abcunit-cmip5-stats
Processing Framework for calculating temporal statistics from CMIP5 (using ABCUnit).

## Overview ##

The name ABCunit corresponds to the 4 layers the workflow is split in to:
1. A - all
2. B - batch
3. C - chunk
4. The Unit

These scripts are an example of using the ABCUnit structure on CMIP5 data. This provides a repteable and efficient workflow.

The statistics that can be calculated are the maximum, minimum and mean.

The models, ensembles and variables available can be found in `lib/defaults.py`

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
* Defaults to all variables
* For each variable it: 
    * Ignores if already calculated
    * Finds the necessary files
    * Checks the date range specified is valid
    * Calculates the statistic and writes to output file
    * Checks output file exists
    
## Example usage ##

Log in to a JASMIN sci server:

`ssh <user-id>@jasmin-sci5.ceda.ac.uk`

### Edit these files to match your setup: ###

* `SETTINGS.py`
* `setup-env.sh`

Clone this repositroy and make sure you are in the top level abcunit-cmip5-stats directory:

* `https://github.com/cedadev/abcunit-cmip5-stats.git`
* `cd abcunit-cmip5-stats`

***First run the*** `setup-env.sh` ***script to setup up your environment.***

Options for models, ensembles and variables can be found in `lib/defaults.py`. Note that the model is defined by its institute/model combination.

Running the top level 'run all' script at the command line:

`python run_all.py -s mean` 

Running the 'run batch' script:

`python run_batch.py -s mean -m MOHC/HadGEM2-ES`

Running the 'run chunk' script locally, instead of using LOTUS, which is how it is invoked in the batch script:

`python run_chunk.py -s mean -m MOHC/HadGEM2-ES -e r1i1p1`

In each example, all other arguments are optional and can be included. 
For example, to calculate the mean of only 2 variables for in one model and ensemble:

`python run_chunk.py -s mean -m MOHC/HadGEM2-ES -e r1i1p1 -v rh ra`

## Log Handling and Outputs ##

Currently the system supports two different ways to log successes and failures of jobs, output to the file system or using a database. One of these methods can be chosen in the settings file with the BACKEND variable.

### File system logs ###

If using the file system log handler, log files will be outputted in the following way. Each job will result in a file with a success path or failure path in the following formats:

`<current-directory>/logs/success/<stat>/<model>/<ensemble>/<var_id>`

`<current-directory>/logs/failure/<failure-type>/<stat>/<model>/<ensemble>/<var_id>`
   
* current-directory is the directory you are in when running the python scripts.
* failure-type can be one of:
   * bad_data - Empty file produced when no netCDF files could be found for the chosen arguments.
   * bad_num - Empty file produced when the chosen date range is invalid for the chosen files.
   * no_output - Empty file produced when the output file could not be generated.

### Database logs ###

If using the database log handler, success / failure logs will be output into a relation (named 'results' by default) in the following format:

| id                                    |   result |
| :------------------------------------ | -------: |
| mean.MOHC.HadGEM2-ES.r1i1p1.shrubFrac |  success |
| mean.MOHC.HadGEM2-ES.r1i1p1.tran      | bad_data |
| mean.MOHC.HadGEM2-ES.r1i1p1.treeFrac  |  success |

To use this handler you will need to do the following setup:

1. Contact the JASMIN help desk and ask for a postgresql database to be made for you
2. Create an environment variable called ABCUNIT_DB_SETTINGS which stores a connection string for `psycopg2`, for example:
   * `export ABCUNIT_DB_SETTINGS="dbname=<database_name> user=<user_name> host=<host_name> password=<database_password>"`

Its useful to setup the variable in a script separate from your public code. 

### Outputs ###

Lotus outputs are in the following format:

`<current-directory>/logs/lotus-outputs/<stat>/<model>/<ensemble>.out or <ensemble>.err`

If a job is successful, its corresponding netcdf4 file will be output to:

`<gws>/<user>/abcunit-outputs/<var_id>.nc`

Where `gws` is a path to a group workspace and `user` is your username. Netcdf4 files are output to a group workspace to more effectivley use storage space. 
