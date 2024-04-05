# En urls.py
from django.urls import path
from mi_aplicacion import views 

urlpatterns = [
    path('', views.index, name='index'),  # Default route to index view
    path('cargar-docx/', views.cargar_documento_docx, name='cargar_docx'),  # Route for uploading documents
    path('buscar-documentos/', views.buscar_documentos, name='buscar_documentos'),  # Route for searching documents
]
