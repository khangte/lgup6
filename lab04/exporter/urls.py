from django.urls import path
from .views import ExportExcelView

urlpatterns = [
    path('export/', ExportExcelView.as_view(), name='export-excel'),
]