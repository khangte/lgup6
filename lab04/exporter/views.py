import io
from django.http import HttpResponse
from django.views import View
from django.conf import settings
from db_to_excel import DB2EXCEL

class ExportExcelView(View):
    """
    Endpoint: GET /export/
    """
    def get(self, request, *args, **kwargs):
        config = {
            'db_type': settings.DB_TYPE,
            'host': settings.DB_HOST,
            'user': settings.DB_USER,
            'password': settings.DB_PASSWORD,
            'database': settings.DB_NAME,
            'query': settings.DB_QUERY,
        }
        exporter = DB2EXCEL()
        df = exporter.fetch(**config)
        df = exporter.process_data(df)
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)
        response = HttpResponse(
            buffer.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="data_export.xlsx"'
        return response