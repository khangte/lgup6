"""
DB2EXCEL - 다양한 데이터베이스에서 데이터를 추출하여 Excel로 내보내는 유틸리티 클래스

이 모듈은 다음 기능을 제공합니다:
1. 다양한 데이터베이스(MSSQL, MySQL 등) 연결
2. SQL 쿼리 실행 및 데이터 추출
3. 데이터 처리 및 변환
4. Excel 파일로 결과 내보내기

필요한 라이브러리:
- pymssql: MSSQL 데이터베이스 연결용
- mysql-connector-python: MySQL 데이터베이스 연결용
- pandas: 데이터 조작 및 Excel 내보내기용
- openpyxl: Excel 파일 처리용
"""

import pymssql
import mysql.connector
import pandas as pd
from typing import Union, Dict, List, Optional
import logging

class DB2EXCEL:
    """
    데이터베이스 연결, 데이터 추출, Excel 내보내기 작업을 처리하는 클래스입니다.
    
    속성:
        db_type (str): 데이터베이스 종류 ('mssql' 또는 'mysql')
        connection_params (dict): 데이터베이스 연결 매개변수
        conn: 데이터베이스 연결 객체
        cursor: 데이터베이스 커서 객체
    """
    
    def __init__(self, db_type: str, **connection_params):
        """
        DB2EXCEL 클래스를 데이터베이스 종류와 연결 매개변수로 초기화합니다.
        
        매개변수:
            db_type (str): 데이터베이스 종류 ('mssql' 또는 'mysql')
            **connection_params: 데이터베이스 연결 매개변수
                MSSQL의 경우:
                    - server: 서버 주소
                    - port: 포트 번호
                    - user: 사용자 이름
                    - password: 비밀번호
                    - database: 데이터베이스 이름
                MySQL의 경우:
                    - host: 호스트 주소
                    - port: 포트 번호
                    - user: 사용자 이름
                    - password: 비밀번호
                    - database: 데이터베이스 이름
        """
        self.db_type = db_type.lower()
        self.connection_params = connection_params
        self.conn = None
        self.cursor = None
        
        # 로깅 설정
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # 필수 라이브러리 확인
        self._check_dependencies()
    
    def _check_dependencies(self) -> None:
        """필요한 모든 라이브러리가 설치되어 있는지 확인합니다."""
        try:
            if self.db_type == 'mssql':
                import pymssql
            elif self.db_type == 'mysql':
                import mysql.connector
            import pandas
            import openpyxl
        except ImportError as e:
            self.logger.error(f"필수 라이브러리가 없습니다: {str(e)}")
            raise
    
    def connect(self) -> None:
        """
        지정된 종류의 데이터베이스에 연결을 설정합니다.
        
        예외:
            ValueError: 지원하지 않는 데이터베이스 종류인 경우
            Exception: 연결 실패 시
        """
        try:
            if self.db_type == 'mssql':
                self.conn = pymssql.connect(**self.connection_params)
                self.cursor = self.conn.cursor(as_dict=True)  # MSSQL은 as_dict 사용
            elif self.db_type == 'mysql':
                self.conn = mysql.connector.connect(**self.connection_params)
                self.cursor = self.conn.cursor(dictionary=True)  # MySQL은 dictionary 사용
            else:
                raise ValueError(f"지원하지 않는 데이터베이스 종류: {self.db_type}")
            
            self.logger.info(f"{self.db_type.upper()} 데이터베이스에 성공적으로 연결되었습니다")
            
        except Exception as e:
            self.logger.error(f"데이터베이스 연결 실패: {str(e)}")
            raise
    
    def execute_query(self, query: str) -> List[Dict]:
        """
        SQL 쿼리를 실행하고 결과를 반환합니다.
        
        매개변수:
            query (str): 실행할 SQL 쿼리
            
        반환:
            List[Dict]: 쿼리 결과를 포함하는 딕셔너리 리스트
            
        예외:
            Exception: 쿼리 실행 실패 시
        """
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            self.logger.info(f"쿼리가 성공적으로 실행되었습니다. {len(results)}개의 행을 가져왔습니다")
            return results
        except Exception as e:
            self.logger.error(f"쿼리 실행 실패: {str(e)}")
            raise
    
    def process_data(self, data: List[Dict], processing_function: Optional[callable] = None) -> pd.DataFrame:
        """
        데이터를 처리하고 pandas DataFrame으로 변환합니다.
        
        매개변수:
            data (List[Dict]): 데이터베이스에서 가져온 원본 데이터
            processing_function (callable, optional): 데이터를 처리할 함수
            
        반환:
            pd.DataFrame: 처리된 데이터를 DataFrame 형식으로
        """
        df = pd.DataFrame(data)
        
        if processing_function:
            df = processing_function(df)
            self.logger.info("데이터 처리가 완료되었습니다")
        
        return df
    
    def export_to_excel(self, df: pd.DataFrame, output_path: str, sheet_name: str = 'Sheet1') -> None:
        """
        DataFrame을 Excel 파일로 내보냅니다.
        
        매개변수:
            df (pd.DataFrame): 내보낼 데이터
            output_path (str): Excel 파일을 저장할 경로
            sheet_name (str): Excel 시트 이름
            
        예외:
            Exception: 내보내기 실패 시
        """
        try:
            df.to_excel(output_path, sheet_name=sheet_name, index=False)
            self.logger.info(f"데이터가 성공적으로 {output_path}로 내보내졌습니다")
        except Exception as e:
            self.logger.error(f"Excel로 내보내기 실패: {str(e)}")
            raise
    
    def close(self) -> None:
        """데이터베이스 연결을 종료합니다."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        self.logger.info("데이터베이스 연결이 종료되었습니다")
    
    def __enter__(self):
        """컨텍스트 매니저 진입"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 매니저 종료"""
        self.close()