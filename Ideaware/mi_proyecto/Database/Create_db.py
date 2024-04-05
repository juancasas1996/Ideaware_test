from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
import openai
import os
import getpass
import qdrant_client
from qdrant_client.models import PointStruct
from qdrant_client.models import VectorParams, Distance
from Database.import_key import load_api_key_from_config

def create_vector_db(database):
    # Load API key from config file
    config_file_path = "./Keys/config.json"
    openai_key = load_api_key_from_config(config_file_path)
    
    # Initialize OpenAI client
    openai_client = openai.Client(api_key=openai_key)

    # Specify the directory containing uploaded files
    directory = '../mi_proyecto/uploaded_files'
    
    # Load documents from the specified directory
    loader = DirectoryLoader(directory, glob="**/*.docx", show_progress=False)
    in_docs = loader.load()
    
    # Split text from documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    texts = text_splitter.split_documents(in_docs)

    # Define embedding model
    embedding_model = "text-embedding-3-small"

    # Extract text content from documents
    list_docs = [doc.page_content for doc in texts]

    # Generate embeddings for the text content using OpenAI
    result = openai_client.embeddings.create(input=list_docs, model=embedding_model)

    # Prepare points with embeddings and corresponding text
    points = [
        PointStruct(
            id=idx,
            vector=data.embedding,
            payload={"text": text},
        )
        for idx, (data, text) in enumerate(zip(result.data, list_docs))
    ]

    # Define collection name
    collection_name = "example_collection"

    # Recreate the collection in the database with specified vector configuration
    database.recreate_collection(
        collection_name,
        vectors_config=VectorParams(
            size=1536,
            distance=Distance.COSINE,
        ),
    )
    
    # Upsert points into the collection
    database.upsert(collection_name, points)
    
    # Remove uploaded files after processing
    directory = '../mi_proyecto/uploaded_files'
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            os.remove(file_path)
            print("Archivo borrado:", file_path)
        except Exception as e:
            print("Error al borrar el archivo:", e)
