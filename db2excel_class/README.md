# 프로젝트 개요
- 잠깐식 사용

# 기능 명세서
- 이 프로젝트 안에는 00 기능이 있다.

## main functions
- MS-SQL, MYSQL 파이썬 연동 및 쿼리 기능 지원 (클래스 구현)
    + DB2EXCEL 클래스
        - 연결기능
        - 쿼리실행기능
        - 엑셀내보내기 기능
- 웹 대시보드를 통해서 간단하게 테스트 할 수 있음
    + 포트번호 입력
    + 사용자 입력

## 기대효과
- 우베 배포 후, 전국 어디에서든지, 쿼리 연습 가능

## sample DB
- MS-SQL 링크 : https://
- MySQL 링크 : https://

# 사용법
- 파이썬 3.13.6 버전 실행
- 가상환경 설치
- 라이브러리 실행
- streamlit 웹 실행
```bash
$ git clone -
$ virtualenv venv
$ source venv/scripts/activate # Mac/Linux source venv/bin/activate
(venv) $ strealit run app.py
```

## 개선사항
- 한글 인코딩 문제 발생 (현재 버그 수정 중)
