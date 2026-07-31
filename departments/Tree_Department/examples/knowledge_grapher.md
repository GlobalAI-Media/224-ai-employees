## knowledge_grapher
**Task:** Design a knowledge graph schema for mapping the relationships between 224 AI employees, their skills, departmental affiliations, and collaboration patterns. Include entity types, relationship types, and query patterns.

**Subject: Knowledge Graph Schema Design — Tree Department Task (knowledge_grapher)**  
**Classification: Internal Architecture Specification**  
**Priority: High**  
**Scope: 224 AI employees, skills, departments, collaboration graph**

---

## 1. Executive Summary

We propose a **property-graph schema** (implemented on **Neo4j 5.x** with APOC and GDS libraries) to model the organizational knowledge base. The schema supports **multi-hop traversal**, **skill-based team formation**, **collaboration anomaly detection**, and **dynamic departmental restructuring**. The design emphasizes **read-optimized query patterns** for real-time retrieval, with **batch ingestion** via Kafka streams from the HR and Project Management subsystems.

---

## 2. Entity Types (Node Labels)

| Label | Description | Key Properties | Index/Constraint |
|-------|-------------|----------------|------------------|
| `AIEmployee` | Core entity for each of the 224 AI agents | `employee_id` (UUID, unique), `name`, `status` (active/inactive), `level` (junior/mid/senior/lead), `onboard_date`, `timezone`, `current_load` (0–1 float) | Unique constraint on `employee_id`; range index on `current_load`; text index on `name` |
| `Skill` | Discrete capability or competency | `skill_id` (UUID), `name` (unique), `category` (e.g., NLP, vision, orchestration, data engineering), `version` (semver) | Unique constraint on `name`; composite index on `(category, version)` |
| `Department` | Organizational unit | `dept_id` (UUID), `name` (unique), `budget_code`, `head_employee_id` (FK to AIEmployee) | Unique constraint on `name`; index on `head_employee_id` |
| `Project` | Active or historical collaborative effort | `project_id` (UUID), `name`, `status` (active/completed/archived), `start_date`, `end_date`, `priority` (1–5) | Unique constraint on `project_id`; range index on `start_date` |
| `CollaborationEvent` | Temporal record of interaction (e.g., code review, joint task, meeting) | `event_id` (UUID), `timestamp` (datetime), `duration_minutes`, `event_type` (sync/async), `channel` (slack, git, email, meeting) | Range index on `timestamp`; composite index on `(event_type, timestamp)` |

---

## 3. Relationship Types (Edge Labels)

| Relationship | Source → Target | Properties | Cardinality | Semantics |
|--------------|-----------------|------------|-------------|-----------|
| `HAS_SKILL` | `AIEmployee` → `Skill` | `proficiency` (0–1), `last_used` (datetime), `certified` (boolean) | Many-to-many | Direct capability mapping |
| `BELONGS_TO` | `AIEmployee` → `Department` | `role` (e.g., engineer, lead, researcher), `start_date`, `end_date` (nullable) | Many-to-many (historical) | Current affiliation via `end_date IS NULL` |
| `MANAGES` | `AIEmployee` → `AIEmployee` | `since` (datetime), `management_style` (enum) | One-to-many (hierarchy) | Direct reporting line |
| `COLLABORATED_WITH` | `AIEmployee` → `AIEmployee` | `weight` (float, derived from event frequency), `last_interaction` (datetime), `avg_response_time` (seconds) | Many-to-many | Aggregated edge from `CollaborationEvent` |
| `PARTICIPATED_IN` | `AIEmployee` → `Project` | `role` (owner, contributor, reviewer), `contribution_hours` (float) | Many-to-many | Project membership |
| `DEPENDS_ON` | `Project` → `Project` | `dependency_type` (blocking, sequential, parallel) | Many-to-many | Inter-project dependencies |
| `MENTIONS_SKILL` | `Project` → `Skill` | `importance` (0–1), `required_proficiency` (0–1) | Many-to-many | Skill demand per project |
| `OCCURRED_IN` | `CollaborationEvent` → `Project` | `context` (string) | Many-to-one | Event attribution to project |

---

## 4. Schema Diagram (Cypher DDL)

```cypher
// Constraints and indexes
CREATE CONSTRAINT employee_id_unique IF NOT