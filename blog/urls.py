# blog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('upload_multiple/', views.upload_multiple, name='upload_multiple'),
    path('uploadtraining/', views.upload_multiple_pdfs, name='upload_multiple_pdfs'),
    path('uploadtester/', views.upload_pdf, name='upload_pdf'),
    path('run/', views.run_plagiarism_check, name='run_plagiarism_check'),
    path('delete_training/<int:pdf_id>/', views.delete_pdf_training, name='delete_pdf_training'),
    path('delete_tester/<int:pdf_id>/', views.delete_pdf_tester, name='delete_pdf_tester'),
    path('view_training/<int:pdf_id>/', views.view_pdf_training, name='view_pdf_training'),
    path('view_tester/<int:pdf_id>/', views.view_pdf_tester, name='view_pdf_tester'),
    path('download_training/<int:pdf_id>/', views.download_pdf_training, name='download_pdf_training'),
    path('download_tester/<int:pdf_id>/', views.download_pdf_tester, name='download_pdf_tester'),
    path('delete_all/', views.delete_all, name='delete_all'),    
    path('preview/<int:result_id>/', views.detail_view, name='detail_view'),

    path('coba/', views.coba, name='coba'),
]
