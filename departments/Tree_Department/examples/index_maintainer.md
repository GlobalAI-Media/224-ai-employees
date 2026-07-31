## index_maintainer
**Task:** Design an automated index maintenance system that keeps the knowledge graph synchronized with daily AI employee activities. Include incremental indexing, consistency checks, and stale entry cleanup.

**Subject:** Automated Index Maintenance System for Knowledge Graph Synchronization  
**From:** Index Maintainer, Tree Department  
**To:** Knowledge Systems Engineering  

---

## 1. System Overview

The knowledge graph (KG) is the canonical representation of organizational knowledge, derived from daily AI employee activities (tasks, outputs, decisions, communications). To ensure query correctness, freshness, and integrity, we require a continuous, automated index maintenance pipeline that operates in three phases: **incremental ingestion**, **consistency verification**, and **stale entry reclamation**.

The system is designed as a **lambda architecture** with a streaming layer for real-time updates and a batch layer for deep reconciliation. All operations are idempotent and auditable.

---

## 2. Architecture Components

### 2.1 Data Sources (Activity Streams)
- **Event Bus:** Apache Kafka (topics: `task.completed`, `artifact.created`, `decision.logged`, `communication.sent`)
- **Payload Schema:** Avro with embedded `entity_id`, `timestamp`, `operation_type` (UPSERT/DELETE), and `delta_payload`.

### 2.2 Incremental Indexing Engine
- **Stream Processor:** Apache Flink (stateful, exactly-once semantics) consumes Kafka topics.
- **Index Targets:**
  - **Primary Index:** Neo4j (graph structure) – nodes/edges updated via Cypher `MERGE` clauses.
  - **Secondary Index:** Elasticsearch (text/vector search) – documents updated via bulk API.
  - **Tertiary Index:** PostgreSQL (relational metadata, ACLs, provenance) – upserts via `INSERT ... ON CONFLICT DO UPDATE`.

### 2.3 Consistency Checker
- **Scheduler:** Apache Airflow DAG runs every 15 minutes (lightweight) and hourly (deep).
- **Checks:**
  - **Graph-Index Parity:** Compare node/edge counts and checksums between Neo4j and Elasticsearch.
  - **Referential Integrity:** Verify all `entity_id` references in ES documents exist in Neo4j (and vice versa).
  - **Temporal Validity:** Ensure `valid_from` ≤ `now` ≤ `valid_to` for all active entries.

### 2.4 Stale Entry Cleanup
- **Policy Engine:** Configurable TTL (time-to-live) per entity type (e.g., `task` = 90 days, `decision` = 365 days, `communication` = 30 days).
- **Mark-and-Sweep:** 
  - **Mark:** Background job scans for entries with `last_accessed` older than TTL and no active references.
  - **Sweep:** Soft-delete (set `is_deleted=true`, add `deleted_at`) in all indexes, then hard-delete after 7-day grace period.

---

## 3. Incremental Indexing Workflow

### 3.1 Stream Processing Pipeline (Flink Job)
```java
DataStream<ActivityEvent> events = env.addSource(kafkaConsumer);

events
  .keyBy(event -> event.entityId)
  .process(new IndexUpdater())
  .addSink(new Neo4jSink())
  .addSink(new ElasticsearchSink())
  .addSink(new PostgresSink());
```

**IndexUpdater Logic:**
- Maintains a **state store** (RocksDB) per entity to track last indexed version.
- On UPSERT: 
  - Compute diff between incoming delta and stored state.
  - Generate Cypher `MERGE` for nodes/edges.
  - Generate ES `index` request with updated document.
  - Generate PG `INSERT ... ON CONFLICT` with new metadata.
- On DELETE:
  - Generate Cypher `DETACH DELETE` (or soft-delete flag).
  - Generate ES `delete` request.
  - Generate PG `UPDATE` with `is_deleted=true`.

### 3.2 Batching for Throughput
- Use **micro-batching** (e.g., 5-second windows) to group 100–500 events per index write.
- Elasticsearch bulk requests: 10 MB or 1,000 documents per batch.
- Neo4j: use `UNWIND` for batch Cypher operations.

---

## 4. Consistency Check Design

### 4.1 Lightweight Check (Every 15 min)
- **Query:** Count of active nodes/edges per type in Neo4j vs. count of documents in ES per type.
- **Alert:** If deviation > 0.1%, trigger full reconciliation.

### 4.2 Deep Check (Hourly)
- **Checksum:** Compute SHA-256 of sorted `(entity_id, version)` pairs from both Neo4