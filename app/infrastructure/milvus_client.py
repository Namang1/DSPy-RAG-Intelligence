from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)
from app.config import Config
from app.infrastructure.embedding_model import EmbeddingModel
from typing import List, Dict, Any, Optional

class MilvusClient:
    def __init__(self):
        self.host = Config.MILVUS_HOST
        self.port = Config.MILVUS_PORT
        self.collection_name = Config.MILVUS_COLLECTION_NAME
        self.embedding_model = EmbeddingModel()
        self.collection = None
        
        self.connect()
        self.init_collection()

    def connect(self):
        print(f"Connecting to Milvus at {self.host}:{self.port}...")
        try:
            connections.connect("default", host=self.host, port=self.port)
            print("Successfully connected to Milvus.")
        except Exception as e:
            print(f"Failed to connect to Milvus: {e}")
            raise

    def init_collection(self):
        if utility.has_collection(self.collection_name):
            print(f"Collection '{self.collection_name}' exists. Loading...")
            self.collection = Collection(self.collection_name)
            self.collection.load()
        else:
            print(f"Collection '{self.collection_name}' does not exist. Creating...")
            self.create_collection()

    def create_collection(self):
        # Define Schema based on requirements
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=self.embedding_model.dimension),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=255),
            FieldSchema(name="metadata", dtype=DataType.JSON, nullable=True) # Supported in newer Milvus
        ]
        
        schema = CollectionSchema(fields, "Document collection for DSPy RAG")
        self.collection = Collection(self.collection_name, schema)
        
        # Create Index
        index_params = {
            "metric_type": "L2",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 1024}
        }
        self.collection.create_index("vector", index_params)
        self.collection.load()
        print(f"Collection '{self.collection_name}' created and loaded.")

    def insert_documents(self, documents: List[str], sources: List[str], metadatas: Optional[List[Dict]] = None):
        """
        Insert documents into Milvus.
        """
        print(f"Generating embeddings for {len(documents)} documents...")
        vectors = self.embedding_model.encode(documents)
        
        entities = [
            vectors,
            documents,
            sources,
            metadatas if metadatas else [{}] * len(documents)
        ]
        
        self.collection.insert(entities)
        self.collection.flush()
        print(f"Inserted {len(documents)} documents.")

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for relevant documents.
        """
        query_vector = self.embedding_model.encode(query) # List[List[float]]
        
        search_params = {
            "metric_type": "L2",
            "params": {"nprobe": 10},
        }
        
        results = self.collection.search(
            data=query_vector,
            anns_field="vector",
            param=search_params,
            limit=top_k,
            output_fields=["text", "source", "metadata"]
        )
        
        # Format results
        hits = results[0]
        formatted_results = []
        for hit in hits:
            formatted_results.append({
                "id": hit.id,
                "score": hit.score,
                "text": hit.entity.get("text"),
                "source": hit.entity.get("source"),
                "metadata": hit.entity.get("metadata")
            })
            
        return formatted_results
