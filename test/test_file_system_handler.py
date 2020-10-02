import pytest
from outputAPI.file_system_handler import FileSystemAPI

fs_api = None

def setup_module():
    global fs_api
    print("SETTING UP")
    fs_api = FileSystemAPI(5, '.', ['bad_data', 'bad_num', 'no_output'])

def teardown_module():
    print("TEARING DOWN")
    #fs_api.delete_all_results()

def test_success_inserted():
    fs_api.insert_success('mean.MOHC.HadGEM2-ES.r1i1p1.cLeaf')
    result = fs_api.get_result('mean.MOHC.HadGEM2-ES.r1i1p1.cLeaf')
    assert(result == 'success')

def test_ran_successfully():
    fs_api.insert_success('mean.MOHC.HadGEM2-ES.r1i1p1.cWood')
    assert(fs_api.ran_succesfully('mean.MOHC.HadGEM2-ES.r1i1p1.cWood'))

def test_failure_inserted():
    fs_api.insert_failure('mean.MOHC.HadGEM2-ES.r1i1p1.burntArea', 'bad_data')
    result = fs_api.get_result('mean.MOHC.HadGEM2-ES.r1i1p1.burntArea')
    assert(result == 'bad_data')

def test_deletion_of_entry():
    fs_api.insert_success('mean.MOHC.HadGEM2-ES.r1i1p1.cSoil')
    fs_api.delete_result('mean.MOHC.HadGEM2-ES.r1i1p1.cSoil')
    result = fs_api.get_result('mean.MOHC.HadGEM2-ES.r1i1p1.cSoil')
    assert(result == None)

def _unique_setup():
    fs_api.delete_all_results()

    fs_api.insert_success('min.CMCC.CMCC-CM.r2i1p1.fFire')
    fs_api.insert_success('min.CMCC.CMCC-CM.r2i1p1.cVeg')
    fs_api.insert_success('min.CMCC.CMCC-CM.r2i1p1.treeFracSecDec')
    fs_api.insert_failure('min.CMCC.CMCC-CM.r2i1p1.fGrazing', 'bad_data')
    fs_api.insert_failure('min.CMCC.CMCC-CM.r2i1p1.rGrowth', 'bad_num')

def test_counting():
    _unique_setup()

    total = fs_api.count_results()
    total_success = fs_api.count_successes()
    total_failures = fs_api.count_failures()
    assert((total == 5) and (total_success == 3) and (total_failures == 2))

def test_get_successful_names():
    _unique_setup()
    
    success_results = ['min.CMCC.CMCC-CM.r2i1p1.fFire','min.CMCC.CMCC-CM.r2i1p1.cVeg',
                      'min.CMCC.CMCC-CM.r2i1p1.treeFracSecDec']
    assert(fs_api.get_successful_runs() == success_results)

def test_get_failed_names():
    _unique_setup()

    failed_results = {
        "bad_data": ["min.CMCC.CMCC-CM.r2i1p1.fGrazing"],
        "bad_num": ["min.CMCC.CMCC-CM.r2i1p1.rGrowth"],
        "no_output": []
    }
    assert(fs_api.get_failed_runs() == failed_results)

def test_get_result_dict():
    _unique_setup()

    correct_dict = {
        "min.CMCC.CMCC-CM.r2i1p1.fFire": "success",
        "min.CMCC.CMCC-CM.r2i1p1.cVeg": "success",
        "min.CMCC.CMCC-CM.r2i1p1.treeFracSecDec": "success",
        "min.CMCC.CMCC-CM.r2i1p1.fGrazing": "bad_data",
        "min.CMCC.CMCC-CM.r2i1p1.rGrowth": "bad_num"
    }
    assert(fs_api.get_all_results() == correct_dict)


