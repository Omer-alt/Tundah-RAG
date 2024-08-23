from .model import Model
from .utility import *
from sentence_transformers import util, SentenceTransformer

device = Utility.get_device()

class EmbeddingModel(Model):
    
    _instance = None  # Class variable to store the unique instance
    embedding_model = SentenceTransformer(model_name_or_path="all-mpnet-base-v2", device=device)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)  # Creates the instance if it does not yet exist
        return cls._instance

    # Create embedding vectors for Qdrant
    def create_embeddings(self, chunks):
        vectors = [self.embedding_model.encode(item["sentence_chunk"]) for item in chunks]
        return vectors
    
    # Create embedding vectors for Qdrant
    def create_query_embeddings(self, query):
        vector_of_query = self.embedding_model.encode(query) 
        return vector_of_query
    
    