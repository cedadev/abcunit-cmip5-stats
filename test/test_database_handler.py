import pytest
import os
from outputAPI.database_handler import DataBaseAPI

CONNECTION_DETAILS = os.environ["ABCUNIT_DB_SETTINGS"]
db_api = None

def setup_module():
    global db_api
    print("SETTING UP")
    db_api = DataBaseAPI(CONNECTION_DETAILS, ['bad_data', 'bad_num', 'no_output'], 'test_results')
    db_api._delete_table()
    db_api._create_table()

def teardown_module():
    print("TEARING DOWN")
    db_api._delete_table()
    db_api.close()

def test_success_inserted():
    db_api.insert_success('mean/MOHC/HadGEM2-ES/r1i1p1/cLeaf')
    result = db_api.get_result('mean/MOHC/HadGEM2-ES/r1i1p1/cLeaf')
    assert(result == 'success')

def test_ran_successfully():
    db_api.insert_success('mean/MOHC/HadGEM2-ES/r1i1p1/cWood')
    assert(db_api.ran_succesfully('mean/MOHC/HadGEM2-ES/r1i1p1/cWood'))

def test_failure_inserted():
    db_api.insert_failure('mean/MOHC/HadGEM2-ES/r1i1p1/burntArea', 'bad_data')
    result = db_api.get_result('mean/MOHC/HadGEM2-ES/r1i1p1/burntArea')
    assert(result == 'bad_data')

def test_deletion_of_entry():
    db_api.insert_success('mean/MOHC/HadGEM2-ES/r1i1p1/cSoil')
    db_api.delete_result('mean/MOHC/HadGEM2-ES/r1i1p1/cSoil')
    result = db_api.get_result('mean/MOHC/HadGEM2-ES/r1i1p1/cSoil')
    assert(result == None)

def _unique_setup():
    db_api._delete_table() #reset table for this
    db_api._create_table()

    db_api.insert_success('min/CMCC/CMCC-CM/r2i1p1/fFire')
    db_api.insert_success('min/CMCC/CMCC-CM/r2i1p1/cVeg')
    db_api.insert_success('min/CMCC/CMCC-CM/r2i1p1/treeFracSecDec')
    db_api.insert_failure('min/CMCC/CMCC-CM/r2i1p1/fGrazing', 'bad_data')
    db_api.insert_failure('min/CMCC/CMCC-CM/r2i1p1/rGrowth', 'bad_num')

def test_counting():
    _unique_setup()

    total = db_api.count_results()
    total_success = db_api.count_successes()
    total_failures = db_api.count_failures()
    assert((total == 5) and (total_success == 3) and (total_failures == 2))

def test_get_successful_names():
    _unique_setup()
    
    success_results = ['min/CMCC/CMCC-CM/r2i1p1/fFire','min/CMCC/CMCC-CM/r2i1p1/cVeg',
                      'min/CMCC/CMCC-CM/r2i1p1/treeFracSecDec']
    assert(db_api.get_successful_runs() == success_results)

def test_get_failed_names():
    _unique_setup()

    failed_results = {
        "bad_data": ["min/CMCC/CMCC-CM/r2i1p1/fGrazing"],
        "bad_num": ["min/CMCC/CMCC-CM/r2i1p1/rGrowth"],
        "no_output": []
    }
    assert(db_api.get_failed_runs() == failed_results)

def test_get_result_dict():
    _unique_setup()

    correct_dict = {
        "min/CMCC/CMCC-CM/r2i1p1/fFire": "success",
        "min/CMCC/CMCC-CM/r2i1p1/cVeg": "success",
        "min/CMCC/CMCC-CM/r2i1p1/treeFracSecDec": "success",
        "min/CMCC/CMCC-CM/r2i1p1/fGrazing": "bad_data",
        "min/CMCC/CMCC-CM/r2i1p1/rGrowth": "bad_num"
    }
    assert(db_api.get_all_results() == correct_dict)


