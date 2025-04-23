from db_to_excel import DB2EXCEL

def main():
    exporter = DB2EXCEL()
    exporter.check_versions()

    df = exporter.fetch(
        db_type = 'mssql_pymssql',
        host='127.0.0.1:1433',
        user='kmh-tester1',
        password='1234',
        database='BikeStores',
        query='SELECT * FROM sales.customers'
    )

    processed_df = exporter.process_data(df)

    exporter.export_to_excel(processed_df, file_path='output.xlsx')

if __name__ == '__main__':
    main()

