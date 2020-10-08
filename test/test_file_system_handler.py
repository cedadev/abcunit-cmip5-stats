import pytest
from output_handler.file_system_handler import FileSystemHandler

fs_handler = None

def setup_module():
    global fs_handler
    print("SETTING UP")
    fs_handler = FileSystemHandler(5, '.', ['bad_data', 'bad_num', 'no_output'])

def teardown_module():
    print("TEARING DOWN")
    #fs_handler.delete_all_results()

def test_success_inserted():
    fs_handler.insert_success('mean.MOHC.HadGEM2-ES.r1i1p1.cLeaf')
    result = fs_handler.get_result('mean.MOHC.HadGEM2-ES.r1i1p1.cLeaf')
    assert(result == 'success')

def test_ran_successfully():
    fs_handler.insert_success('mean.MOHC.HadGEM2-ES.r1i1p1.cWood')
    assert(fs_handler.ran_succesfully('mean.MOHC.HadGEM2-ES.r1i1p1.cWood'))

def test_failure_inserted():
    fs_handler.insert_failure('mean.MOHC.HadGEM2-ES.r1i1p1.burntArea', 'bad_data')
    result = fs_handler.get_result('mean.MOHC.HadGEM2-ES.r1i1p1.burntArea')
    assert(result == 'bad_data')

def test_deletion_of_entry():
    fs_handler.insert_success('mean.MOHC.HadGEM2-ES.r1i1p1.cSoil')
    fs_handler.delete_result('mean.MOHC.HadGEM2-ES.r1i1p1.cSoil')
    result = fs_handler.get_result('mean.MOHC.HadGEM2-ES.r1i1p1.cSoil')
    assert(result == None)

def _unique_setup():
    fs_handler.delete_all_results()

    fs_handler.insert_success('min.CMCC.CMCC-CM.r2i1p1.fFire')
    fs_handler.insert_success('min.CMCC.CMCC-CM.r2i1p1.cVeg')
    fs_handler.insert_success('min.CMCC.CMCC-CM.r2i1p1.treeFracSecDec')
    fs_handler.insert_failure('min.CMCC.CMCC-CM.r2i1p1.fGrazing', 'bad_data')
    fs_handler.insert_failure('min.CMCC.CMCC-CM.r2i1p1.rGrowth', 'bad_num')

def test_counting():
    _unique_setup()

    total = fs_handler.count_results()
    total_success = fs_handler.count_successes()
    total_failures = fs_handler.count_failures()
    assert((total == 5) and (total_success == 3) and (total_failures == 2))

def test_get_successful_names():
    _unique_setup()
    
    success_results = ['min.CMCC.CMCC-CM.r2i1p1.fFire','min.CMCC.CMCC-CM.r2i1p1.cVeg',
                      'min.CMCC.CMCC-CM.r2i1p1.treeFracSecDec']
    assert(fs_handler.get_successful_runs() == success_results)

def test_get_failed_names():
    _unique_setup()

    failed_results = {
        "bad_data": ["min.CMCC.CMCC-CM.r2i1p1.fGrazing"],
        "bad_num": ["min.CMCC.CMCC-CM.r2i1p1.rGrowth"],
        "no_output": []
    }
    assert(fs_handler.get_failed_runs() == failed_results)

def test_get_result_dict():
    _unique_setup()

    correct_dict = {
        "min.CMCC.CMCC-CM.r2i1p1.fFire": "success",
        "min.CMCC.CMCC-CM.r2i1p1.cVeg": "success",
        "min.CMCC.CMCC-CM.r2i1p1.treeFracSecDec": "success",
        "min.CMCC.CMCC-CM.r2i1p1.fGrazing": "bad_data",
        "min.CMCC.CMCC-CM.r2i1p1.rGrowth": "bad_num"
    }
    assert(fs_handler.get_all_results() == correct_dict)


