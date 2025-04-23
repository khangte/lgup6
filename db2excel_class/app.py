import streamlit as st
import pandas as pd
from db2excel import DB2EXCEL
import tempfile
import os
import mysql.connector
import pymssql

st.set_page_config(
    page_title="DB2Excel Converter",
    page_icon="📊",
    layout="wide"
)

def validate_connection_params(db_type, params):
    """연결 파라미터 유효성 검사"""
    required_fields = {
        "mssql": ["server", "port", "database", "user", "password"],
        "mysql": ["host", "port", "database", "user", "password"]
    }
    
    missing_fields = [field for field in required_fields[db_type] 
                     if not params.get(field)]
    
    if missing_fields:
        return False, f"다음 필드를 입력해주세요: {', '.join(missing_fields)}"
    
    try:
        port = int(params.get("port"))
        if port <= 0 or port > 65535:
            return False, "포트 번호는 1-65535 사이의 값이어야 합니다."
    except ValueError:
        return False, "올바른 포트 번호를 입력해주세요."
    
    return True, ""

def test_connection(db_type, params):
    """데이터베이스 연결 테스트"""
    try:
        with DB2EXCEL(db_type, **params) as db:
            return True, "데이터베이스 연결이 성공적으로 테스트되었습니다."
    except pymssql.Error as e:
        return False, f"MSSQL 연결 오류: {str(e)}"
    except mysql.connector.Error as e:
        return False, f"MySQL 연결 오류: {str(e)}"
    except Exception as e:
        return False, f"연결 오류: {str(e)}"

def validate_sql_query(query):
    """SQL 쿼리 기본 유효성 검사"""
    if not query.strip():
        return False, "SQL 쿼리를 입력해주세요."
    
    # 기본적인 SQL 키워드 체크
    query_lower = query.lower().strip()
    if not any(query_lower.startswith(keyword) for keyword in ['select', 'show']):
        return False, "현재 SELECT 또는 SHOW 쿼리만 지원합니다."
    
    return True, ""

st.title("📊 DB2Excel Converter")
st.markdown("""
이 앱은 데이터베이스에서 데이터를 추출하여 Excel 파일로 변환해주는 도구입니다.
""")

# 사이드바 설정
st.sidebar.header("데이터베이스 설정")

# 데이터베이스 종류 선택
db_type = st.sidebar.selectbox(
    "데이터베이스 종류",
    ["mssql", "mysql"]
)

# 연결 정보 입력
if db_type == "mssql":
    server = st.sidebar.text_input("서버 주소")
    port = st.sidebar.number_input("포트", value=1433)
    database = st.sidebar.text_input("데이터베이스 이름")
    username = st.sidebar.text_input("사용자 이름")
    password = st.sidebar.text_input("비밀번호", type="password")
    
    connection_params = {
        "server": server,
        "port": port,
        "database": database,
        "user": username,
        "password": password
    }
else:  # mysql
    host = st.sidebar.text_input("호스트 주소")
    port = st.sidebar.number_input("포트", value=3306)
    database = st.sidebar.text_input("데이터베이스 이름")
    username = st.sidebar.text_input("사용자 이름")
    password = st.sidebar.text_input("비밀번호", type="password")
    
    connection_params = {
        "host": host,
        "port": port,
        "database": database,
        "user": username,
        "password": password
    }

# 연결 테스트 버튼
if st.sidebar.button("연결 테스트"):
    # 연결 파라미터 검증
    is_valid, message = validate_connection_params(db_type, connection_params)
    if not is_valid:
        st.sidebar.error(message)
    else:
        # 실제 연결 테스트
        is_connected, message = test_connection(db_type, connection_params)
        if is_connected:
            st.sidebar.success(message)
        else:
            st.sidebar.error(message)

# SQL 쿼리 입력
st.header("SQL 쿼리 입력")
query = st.text_area("SQL 쿼리를 입력하세요", height=150)

# 실행 버튼
if st.button("쿼리 실행 및 Excel로 내보내기"):
    # 쿼리 유효성 검사
    is_valid, message = validate_sql_query(query)
    if not is_valid:
        st.error(message)
    else:
        # 연결 파라미터 검증
        is_valid, message = validate_connection_params(db_type, connection_params)
        if not is_valid:
            st.error(message)
        else:
            try:
                with st.spinner('데이터베이스에서 데이터를 가져오는 중...'):
                    # DB2EXCEL 인스턴스 생성 및 연결
                    with DB2EXCEL(db_type, **connection_params) as db:
                        # 쿼리 실행
                        results = db.execute_query(query)
                        
                        if not results:
                            st.warning("쿼리 결과가 없습니다.")
                            st.stop()
                        
                        # 데이터 처리
                        df = db.process_data(results)
                        
                        # 결과 미리보기
                        st.subheader("쿼리 결과 미리보기")
                        st.dataframe(df)
                        
                        # 행과 열 정보 표시
                        st.info(f"총 {len(df)} 행, {len(df.columns)} 열의 데이터가 조회되었습니다.")
                        
                        # Excel 파일 생성 및 다운로드
                        try:
                            with st.spinner('Excel 파일 생성 중...'):
                                # BytesIO를 사용하여 메모리에서 Excel 파일 생성
                                from io import BytesIO
                                buffer = BytesIO()
                                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                                    df.to_excel(writer, sheet_name='Sheet1', index=False)
                                
                                # 다운로드 버튼 생성
                                st.download_button(
                                    label="Excel 파일 다운로드",
                                    data=buffer.getvalue(),
                                    file_name="query_results.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                        except Exception as e:
                            st.error(f"Excel 파일 생성 중 오류가 발생했습니다: {str(e)}")

            except pymssql.Error as e:
                st.error(f"MSSQL 오류: {str(e)}")
            except mysql.connector.Error as e:
                st.error(f"MySQL 오류: {str(e)}")
            except pd.errors.EmptyDataError:
                st.error("데이터를 처리하는 중 오류가 발생했습니다: 빈 데이터셋")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")

# 사용 방법 설명
with st.expander("사용 방법"):
    st.markdown("""
    1. 왼쪽 사이드바에서 데이터베이스 종류를 선택하세요.
    2. 데이터베이스 연결 정보를 입력하세요.
    3. '연결 테스트' 버튼을 클릭하여 연결이 정상적인지 확인하세요.
    4. SQL 쿼리를 입력하세요. (현재는 SELECT 쿼리만 지원합니다)
    5. "쿼리 실행 및 Excel로 내보내기" 버튼을 클릭하세요.
    6. 쿼리 결과를 확인하고 Excel 파일을 다운로드하세요.
    
    주의사항:
    - 모든 필수 연결 정보를 입력해야 합니다.
    - SELECT 쿼리만 실행 가능합니다.
    - 대용량 데이터의 경우 처리 시간이 길어질 수 있습니다.
    """)
