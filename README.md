# abcunit-cmip5-stats
Processing Framework for calculating temporal statistics from CMIP5 (using ABCUnit)

The statistics that can be calculated are the maximum, minimumm and mean.

The structure of the files is:

1. Run all script = `run_all.py`
* Calculates given statistic for chosen models, ensembles and variables
* These are given as arguments on the command line
* The statistic must be specified as an argument at the command line
* Defaults to running for all models, ensembles and variables
* For each model it runs the batch script

2. Run batch script = `run_batch.py`
* Calculates the statistic over one chosen model and chosen ensembles and variables
* Defaults to all ensembles and variables
* Model must be specified when run at the command line 
* Calls each ensemble as an argument for the chunk script
* The chunk script is submitted to LOTUS via `bsub`

3. Run chunk script = `run_chunk.py`
* Typically run on lotus but can be run from the command line
* Calculates the statstic for the specified model, ensemble and variable
* These must all be specified if run from the command line
* For each variable it:
    * Ignores if already calculated
    * Finds the necessary files
    * Checks the date range specified is valid
    * Calculates the statistic and writes to output file
    * Checks output file exists
    * Checks the sisze of the output file is as expected
    

