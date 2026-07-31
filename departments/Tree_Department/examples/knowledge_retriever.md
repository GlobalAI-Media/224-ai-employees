## knowledge_retriever
**Task:** Create a semantic search architecture that allows AI employees to query the collective knowledge base using natural language. Include embedding strategy, hybrid retrieval combining vector and keyword search, and relevance ranking.

**ARCHITECTURE SPECIFICATION: SEMANTIC SEARCH LAYER FOR COLLECTIVE KNOWLEDGE BASE**  
**Version:** 1.0 | **Owner:** Tree Department – knowledge_retriever | **Status:** Approved for Implementation  

---

## 1. SYSTEM OVERVIEW

The semantic search layer enables 224 AI employees to query the collective knowledge base via natural language, returning ranked, context-aware results. The architecture employs a **hybrid retrieval pipeline** combining dense vector embeddings (semantic similarity) with sparse lexical indexing (exact keyword matching), fused via a **reciprocal rank fusion (RRF)** algorithm. Relevance is further refined by a **cross-encoder re-ranker** for precision.

**Core Components:**
- **Ingestion Pipeline:** Document preprocessing → chunking → embedding generation → dual-index persistence.
- **Query Pipeline:** Natural language query → embedding generation → hybrid retrieval → fusion → re-ranking → response assembly.
- **Governance Layer:** Access control, audit logging, and knowledge provenance tracking.

---

## 2. EMBEDDING STRATEGY

### 2.1 Model Selection
- **Primary Model:** `text-embedding-3-large` (OpenAI) – 3072 dimensions, optimized for semantic similarity and retrieval tasks.
- **Fallback Model:** `BAAI/bge-m3` (open-source, multilingual) – 1024 dimensions, for cost-sensitive or offline scenarios.
- **Dimension Reduction:** Apply **PCA** to reduce 3072 → 1024 dimensions for storage efficiency while retaining >95% retrieval accuracy (validated on internal benchmark set).

### 2.2 Chunking Strategy
- **Chunk Size:** 512 tokens with 128-token overlap (empirically optimal for domain-specific documents).
- **Chunking Method:** Recursive character splitting with delimiter priority: `\n\n` → `\n` → `.` → `;` → space.
- **Metadata Attachment:** Each chunk carries: `source_id`, `doc_type`, `author_ai_id`, `timestamp`, `access_level`, `project_id`, and `chunk_index`.

### 2.3 Embedding Pipeline
```python
def generate_embeddings(chunk: str, metadata: dict) -> dict:
    embedding = embedding_model.encode(chunk, normalize=True)
    reduced_embedding = pca.transform(embedding.reshape(1, -1))
    return {
        "id": f"{metadata['source_id']}_{metadata['chunk_index']}",
        "vector": reduced_embedding.tolist(),
        "metadata": metadata,
        "text": chunk
    }
```

**Batch Processing:** 256 chunks per batch, with retry logic (exponential backoff) for API failures. Embeddings are cached in Redis (TTL: 24h) to avoid redundant computation.

---

## 3. DUAL-INDEX ARCHITECTURE

### 3.1 Vector Index (Dense)
- **Database:** Pinecone (pod-based, `p1.x1` pods) – chosen for low-latency (<50ms) and native metadata filtering.
- **Index Configuration:**
  - Metric: **Cosine similarity**
  - Pods: 8 (auto-scaling based on query QPS)
  - Metadata indexing: `access_level`, `project_id`, `doc_type` (filtered during query)
- **Namespace Strategy:** Separate namespaces per department (e.g., `tree-dept`, `legal`, `research`) to isolate queries by scope.

### 3.2 Lexical Index (Sparse)
- **Database:** Elasticsearch 8.x (3-node cluster, 128GB RAM each)
- **Index Mapping:**
  ```json
  {
    "mappings": {
      "properties": {
        "text": { "type": "text", "analyzer": "standard" },
        "metadata": { "type": "object", "dynamic": true },
        "chunk_id": { "type": "keyword" }
      }
    }
  }
  ```
- **Custom Analyzer:** Add synonyms (domain-specific), stop-word removal, and n-gram tokenizer (min_gram: 2, max_gram: 3) for typo tolerance.
- **Indexing Strategy:** Bulk API with refresh interval set to `30s` during ingestion, `1s` during active query periods.

### 3.3 Synchronization
- **Change Data Capture (CDC):** Debezium monitors knowledge base mutations → triggers re-embedding and re-indexing within 5 seconds.
- **Consistency Check:** Hourly reconciliation job compares document counts and checksums between Pinecone and Elasticsearch.

---

## 4. HYBRID RET