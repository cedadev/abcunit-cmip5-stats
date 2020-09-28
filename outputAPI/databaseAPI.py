import psycopg2
from outputInterface import OutputInterface

class DataBaseAPI(OutputInterface):

    def __init__(self, connection_info, table_name='results'):
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
            return None #probably a way better thing to do than this

    def get_all_results(self):
        query = f"SELECT * FROM {self.tablename}"
        self.cur.execute(query)
        result_dict = {}
        for (name, result) in self.cur:
            result_dict[name] = result
        return result_dict

    def get_successful_runs(self):
        query = f"SELECT id FROM {self.tablename} " \
                "WHERE result='SUCCESS';"
        self.cur.execute(query)
        return [name[0] for name in self.cur]

    def get_failed_runs(self):
        query = f"SELECT id FROM {self.tablename} " \
                "WHERE result<>'SUCCESS';"
        self.cur.execute(query)
        return [name[0] for name in self.cur]

    def delete_result(self, identifier):
        query = f"DELETE FROM {self.tablename} " \
                f"WHERE id='{identifier}';"
        self.cur.execute(query)
        self.conn.commit()

    def delete_all_results(self):
        self.cur.execute(f"DROP TABLE {self.tablename};")
        self.conn.commit()

    def count_results(self):
        self.cur.execute(f"SELECT COUNT(*) FROM {self.tablename};")
        return self.cur.fetchone()[0]

    def count_successes(self):
         query = f"SELECT COUNT(*) FROM {self.tablename} " \
                "WHERE result='SUCCESS';"
        self.cur.execute(query)
        return self.cur.fetchone()[0]

    def count_failures(self):
        query = f"SELECT COUNT(*) FROM {self.tablename} " \
                "WHERE result<>'SUCCESS';"
        self.cur.execute(query)
        return self.cur.fetchone()[0]

    def insert_success(self, identifier):
        query = f"INSERT INTO {self.tablename} " \
                f"VALUES ('{identifier}', 'SUCCESS');"s
        self.cur.execute(query)
        self.conn.commit()

    def insert_failure(self, identifier, error_type):
        if error_type != 'SUCCESS':
            query = f"INSERT INTO {self.tablename} " \
                    f"VALUES ('{identifier}', '{error_type}');"
            self.cur.execute(query)
            self.conn.commit()
        #Don't know what to do in theother case
            
        


    
