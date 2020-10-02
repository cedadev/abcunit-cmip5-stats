import glob
import os
import numpy as np
import functools
#from handler_interface import OutputInterface
import SETTINGS

class FileSystemAPI(object):

    def __init__(self, n_facets, sep, error_types):
        self.current_dir = os.getcwd()
        self.error_types = error_types
        self.n_facets = n_facets
        self.sep = sep
        self.success_dir = SETTINGS.SUCCESS_DIR.format(current_directory=self.current_dir)
        self.failure_dir = SETTINGS.FAILURE_DIR.format(current_directory=self.current_dir)

    def _path_to_identifier(self, path):
        path_arr = path.split(os.sep)
        trimmed_path = '/'.join(path_arr[-self.n_facets:])
        return trimmed_path.replace('/', self.sep)

    @validate # don't actually need because this is always called from a decorated function
    def _identifier_to_path(self, identifier, result):
        id_path = identifier.replace(self.sep, '/')
        if result == 'success':
            return os.path.join(self.success_dir, id_path)
        else:
            return os.path.join(self.failure_dir, result, id_path)

    def validate(func):
        @functools.wraps(func)
        def validate_identifier(*args, **kwargs):
            identifier = args[0]
            if '/' in identifier:
                raise ValueError
            return func(*args, **kwargs)
        return validate_identifier

    @validate
    def get_result(self, identifier):
        path = self._identifier_to_path(identifier, 'success')
        if os.path.exists(path):
            return 'success'
        
        for error in self.error_types:
            path = self._identifier_to_path(identifier, error)
            if os.path.exists(path):
                return error

        return None

    def get_all_results(self):
        results = {}
        for identifier in self.get_successful_runs():
            results[identifier] = 'success'

        error_dict = self.get_failed_runs()
        for (error_type, identifiers) in error_dict.items():
            for identifier in identifiers:
                results[identifier] = error_type

        return results

    def get_successful_runs(self):
        glob_pattern = os.path.join(self.success_dir, '/'.join(['*' for _ in range(self.n_facets)]))
        files = glob.glob(glob_pattern)
        return [self._path_to_identifier(fname) for fname in files]


    def get_failed_runs(self):
        failures = {}
        for error_type in self.error_types:
            glob_pattern = os.path.join(self.failure_dir, error_type, '/'.join(['*' for _ in range(self.n_facets)]))
            files = glob.glob(glob_pattern)
            failures[error_type] = [self._path_to_identifier(fname) for fname in files]
        
        return failures

    @validate
    def delete_result(self, identifier):
        path = self._identifier_to_path(identifier, 'success')
        if os.path.exists(path):
            os.unlink(path)
        
        for error in self.error_types:
            path = self._identifier_to_path(identifier, error)
            if os.path.exists(path):
                os.unlink(path)

    def delete_all_results(self):
        success_pattern = os.path.join(self.success_dir, '/'.join(['*' for _ in range(self.n_facets)]))
        failure_pattern = os.path.join(self.failure_dir, '/'.join(['*' for _ in range(self.n_facets + 1)]))   
        success_files = glob.glob(success_pattern)
        failure_files = glob.glob(failure_pattern)

        for success_file in success_files:
            os.unlink(success_file)

        for failure_file in failure_files:
            os.unlink(failure_file)

    @validate
    def ran_succesfully(self, identifier):
        path = self._identifier_to_path(identifier, 'success')
        return os.path.exists(path)

    def count_results(self):
        return len(self.get_all_results())

    def count_successes(self):
        return len(self.get_successful_runs())

    def count_failures(self):
        size = 0
        error_dict = self.get_failed_runs()
        for error in error_dict.keys():
            size += len(error_dict[error])
        return size

    @validate
    def insert_success(self, identifier):
        path = self._identifier_to_path(identifier, 'success')
        dr = os.path.dirname(path)

        if not os.path.isdir(dr): #Should there be a case for if it does?
            os.makedirs(dr)
        open(path, 'w') #empty success file

    @validate # could check error_type too
    def insert_failure(self, identifier, error_type):
        path = self._identifier_to_path(identifier, error_type)
        dr = os.path.dirname(path)

        if not os.path.isdir(dr): #Should there be a case for if it does?
            os.makedirs(dr) #used to be os.path.dirname(path) 
        with open(path, 'w') as writer:
            writer.write(f'{error_type} has occured!')
