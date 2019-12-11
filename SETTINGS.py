EXIT_AFTER_N_FAILURES = 1000000

START_DATE = '1900-01-01'

END_DATE = '2000-01-01'

# lotus settings

QUEUE = 'short-serial'

WALLCLOCK = '00:10'

# Output path templates

LOTUS_OUTPUT_PATH_TMPL = "{current_directory}/ALL_OUTPUTS/lotus_outputs/{stat}/{model}"

OUTPUT_PATH_TMPL = "{current_directory}/ALL_OUTPUTS/outputs/{stat}/{model}/{ensemble}"
SUCCESS_PATH_TMPL = "{current_directory}/ALL_OUTPUTS/success/{stat}/{model}/{ensemble}"
BAD_DATA_PATH_TMPL = "{current_directory}/ALL_OUTPUTS/bad_data/{stat}/{model}/{ensemble}"
BAD_NUM_PATH_TMPL = "{current_directory}/ALL_OUTPUTS/bad_num/{stat}/{model}/{ensemble}"
NO_OUTPUT_PATH_TMPL = "{current_directory}/ALL_OUTPUTS/no_output/{stat}/{model}/{ensemble}"


