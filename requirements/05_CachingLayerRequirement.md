# Caching Layer Requirement Specification

## 1. Introduction

### Purpose
This document specifies the functional and non-functional requirements for the Caching Layer component of the DSPy Self-Optimizing RAG System. The Caching Layer reduces repeated LLM costs by storing and retrieving previously computed answers, evidence, and intermediate results.

### Scope
**In-Scope:**
- Cache key generation (hash of query + version_id)
- Cache storage backends (SQLite, Redis, local JSON)
- Cache retrieval and invalidation
- TTL (Time-To-Live) configuration
- Stats API (hit/miss tracking)
- Integration with all pipeline components

**Out-of-Scope:**
- Cache warming strategies
- Distributed cache synchronization
- Cache replication
- Cache encryption at rest (covered in Security Requirements)

### Assumptions
- SQLite is available as primary cache backend
- Redis is optional (for production scaling)
- Local JSON cache is sufficient for development
- Cache size is manageable (<10GB for small-scale deployment)
- Query variations are common (caching will be effective)

### Glossary
- **Cache Key**: A unique identifier for a cached entry (hash of query + version_id)
- **Cache Hit**: When a requested item is found in cache
- **Cache Miss**: When a requested item is not found in cache
- **TTL**: Time-To-Live, the duration a cache entry remains valid
- **Cache Invalidation**: The process of removing or marking cache entries as invalid

## 2. Functional Requirements

### 2.1 Cache Key Generation

**REQ-CACHE-001**: The system SHALL generate cache keys using a hash of the user query and program version ID.

**REQ-CACHE-002**: The cache key generation SHALL use a deterministic hashing algorithm (SHA-256).

**REQ-CACHE-003**: The cache key SHALL include:
- User query text (normalized: trimmed, lowercased)
- Program version ID (e.g., "rag_v1", "rag_v2")
- Optional: query parameters (top_k, max_iterations, etc.) if they affect results

**REQ-CACHE-004**: The cache key SHALL be unique for each unique query+version combination.

**REQ-CACHE-005**: The system SHALL normalize queries before hashing (trim whitespace, handle case sensitivity).

### 2.2 Cache Storage

**REQ-CACHE-006**: The system SHALL support multiple cache backends:
- SQLite (primary, default)
- Redis (optional, for production)
- Local JSON file (fallback, for development)

**REQ-CACHE-007**: The system SHALL allow configuration of cache backend at runtime.

**REQ-CACHE-008**: The system SHALL store the following data for each cache entry:
- Cache key (primary identifier)
- Final structured answer (FinalAnswer schema)
- Retrieved evidence chunks (list)
- Program version used
- Timestamp of cache creation
- TTL expiration timestamp
- Execution metadata (execution time, token usage, etc.)

**REQ-CACHE-009**: The system SHALL support cache entry size limits (default: 1MB per entry, configurable).

**REQ-CACHE-010**: The system SHALL handle cache storage failures gracefully (fallback to no cache, continue execution).

### 2.3 Cache Retrieval

**REQ-CACHE-011**: The system SHALL check cache before executing the RAG pipeline.

**REQ-CACHE-012**: The cache retrieval SHALL match on cache key (query hash + version_id).

**REQ-CACHE-013**: The system SHALL verify TTL expiration before returning cached results.

**REQ-CACHE-014**: The system SHALL return cached results immediately if valid cache entry exists (cache hit).

**REQ-CACHE-015**: The system SHALL proceed with normal pipeline execution if cache miss or expired entry.

**REQ-CACHE-016**: The system SHALL handle cache retrieval errors gracefully (treat as cache miss, log error).

### 2.4 Cache Storage (Write)

**REQ-CACHE-017**: The system SHALL store results in cache after successful pipeline execution.

**REQ-CACHE-018**: The system SHALL store results only for successful executions (validated answers).

**REQ-CACHE-019**: The system SHALL calculate and store TTL expiration timestamp based on configured TTL.

**REQ-CACHE-020**: The system SHALL handle cache write failures gracefully (log warning, continue without caching).

**REQ-CACHE-021**: The system SHALL support asynchronous cache writes (non-blocking, optional).

### 2.5 Cache Invalidation

**REQ-CACHE-022**: The system SHALL invalidate cache entries when TTL expires.

**REQ-CACHE-023**: The system SHALL support manual cache invalidation by:
- Cache key (specific entry)
- Program version (all entries for a version)
- Query pattern (partial match)
- All entries (clear entire cache)

**REQ-CACHE-024**: The system SHALL support cache invalidation via API or configuration.

**REQ-CACHE-025**: The system SHALL automatically clean up expired entries (lazy cleanup on access, or scheduled cleanup).

### 2.6 TTL Configuration

**REQ-CACHE-026**: The system SHALL support configurable TTL for cache entries (default: 24 hours, range: 1 hour to 30 days).

**REQ-CACHE-027**: The system SHALL allow different TTL values for different program versions.

**REQ-CACHE-028**: The system SHALL allow TTL configuration per query type or pattern (optional, advanced feature).

**REQ-CACHE-029**: The system SHALL support TTL of 0 (no caching) for specific queries or versions.

### 2.7 Stats API

**REQ-CACHE-030**: The system SHALL provide a stats API that tracks:
- Total cache hits (count)
- Total cache misses (count)
- Cache hit rate (percentage)
- Cache size (number of entries, total size in MB)
- Cache backend type
- Average cache retrieval time

**REQ-CACHE-031**: The system SHALL track stats per program version.

**REQ-CACHE-032**: The system SHALL provide stats in both programmatic (JSON) and human-readable formats.

**REQ-CACHE-033**: The system SHALL reset stats on demand (via API or configuration).

**REQ-CACHE-034**: The system SHALL persist stats across restarts (if using persistent backend).

### 2.8 Integration with Pipeline Components

**REQ-CACHE-035**: The caching layer SHALL integrate with the RAG Pipeline (check cache before retrieval).

**REQ-CACHE-036**: The caching layer SHALL integrate with the Multi-Agent Critic Loop (cache final improved answers).

**REQ-CACHE-037**: The caching layer SHALL integrate with the BAML Validator (cache only validated answers).

**REQ-CACHE-038**: The caching layer SHALL be transparent to pipeline components (cache check happens before pipeline execution).

## 3. Non-Functional Requirements

### 3.1 Performance

**REQ-CACHE-NFR-001**: Cache retrieval SHALL complete within 50ms for 95% of requests (p95 latency) for SQLite backend.

**REQ-CACHE-NFR-002**: Cache retrieval SHALL complete within 10ms for 95% of requests (p95 latency) for Redis backend.

**REQ-CACHE-NFR-003**: Cache storage (write) SHALL complete within 100ms for 95% of requests (p95 latency) for SQLite backend.

**REQ-CACHE-NFR-004**: Cache storage (write) SHALL complete within 20ms for 95% of requests (p95 latency) for Redis backend.

**REQ-CACHE-NFR-005**: Cache operations SHALL not block pipeline execution (use async writes if needed).

### 3.2 Scalability

**REQ-CACHE-NFR-006**: The cache SHALL support at least 10,000 cache entries for SQLite backend.

**REQ-CACHE-NFR-007**: The cache SHALL support at least 100,000 cache entries for Redis backend.

**REQ-CACHE-NFR-008**: The cache SHALL handle concurrent read/write operations safely.

**REQ-CACHE-NFR-009**: The cache SHALL support cache size limits (default: 5GB, configurable).

### 3.3 Reliability

**REQ-CACHE-NFR-010**: The cache SHALL handle backend failures gracefully (fallback to no cache, continue execution).

**REQ-CACHE-NFR-011**: The cache SHALL recover from corrupted cache entries (skip invalid entries, log error).

**REQ-CACHE-NFR-012**: The cache SHALL support cache backend health checks.

**REQ-CACHE-NFR-013**: The cache SHALL not lose data on unexpected shutdowns (for persistent backends).

### 3.4 Resource Usage

**REQ-CACHE-NFR-014**: The cache SHALL have minimal memory footprint for cache operations (<100MB for cache manager).

**REQ-CACHE-NFR-015**: The cache SHALL support disk space limits and cleanup of oldest entries when limit reached (LRU eviction).

## 4. Interfaces & Contracts

### 4.1 Cache Key Generation

**Function Signature:**
```python
def generate_cache_key(
    query: str,
    version_id: str,
    query_params: Optional[Dict[str, Any]] = None
) -> str:
    """
    Generate a cache key from query and version.
    
    Args:
        query: User query text
        version_id: Program version ID (e.g., "rag_v1")
        query_params: Optional query parameters that affect results
        
    Returns:
        SHA-256 hash string as cache key
    """
```

**Key Format:**
- Input: `query="What is DSPy?"`, `version_id="rag_v1"`
- Normalized: `query.lower().strip()`
- Hash: `sha256(f"{normalized_query}::{version_id}")`
- Output: `"a1b2c3d4e5f6..."` (64-character hex string)

### 4.2 Cache Interface

**Cache Entry Schema:**
```python
@dataclass
class CacheEntry:
    cache_key: str
    final_answer: FinalAnswer  # Validated structured answer
    evidence_chunks: List[EvidenceChunk]
    program_version: str
    created_at: datetime
    expires_at: datetime
    execution_metadata: Dict[str, Any]  # Execution time, token usage, etc.
```

**Cache Interface:**
```python
class CacheBackend(ABC):
    @abstractmethod
    def get(self, cache_key: str) -> Optional[CacheEntry]:
        """Retrieve cache entry by key. Returns None if not found or expired."""
        
    @abstractmethod
    def set(self, cache_key: str, entry: CacheEntry, ttl_seconds: int) -> bool:
        """Store cache entry with TTL. Returns True if successful."""
        
    @abstractmethod
    def delete(self, cache_key: str) -> bool:
        """Delete cache entry by key. Returns True if successful."""
        
    @abstractmethod
    def invalidate_version(self, version_id: str) -> int:
        """Invalidate all entries for a version. Returns count of deleted entries."""
        
    @abstractmethod
    def clear(self) -> int:
        """Clear all cache entries. Returns count of deleted entries."""
        
    @abstractmethod
    def get_stats(self) -> CacheStats:
        """Get cache statistics."""
```

### 4.3 Cache Stats Schema

```python
@dataclass
class CacheStats:
    total_hits: int
    total_misses: int
    hit_rate: float  # Percentage (0.0 to 100.0)
    total_entries: int
    cache_size_mb: float
    backend_type: str  # "sqlite", "redis", "json"
    avg_retrieval_time_ms: float
    stats_by_version: Dict[str, VersionStats]  # Stats per program version

@dataclass
class VersionStats:
    hits: int
    misses: int
    hit_rate: float
    entries: int
```

### 4.4 Cache Configuration

**Configuration Schema:**
```python
@dataclass
class CacheConfig:
    backend: str  # "sqlite", "redis", "json"
    ttl_hours: int = 24  # Default TTL in hours
    max_cache_size_mb: int = 5120  # 5GB default
    max_entry_size_mb: int = 1  # 1MB per entry default
    sqlite_path: str = "cache.db"  # SQLite database path
    redis_host: Optional[str] = None  # Redis host
    redis_port: Optional[int] = None  # Redis port
    redis_db: int = 0  # Redis database number
    json_cache_path: str = "cache.json"  # JSON cache file path
    enable_async_writes: bool = False  # Async cache writes
    cleanup_interval_hours: int = 24  # Scheduled cleanup interval
```

### 4.5 Error Codes

| Error Code | Description | HTTP Equivalent |
|------------|-------------|-----------------|
| CACHE-ERR-001 | Cache backend connection failure | 503 Service Unavailable |
| CACHE-ERR-002 | Cache retrieval error | 500 Internal Server Error |
| CACHE-ERR-003 | Cache storage error | 500 Internal Server Error |
| CACHE-ERR-004 | Cache entry too large | 413 Payload Too Large |
| CACHE-ERR-005 | Cache key generation error | 500 Internal Server Error |
| CACHE-ERR-006 | Cache invalidation error | 500 Internal Server Error |
| CACHE-ERR-007 | Cache stats retrieval error | 500 Internal Server Error |

## 5. Tenant & Security Considerations

### 5.1 Multi-Tenancy
**REQ-CACHE-SEC-001**: The system SHALL support single-tenant operation for local deployment (no multi-tenancy required).

### 5.2 Data Privacy
**REQ-CACHE-SEC-002**: The system SHALL hash or mask sensitive query content in cache keys (if required by privacy policies).

**REQ-CACHE-SEC-003**: The system SHALL support cache encryption at rest for sensitive deployments (optional, advanced feature).

### 5.3 Access Control
**REQ-CACHE-SEC-004**: The system SHALL restrict cache access to authorized processes only.

**REQ-CACHE-SEC-005**: The system SHALL validate cache entry integrity (checksums, if applicable).

## 6. Observability & Telemetry

### 6.1 Metrics

**REQ-CACHE-OBS-001**: The system SHALL track the following metrics:
- Cache hit rate (gauge, percentage)
- Cache miss rate (gauge, percentage)
- Total cache hits (counter)
- Total cache misses (counter)
- Cache retrieval latency (histogram)
- Cache storage latency (histogram)
- Cache size (gauge, MB)
- Number of cache entries (gauge)
- Cache evictions (counter)
- Cache errors (counter)

### 6.2 Logging

**REQ-CACHE-OBS-002**: The system SHALL log at INFO level:
- Cache hits/misses
- Cache size changes
- Cache invalidation operations

**REQ-CACHE-OBS-003**: The system SHALL log at ERROR level:
- Cache backend connection failures
- Cache retrieval/storage errors
- Cache corruption issues

**REQ-CACHE-OBS-004**: The system SHALL log at DEBUG level:
- Cache key generation details
- TTL calculations
- Cache entry details (without sensitive data)

### 6.3 Health Checks

**REQ-CACHE-OBS-005**: The system SHALL verify cache backend connectivity in health checks.

**REQ-CACHE-OBS-006**: The system SHALL report cache health status (healthy, degraded, unavailable).

## 7. Compliance & Governance

### 7.1 Audit Logging

**REQ-CACHE-COMP-001**: The system SHALL log all cache operations with:
- Timestamp
- Operation type (get, set, delete, invalidate)
- Cache key (hashed for privacy)
- Success/failure status

### 7.2 Data Retention

**REQ-CACHE-COMP-002**: The system SHALL support configurable cache retention policies (TTL-based).

**REQ-CACHE-COMP-003**: The system SHALL support manual cache purging for compliance requirements.

### 7.3 Cache Management

**REQ-CACHE-COMP-004**: The system SHALL provide audit trail for cache invalidation operations.

## 8. Open Questions & Assumptions

### Open Questions

1. **Q1**: Should cache support partial matches (similar queries)? (Assumed: Exact match only for initial version)
2. **Q2**: Should cache support version migration (convert old format to new)? (Assumed: Invalidate on version change)
3. **Q3**: What is the optimal TTL for different query types? (Assumed: 24 hours default, configurable)
4. **Q4**: Should cache support compression for large entries? (Assumed: No compression for initial version)
5. **Q5**: Should cache be shared across multiple instances? (Assumed: Single instance, local cache)

### Assumptions

1. SQLite is sufficient for small-scale deployment (<1000 queries/day)
2. Redis is optional and only needed for production scaling
3. Cache hit rate will be 30-50% for typical usage patterns
4. Cache entries are relatively small (<1MB each)
5. TTL of 24 hours is reasonable for most queries
6. Cache invalidation on version change is acceptable
7. Local JSON cache is sufficient for development and testing
8. Cache operations should not significantly impact pipeline latency

