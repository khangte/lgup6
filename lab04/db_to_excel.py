import subprocess
import sys
import os

def install_and_import(package_name, import_name=None):
    """
    Try to import a package; if missing, install it via pip and then import.
    :param package_name: name used by pip to install (e.g. "mysql-connector-python")
    :param import_name: name used to import (e.g. "mysql.connector"); defaults to package_name
    """
    name = import_name or package_name
    try:
        module = __import__(name)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        module = __import__(name)
    return module

# examples for your DB2EXCEL class dependencies
pd = install_and_import("pandas")
pyodbc = install_and_import("pyodbc")
mysql = install_and_import("mysql-connector-python", "mysql.connector")
pymssql = install_and_import("pymssql")

pd = install_and_import("pandas")
openpyxl = install_and_import("openpyxl")      

class DB2EXCEL:
    """
    A class to extract data from various databases and export to Excel files.
    Supports MS-SQL (via pyodbc or pymssql) and MySQL.
    """

    def __init__(self):
        """
        Initialize the DB2EXCEL class and store library versions.
        """
        self.versions = {
            'pandas': pd.__version__,
            'pyodbc': pyodbc.version,
            'mysql.connector': mysql.connector.__version__,
            'pymssql': getattr(pymssql, '__version__', 'unknown')
        }

    def check_versions(self):
        """
        Print the versions of the core libraries.
        """
        for lib, ver in self.versions.items():
            print(f"{lib}: {ver}")

    def fetch_mssql_pyodbc(self, conn_str: str, query: str) -> pd.DataFrame:
        """
        Connect to a MS-SQL database using pyodbc and execute the query.

        Parameters:
        - conn_str (str): ODBC connection string for MS-SQL.
        - query (str): SQL query to execute.

        Returns:
        - pd.DataFrame: The result set as a pandas DataFrame.
        """
        conn = pyodbc.connect(conn_str)
        try:
            df = pd.read_sql_query(query, conn)
        finally:
            conn.close()
        return df

    def fetch_mssql_pymssql(self, host: str, user: str, password: str, database: str, query: str) -> pd.DataFrame:
        """
        Connect to a MS-SQL database using pymssql and execute the query.

        Parameters:
        - host (str): MS-SQL host.
        - user (str): MS-SQL user.
        - password (str): MS-SQL password.
        - database (str): MS-SQL database name.
        - query (str): SQL query to execute.

        Returns:
        - pd.DataFrame: The result set as a pandas DataFrame.
        """
        conn = pymssql.connect(server=host, user=user, password=password, database=database)
        try:
            df = pd.read_sql(query, conn)
        finally:
            conn.close()
        return df

    def fetch_mysql(self, host: str, user: str, password: str, database: str, query: str) -> pd.DataFrame:
        """
        Connect to a MySQL database using mysql.connector and execute the query.

        Parameters:
        - host (str): MySQL host.
        - user (str): MySQL user.
        - password (str): MySQL password.
        - database (str): MySQL database name.
        - query (str): SQL query to execute.

        Returns:
        - pd.DataFrame: The result set as a pandas DataFrame.
        """
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        try:
            df = pd.read_sql(query, conn)
        finally:
            conn.close()
        return df

    def fetch(self, db_type: str, **kwargs) -> pd.DataFrame:
        """
        Generic fetch method that delegates to the appropriate DB fetch method.

        Parameters:
        - db_type (str): Type of database ('mssql_pyodbc', 'mssql_pymssql', 'mysql').
        - kwargs: Keyword arguments for the specific fetch method.

        Returns:
        - pd.DataFrame: The result set as a pandas DataFrame.

        Raises:
        - ValueError: If db_type is unsupported.
        """
        db = db_type.lower()
        if db == 'mssql_pyodbc':
            return self.fetch_mssql_pyodbc(kwargs.get('conn_str'), kwargs.get('query'))
        elif db == 'mssql_pymssql':
            return self.fetch_mssql_pymssql(
                kwargs.get('host'),
                kwargs.get('user'),
                kwargs.get('password'),
                kwargs.get('database'),
                kwargs.get('query')
            )
        elif db == 'mysql':
            return self.fetch_mysql(
                kwargs.get('host'),
                kwargs.get('user'),
                kwargs.get('password'),
                kwargs.get('database'),
                kwargs.get('query')
            )
        else:
            raise ValueError(f"Unsupported db_type: {db_type}")

    def process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Placeholder for data processing steps. This method can be customized.

        Parameters:
        - df (pd.DataFrame): Raw DataFrame.

        Returns:
        - pd.DataFrame: Processed DataFrame.
        """
        # 예시: 중복 제거 및 인덱스 재설정
        return df.drop_duplicates().reset_index(drop=True)

    def export_to_excel(self, df: pd.DataFrame, file_path: str, sheet_name: str = 'Sheet1'):
        """
        Export the DataFrame to an Excel file, using openpyxl engine.
        """
        try:
            # 절대 경로로 변환해 두고
            abs_path = os.path.abspath(file_path)
            df.to_excel(abs_path, sheet_name=sheet_name, index=False, engine='openpyxl')
            print(f"[OK] Excel 파일 저장 완료: {abs_path}")
        except Exception as e:
            print(f"[ERROR] 엑셀 내보내기 실패: {e}")
