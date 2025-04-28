import pandas as pd
import subprocess
import sys
import io

class DB2EXCEL:
    """
    Extract data from various databases and export to Excel.
    Supports MySQL, MS-SQL via pyodbc or pymssql.
    """

    @staticmethod
    def install_and_import(package_name, import_name=None):
        name = import_name or package_name
        try:
            module = __import__(name)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            module = __import__(name)
        return module

    def __init__(self):
        self.pd = self.install_and_import('pandas')
        self.pyodbc = self.install_and_import('pyodbc')
        self.mysql = self.install_and_import('mysql-connector-python', 'mysql.connector')
        self.pymssql = self.install_and_import('pymssql')
        self.openpyxl = self.install_and_import('openpyxl')
        self.versions = {
            'pandas': self.pd.__version__,
            'pyodbc': self.pyodbc.version,
            'mysql.connector': self.mysql.__version__,
            'pymssql': getattr(self.pymssql, '__version__', 'unknown'),
            'openpyxl': self.openpyxl.__version__
        }

    def check_versions(self):
        for lib, ver in self.versions.items():
            print(f"{lib}: {ver}")

    def fetch_mysql(self, host, user, password, database, query):
        conn = self.mysql.connect(host=host, user=user, password=password, database=database)
        try:
            return self.pd.read_sql(query, conn)
        finally:
            conn.close()

    def fetch_mssql_pyodbc(self, conn_str, query):
        conn = self.pyodbc.connect(conn_str)
        try:
            return self.pd.read_sql_query(query, conn)
        finally:
            conn.close()

    def fetch_mssql_pymssql(self, host, user, password, database, query):
        conn = self.pymssql.connect(server=host, user=user, password=password, database=database)
        try:
            return self.pd.read_sql(query, conn)
        finally:
            conn.close()

    def fetch(self, db_type, **kwargs):
        t = db_type.lower()
        if t == 'mysql':
            return self.fetch_mysql(**kwargs)
        if t == 'mssql_pyodbc':
            return self.fetch_mssql_pyodbc(kwargs.get('conn_str'), kwargs.get('query'))
        if t == 'mssql_pymssql':
            return self.fetch_mssql_pymssql(**kwargs)
        raise ValueError(f"Unsupported db_type: {db_type}")

    def process_data(self, df):
        return df.drop_duplicates().reset_index(drop=True)

    def export_to_excel(self, df, file_path, sheet_name='Sheet1'):
        abs_path = file_path if file_path.endswith('.xlsx') else file_path + '.xlsx'
        df.to_excel(abs_path, sheet_name=sheet_name, index=False, engine='openpyxl')
        print(f"Saved Excel file: {abs_path}")
        