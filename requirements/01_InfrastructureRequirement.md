# Infrastructure Requirement Specification

## 1. Introduction

### Purpose
This document specifies the functional and non-functional requirements for infrastructure setup, Milvus configuration, embedding models, storage, and development environment for the DSPy Self-Optimizing RAG System.

### Scope
**In-Scope:**
- Milvus vector database setup and configuration
- Local deployment requirements
- Embedding model requirements (sentence-transformers)
- Storage requirements
- Development environment setup
- Dependencies and runtime requirements

**Out-of-Scope:**
- Cloud deployment (AWS, GCP, Azure)
- Kubernetes orchestration
- Production scaling strategies
- Multi-region deployment
- Advanced monitoring infrastructure

### Assumptions
- Local development and deployment environment
- Python 3.9+ runtime
- Docker available for Milvus (optional)
- Sufficient local storage (<50GB)
- Internet connectivity for LLM API access
- Small-scale deployment: <1000 documents, <100 queries/day

### Glossary
- **Milvus**: Open-source vector database for similarity search
- **Embedding Model**: Model that converts text to vector representations
- **Collection**: A Milvus collection containing document embeddings
- **Vector Dimension**: The size of embedding vectors (e.g., 384, 768)
- **Index**: Milvus index for efficient similarity search

## 2. Functional Requirements

### 2.1 Milvus Setup and Configuration

**REQ-INFRA-001**: The system SHALL support Milvus installation and setup.

**REQ-INFRA-002**: The system SHALL support Milvus deployment options:
- Docker container (preferred)
- Standalone binary
- Python pymilvus client connection to remote Milvus

**REQ-INFRA-003**: The system SHALL configure Milvus with:
- Collection name: "documents" (configurable)
- Vector dimension: 384 or 768 (based on embedding model)
- Index type: IVF_FLAT or HNSW (configurable)
- Metric type: L2 (Euclidean distance) or IP (Inner Product)

**REQ-INFRA-004**: The system SHALL create Milvus collection with schema:
- `id`: Primary key (int64 or varchar)
- `vector`: Vector field (float vector)
- `text`: Document text (varchar)
- `document_id`: Source document identifier (varchar)
- `metadata`: Additional metadata (JSON, optional)

**REQ-INFRA-005**: The system SHALL support Milvus connection configuration:
- Host: localhost (default) or configurable
- Port: 19530 (default) or configurable
- Database name: "default" or configurable
- Authentication: Optional (not required for local deployment)

**REQ-INFRA-006**: The system SHALL handle Milvus connection failures gracefully with retry logic.

**REQ-INFRA-007**: The system SHALL support Milvus health checks (connection verification).

### 2.2 Embedding Model Requirements

**REQ-INFRA-008**: The system SHALL use sentence-transformers for text embeddings.

**REQ-INFRA-009**: The system SHALL support embedding model selection:
- `all-MiniLM-L6-v2` (default, 384 dimensions, fast)
- `all-mpnet-base-v2` (768 dimensions, higher quality)
- Custom model (configurable)

**REQ-INFRA-010**: The system SHALL download and cache embedding models locally.

**REQ-INFRA-011**: The system SHALL support offline operation with local embedding models.

**REQ-INFRA-012**: The system SHALL generate embeddings for all documents during indexing.

**REQ-INFRA-013**: The system SHALL support batch embedding generation for efficiency.

**REQ-INFRA-014**: The system SHALL handle embedding model loading errors gracefully.

### 2.3 Document Indexing

**REQ-INFRA-015**: The system SHALL provide document indexing functionality.

**REQ-INFRA-016**: The system SHALL support indexing from:
- Text files (.txt)
- Markdown files (.md)
- PDF files (.pdf, optional)
- JSON files (.json)

**REQ-INFRA-017**: The system SHALL chunk documents into smaller segments (configurable chunk size, default: 500 tokens).

**REQ-INFRA-018**: The system SHALL generate embeddings for each chunk.

**REQ-INFRA-019**: The system SHALL store chunks and embeddings in Milvus.

**REQ-INFRA-020**: The system SHALL support incremental indexing (add new documents without re-indexing all).

**REQ-INFRA-021**: The system SHALL support document deletion from index.

**REQ-INFRA-022**: The system SHALL track indexing progress and provide status updates.

### 2.4 Storage Requirements

**REQ-INFRA-023**: The system SHALL define storage requirements:
- Milvus data: <10GB for 1000 documents
- Embedding model cache: <2GB per model
- Program versions: <100MB per version
- Cache storage: <5GB (SQLite/Redis)
- Logs: <1GB (configurable retention)

**REQ-INFRA-024**: The system SHALL support configurable storage paths:
- Milvus data directory
- Model cache directory
- Program versions directory
- Cache directory
- Logs directory

**REQ-INFRA-025**: The system SHALL handle disk space limits gracefully (warnings, cleanup).

**REQ-INFRA-026**: The system SHALL support storage cleanup (old logs, expired cache entries).

### 2.5 Development Environment Setup

**REQ-INFRA-027**: The system SHALL provide setup instructions for development environment.

**REQ-INFRA-028**: The system SHALL support Python virtual environment (venv, conda, poetry).

**REQ-INFRA-029**: The system SHALL provide dependency management (requirements.txt, pyproject.toml).

**REQ-INFRA-030**: The system SHALL support installation via:
- pip install from requirements.txt
- poetry install
- Manual dependency installation

**REQ-INFRA-031**: The system SHALL provide environment variable configuration:
- LLM API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY)
- Milvus connection settings
- Log level
- Cache configuration

**REQ-INFRA-032**: The system SHALL provide example configuration files (.env.example).

**REQ-INFRA-033**: The system SHALL support development mode with:
- Debug logging
- Hot-reload (optional)
- Mock services for testing

### 2.6 Runtime Requirements

**REQ-INFRA-034**: The system SHALL require Python 3.9 or higher.

**REQ-INFRA-035**: The system SHALL support operating systems:
- macOS (Darwin)
- Linux (Ubuntu 20.04+, Debian 11+)
- Windows (with WSL2, optional)

**REQ-INFRA-036**: The system SHALL require minimum system resources:
- CPU: 2 cores (4+ recommended)
- RAM: 8GB (16GB+ recommended)
- Disk: 20GB free space
- Network: Internet connectivity for LLM APIs

**REQ-INFRA-037**: The system SHALL support GPU acceleration for embeddings (optional, CUDA).

## 3. Non-Functional Requirements

### 3.1 Performance

**REQ-INFRA-NFR-001**: Milvus SHALL respond to queries within 100ms for 95% of queries (p95 latency).

**REQ-INFRA-NFR-002**: Embedding generation SHALL complete within 50ms per chunk (CPU) or 10ms (GPU).

**REQ-INFRA-NFR-003**: Document indexing SHALL process at least 100 chunks per minute.

**REQ-INFRA-NFR-004**: System startup SHALL complete within 30 seconds (including model loading).

### 3.2 Reliability

**REQ-INFRA-NFR-005**: Milvus SHALL maintain data persistence across restarts.

**REQ-INFRA-NFR-006**: The system SHALL handle Milvus crashes gracefully (restart, recovery).

**REQ-INFRA-NFR-007**: The system SHALL support data backup and restore for Milvus.

**REQ-INFRA-NFR-008**: The system SHALL validate data integrity (checksums, if applicable).

### 3.3 Scalability

**REQ-INFRA-NFR-009**: Milvus SHALL support at least 10,000 document chunks.

**REQ-INFRA-NFR-010**: The system SHALL handle indexing of up to 1000 documents.

**REQ-INFRA-NFR-011**: The system SHALL support concurrent queries (up to 5 simultaneous).

### 3.4 Resource Usage

**REQ-INFRA-NFR-012**: Milvus SHALL use <2GB RAM for 1000 documents.

**REQ-INFRA-NFR-013**: Embedding models SHALL use <2GB RAM per model.

**REQ-INFRA-NFR-014**: The system SHALL have minimal disk I/O overhead.

## 4. Interfaces & Contracts

### 4.1 Milvus Configuration

**Milvus Config Schema:**
```python
@dataclass
class MilvusConfig:
    host: str = "localhost"
    port: int = 19530
    database: str = "default"
    collection_name: str = "documents"
    vector_dimension: int = 384  # or 768
    index_type: str = "IVF_FLAT"  # or "HNSW"
    metric_type: str = "L2"  # or "IP"
    index_params: Optional[Dict[str, Any]] = None
    search_params: Optional[Dict[str, Any]] = None
```

**Collection Schema:**
```python
from pymilvus import CollectionSchema, FieldSchema, DataType

fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=384),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=10000),
    FieldSchema(name="document_id", dtype=DataType.VARCHAR, max_length=255),
    FieldSchema(name="metadata", dtype=DataType.JSON)
]

schema = CollectionSchema(fields, "Document collection for RAG")
```

### 4.2 Embedding Model Interface

**Embedding Model Config:**
```python
@dataclass
class EmbeddingModelConfig:
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    device: str = "cpu"  # or "cuda"
    batch_size: int = 32
    max_length: int = 512
    cache_dir: Optional[str] = None
```

**Embedding Function:**
```python
from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    def __init__(self, config: EmbeddingModelConfig):
        self.model = SentenceTransformer(
            config.model_name,
            device=config.device,
            cache_folder=config.cache_dir
        )
        
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for list of texts."""
        return self.model.encode(texts, batch_size=self.config.batch_size)
```

### 4.3 Indexing Interface

**Indexing Config:**
```python
@dataclass
class IndexingConfig:
    chunk_size: int = 500  # tokens
    chunk_overlap: int = 50  # tokens
    embedding_model: EmbeddingModelConfig
    milvus_config: MilvusConfig
    batch_size: int = 100  # chunks per batch
```

**Indexing Function:**
```python
def index_documents(
    documents: List[Document],
    config: IndexingConfig
) -> IndexingResult:
    """
    Index documents into Milvus.
    
    Args:
        documents: List of documents to index
        config: Indexing configuration
        
    Returns:
        IndexingResult with statistics
    """
```

### 4.4 System Dependencies

**Python Dependencies (requirements.txt):**
```
dspy>=2.0.0
pymilvus>=2.3.0
sentence-transformers>=2.2.0
numpy>=1.24.0
pandas>=2.0.0
streamlit>=1.28.0
baml-python>=0.1.0
openai>=1.0.0
anthropic>=0.18.0
redis>=5.0.0
sqlalchemy>=2.0.0
python-dotenv>=1.0.0
```

**System Dependencies:**
- Docker (optional, for Milvus)
- Python 3.9+
- pip or poetry
- Git (for version control)

### 4.5 Environment Variables

**.env.example:**
```bash
# LLM API Keys
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Milvus Configuration
MILVUS_HOST=localhost
MILVUS_PORT=19530
MILVUS_DATABASE=default
MILVUS_COLLECTION=documents

# Embedding Model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DEVICE=cpu

# Cache Configuration
CACHE_BACKEND=sqlite
CACHE_TTL_HOURS=24
CACHE_PATH=./cache.db

# Logging
LOG_LEVEL=INFO
LOG_PATH=./logs

# Program Versions
PROGRAMS_DIR=./programs
```

## 5. Tenant & Security Considerations

### 5.1 Multi-Tenancy
**REQ-INFRA-SEC-001**: The system SHALL support single-tenant operation for local deployment (no multi-tenancy required).

### 5.2 Security
**REQ-INFRA-SEC-002**: The system SHALL protect API keys and credentials (environment variables, not in code).

**REQ-INFRA-SEC-003**: The system SHALL validate all configuration inputs to prevent injection attacks.

**REQ-INFRA-SEC-004**: The system SHALL restrict file system access to authorized directories only.

**REQ-INFRA-SEC-005**: The system SHALL support secure Milvus connections (TLS, if configured).

## 6. Observability & Telemetry

### 6.1 Metrics

**REQ-INFRA-OBS-001**: The system SHALL track infrastructure metrics:
- Milvus query latency
- Embedding generation time
- Indexing progress and speed
- Storage usage
- System resource usage (CPU, RAM, disk)

### 6.2 Logging

**REQ-INFRA-OBS-002**: The system SHALL log infrastructure operations:
- Milvus connection status
- Embedding model loading
- Indexing progress
- Storage operations
- Configuration loading

### 6.3 Health Checks

**REQ-INFRA-OBS-003**: The system SHALL verify:
- Milvus connectivity
- Embedding model availability
- Storage space availability
- Required dependencies installed

## 7. Compliance & Governance

### 7.1 Data Management

**REQ-INFRA-COMP-001**: The system SHALL support data backup for:
- Milvus collections
- Program versions
- Configuration files

**REQ-INFRA-COMP-002**: The system SHALL support data retention policies for logs and cache.

### 7.2 Version Control

**REQ-INFRA-COMP-003**: The system SHALL maintain version history for:
- Program versions
- Configuration changes
- Dependency updates

## 8. Open Questions & Assumptions

### Open Questions

1. **Q1**: Should Milvus run in Docker or as standalone? (Assumed: Docker preferred, standalone optional)
2. **Q2**: What is the optimal chunk size for documents? (Assumed: 500 tokens, configurable)
3. **Q3**: Should the system support multiple embedding models simultaneously? (Assumed: Single model, configurable)
4. **Q4**: What document formats should be supported? (Assumed: Text, Markdown, PDF optional)
5. **Q5**: Should the system support GPU acceleration? (Assumed: Optional, CPU default)

### Assumptions

1. Milvus runs locally (Docker container or standalone)
2. Embedding models are downloaded and cached locally
3. Documents are pre-processed and available in text format
4. Local storage is sufficient for small-scale deployment
5. Internet connectivity is available for LLM API access
6. Python 3.9+ is the runtime environment
7. Development environment is macOS or Linux (Windows with WSL2)
8. Docker is available for Milvus deployment (optional)
9. GPU is optional (CPU is sufficient for small-scale)
10. All dependencies are installable via pip or poetry

