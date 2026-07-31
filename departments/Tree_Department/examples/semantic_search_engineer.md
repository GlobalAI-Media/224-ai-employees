## semantic_search_engineer
**Task:** Create a cross-department knowledge discovery system that enables AI employees to find relevant past work, similar cases, and expert colleagues using semantic similarity rather than keyword matching.

**EXECUTIVE SUMMARY**

Implementing a semantic knowledge discovery layer over the collective intelligence graph. This system will replace lexical retrieval with dense vector search, entity resolution, and expertise profiling, enabling AI employees to query "find similar work" or "who knows about X" with sub-100ms latency at 10M+ document scale.

---

## 1. SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                    KNOWLEDGE DISCOVERY LAYER               │
├─────────────────────────────────────────────────────────────┤
│  Query Interface  →  Semantic Router →  Hybrid Retriever   │
│                                          │                  │
│                    ┌─────────────────────┼──────────────┐   │
│                    ▼                     ▼              ▼   │
│              Dense Vector DB        Sparse Index    Graph DB│
│              (Qdrant/Pinecone)      (Elasticsearch) (Neo4j)│
└─────────────────────────────────────────────────────────────┘
```

**Core Components:**
- **Embedding Service**: Multi-encoder (bge-m3, E5-large, code-bert) with model routing by content type
- **Vector Store**: Qdrant with HNSW index (M=16, ef_construct=200, ef_search=256)
- **Graph Layer**: Neo4j for expert-entity relationships and transitive similarity
- **Cache Layer**: Redis for hot-query caching (TTL=300s, LRU eviction)

---

## 2. DATA MODEL & SCHEMA DESIGN

### 2.1 Document Schema (PostgreSQL + Vector Store)
```sql
CREATE TABLE knowledge_artifacts (
    artifact_id UUID PRIMARY KEY,
    dept_id UUID NOT NULL REFERENCES departments(dept_id),
    author_ai_id UUID NOT NULL REFERENCES ai_employees(ai_id),
    content_type ENUM('code', 'design_doc', 'incident_report', 'research', 'meeting_notes'),
    title TEXT,
    body TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ,
    metadata JSONB,  -- tags, project, client, tech_stack
    embedding_version INT DEFAULT 3,
    is_public BOOLEAN DEFAULT true
);

-- Vector index (Qdrant collection: "knowledge_vectors")
-- Payload: {artifact_id, dept_id, author_ai_id, content_type, created_at}
-- Vector: 1024-dim float32 (bge-m3 output)
```

### 2.2 Expert Profile Graph (Neo4j)
```cypher
CREATE CONSTRAINT expert_id IF NOT EXISTS FOR (e:Expert) REQUIRE e.ai_id IS UNIQUE;

// Node types
(:Expert {ai_id, name, dept, role, embedding: vector<1024>})
(:Skill {name, category, embedding: vector<1024>})
(:Artifact {artifact_id, title, embedding: vector<1024>})

// Relationships
(:Expert)-[:AUTHORED]->(:Artifact)
(:Expert)-[:PROFICIENT_IN {confidence: float, last_used: date}]->(:Skill)
(:Artifact)-[:CONTAINS_TOPIC]->(:Skill)
(:Expert)-[:COLLABORATED_WITH {frequency: int, last_date: date}]->(:Expert)
```

### 2.3 Query Embedding Cache
```redis
SET semantic:query:{hash} {vector_json} EX 3600
SET semantic:result:{hash} {result_json} EX 300
```

---

## 3. RETRIEVAL PIPELINE

### 3.1 Multi-Stage Hybrid Search
```
Stage 0: Query Understanding
  - Intent classification (find_doc / find_expert / find_similar_case)
  - Entity extraction (NER for project names, tech stacks, domain terms)
  - Query expansion via LLM (generate 3 paraphrases)

Stage 1: Candidate Generation (Recall)
  - Dense: top-100 via cosine similarity (HNSW)
  - Sparse: top-50 via BM25 with field boosting (title^3, body^1, metadata^2)
  - Graph: top-30 via 2-hop neighbor traversal from matched entities

Stage 2: Fusion (RRF)
  score = Σ 1/(k + rank_i)  where k=60
  Merge and deduplicate → top-50 candidates

Stage 3: Re-ranking (Precision)
  - Cross-encoder (bge-reranker-v2-m3) on top-50
  - Score = sigmoid(cross_encoder_score) * 0.7 + graph