from django.shortcuts import render  # Importing render function to render HTML templates
from django.http import JsonResponse  # Importing JsonResponse for returning JSON responses
from django.views.decorators.csrf import csrf_exempt  # Importing csrf_exempt to exempt CSRF protection
import os  # Importing os module for interacting with the operating system
import openai  # Importing the OpenAI library
from Database.Create_db import create_vector_db  # Importing the function to create a vector database
from Database.import_key import load_api_key_from_config  # Importing the function to load API key
from qdrant_client import QdrantClient  # Importing QdrantClient for interacting with Qdrant

def index(request):
    return render(request, 'upload_form.html')  # Rendering the upload form template

@csrf_exempt
def cargar_documento_docx(request):
    database = QdrantClient(path="mi_proyecto\Database\local_qdrant")  # Initializing QdrantClient
    if request.method == 'POST' and request.FILES.get('archivo_docx'):
        archivo_docx = request.FILES['archivo_docx']  # Getting the uploaded .docx file
        if not os.path.exists('uploaded_files'):  # Creating 'uploaded_files' directory if not exists
            os.makedirs('uploaded_files')
        file_path = os.path.join('uploaded_files', archivo_docx.name)  # Constructing file path
        with open(file_path, 'wb') as destination:
            for chunk in archivo_docx.chunks():
                destination.write(chunk)  # Saving the file to a specific location
        create_vector_db(database)  # Creating vector database
        return JsonResponse({'mensaje': 'Documento .docx cargado exitosamente'})  # Returning success response
    else:
        return JsonResponse({'error': 'No se proporcionó ningún archivo .docx'}, status=400)  # Returning error response

@csrf_exempt
def buscar_documentos(request):
    database = QdrantClient(path="mi_proyecto\Database\local_qdrant")  # Initializing QdrantClient
    if request.method == 'POST':
        config_file_path = "./Keys/config.json"
        openai_key = load_api_key_from_config(config_file_path)
        openai_client = openai.Client(api_key=openai_key)  # Initializing OpenAI client
        input_query = request.POST.get('query')  # Getting user query from request body
        embedding_model = "text-embedding-3-small"  # Defining embedding model
        collection_name = "example_collection"  # Defining collection name
        query_vector = openai_client.embeddings.create(input=[input_query], model=embedding_model).data[0].embedding  # Creating query vector using OpenAI
        search_results = database.search(collection_name=collection_name, query_vector=query_vector)  # Performing search in vector database
        relevant_documents = [result.payload['text'] for result in search_results]  # Getting relevant documents
        return JsonResponse({'resultados': relevant_documents})  # Returning relevant documents as response
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)  # Returning error response if method not allowed
