EXIT_AFTER_N_FAILURES = 1000000

START_DATE = '1900-01-01'

END_DATE = '2000-01-01'

# lotus settings

QUEUE = 'short-serial'

WALLCLOCK = '00:10'

# Output path templates

LOTUS_OUTPUT_PATH_TMPL = "{current_directory}/logs/lotus_outputs/{stat}/{model}"
OUTPUT_PATH_TMPL = "{GWS}/{USER}/abcunit-outputs"
SUCCESS_DIR = "{current_directory}/logs/success"
FAILURE_DIR = "{current_directory}/logs/failure"

# choice for output handling

BACKEND = 'db' #'db' or 'file'
