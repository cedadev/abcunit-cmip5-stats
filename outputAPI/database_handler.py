import psycopg2
#from handler_interface import OutputInterface

class DataBaseAPI(object):

    def __init__(self, connection_info, error_types, table_name='results'):
        """ 
        Returns an instace of the database handler api.
        
        :param connection_info: (str) Connection string in the psycopg2 format,
        "dbname=<db_name> user=<user_name> password=<password>".
        :param error_types: (list) List of the string names of the types of errors that can occur.
        :param table_name: (str) Optional string for the name of the table created (default 'results')
        """
        self.error_types = error_types
        self.conn = psycopg2.connect(connection_info)
        self.cur = self.conn.cursor()
        self.tablename = tablename
        self._create_table()

    def _create_table(self):
        self.cur.execute(f'CREATE TABLE IF NOT EXISTS {self.tablename}' \
             '(id varchar(255) PRIMARY KEY, result varchar(255) NOT NULL);')
        self.conn.commit()

    def _delete_table(self):
        self.cur.execute(f"DROP TABLE {self.tablename};")
        self.conn.commit()

    def get_result(self, identifier):
        query = f"SELECT result FROM {self.tablename} " \
        f"WHERE id='{identifier}';"
        self.cur.execute(query)
        if self.cur.rowcount > 0:
            return self.cur.fetchone()[0]
        else:
            return None

    def get_all_results(self):
        query = f"SELECT * FROM {self.tablename}"
        self.cur.execute(query)
        result_dict = {}
        for (name, result) in self.cur:
            result_dict[name] = result
        return result_dict

    def get_successful_runs(self):
        query = f"SELECT id FROM {self.tablename} " \
                "WHERE result='success';"
        self.cur.execute(query)
        return [name[0] for name in self.cur]

    def get_failed_runs(self):
        query = f"SELECT id, result FROM {self.tablename} " \
                "WHERE result<>'success';"
        self.cur.execute(query)
        failures = dict([(key, []) for key in self.error_types])
        for (name, result) in self.cur:
            failures[result].append(name)
        return failures

    def delete_result(self, identifier):
        query = f"DELETE FROM {self.tablename} " \
                f"WHERE id='{identifier}';"
        self.cur.execute(query)
        self.conn.commit()

    def delete_all_results(self):
        self.cur.execute(f"DELETE FROM {self.tablename};")
        self.conn.commit()

    def ran_succesfully(self, identifier):
        query = f"SELECT result FROM {self.tablename} " \
        f"WHERE id='{identifier}';"
        self.cur.execute(query)
        return self.cur.fetchone()[0] == 'success'

    def count_results(self):
        self.cur.execute(f"SELECT COUNT(*) FROM {self.tablename};")
        return self.cur.fetchone()[0]

    def count_successes(self):
        query = f"SELECT COUNT(*) FROM {self.tablename} " \
                "WHERE result='success';"
        self.cur.execute(query)
        return self.cur.fetchone()[0]

    def count_failures(self):
        query = f"SELECT COUNT(*) FROM {self.tablename} " \
                "WHERE result<>'success';"
        self.cur.execute(query)
        return self.cur.fetchone()[0]

    def insert_success(self, identifier):
        query = f"INSERT INTO {self.tablename} " \
                f"VALUES ('{identifier}', 'success');"
        self.cur.execute(query)
        self.conn.commit()

    def insert_failure(self, identifier, error_type):
        query = f"INSERT INTO {self.tablename} " \
                f"VALUES ('{identifier}', '{error_type}');"
        self.cur.execute(query)
        self.conn.commit()

    def close_connection(self):
        self.cur.close()
        self.conn.close()
