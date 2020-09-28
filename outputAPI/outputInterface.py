
class OutputInterface(object):

    def get_result(self, identifier):
        """ Returns a result given its identifier """
        raise NotImplementedError

    def get_all_results(self):
        """ Returns a dictionary of all ensembles 
        and their respective result """
        raise NotImplementedError

    def get_successful_runs(self):
        """ Returns a list of the names of all 
        successful runs """
        raise NotImplementedError

    def get_failed_runs(self):
        """ Returns a list of the names of all
        failed runs """
        raise NotImplementedError

    def delete_result(self, identifier):
        """ Deletes a result given its identifier """
        raise NotImplementedError

    def delete_all_results(self):
        """ Deletes all results """
        raise NotImplementedError

    def count_results(self):
        """ Returns the number of results in
        the file system / database """
        raise NotImplementedError

    def count_successes(self):
        """ Returns the number of successful results 
        in the file system / database """
        raise NotImplementedErrors

    def count_failures(self):
        """ Returns the number of failed results 
        in the file system / database """
        raise NotImplementedErrors

    def insert_success(self):
        """ Adds a successful result """
        raise NotImplementedErrors

    def insert_failure(self):
        """ Adds a failed result """
        raise NotImplementedErrors