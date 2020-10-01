import psycopg2
from handler_interface import OutputInterface

class DataBaseAPI(OutputInterface):

    def __init__(self, connection_info, error_types, table_name='results'):
        self.error_types = error_types
        info = connection_info.split(' ')
        command = f'dbname={info[0]} user={info[1]} password={info[2]}'
        self.conn = psycopg2.connect(command)
        self.cur = self.conn.cursor()
        self.tablename = tablename
        self._create_table()

    def _create_table(self):
        self.cur.execute(f'CREATE TABLE IF NOT EXISTS {self.tablename}' \
             '(id varchar(255) PRIMARY KEY, result varchar(255) NOT NULL);')

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

    def close_conection(self):
        self.cur.close()
        self.conn.close()
