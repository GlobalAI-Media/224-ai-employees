## email_handler
**Task:** Create an AI-driven email processing pipeline that can categorize inbound emails, extract action items, draft context-aware replies, and schedule follow-ups. Include spam filtering and urgency detection.

**Subject:** Interact Department Task Execution — AI-Driven Email Processing Pipeline (email_handler)

**Classification:** Internal Systems Engineering Specification  
**Status:** Ready for Integration  
**Version:** 1.0.0  

---

## 1. Executive Summary

This specification defines a production-grade, AI-driven email processing pipeline for the Interact Department. The system ingests inbound emails, performs multi-stage classification, extracts structured action items, generates context-aware draft replies, and schedules follow-up tasks. It integrates spam filtering and urgency detection as first-class components, with delivery guarantees and idempotency enforced at every stage.

The pipeline is designed for horizontal scalability, fault isolation, and full observability, consistent with the Global AI Media Group’s operational standards.

---

## 2. System Architecture Overview

```
[Inbound Email Gateway]
        │
        ▼
[Ingestion Queue] ────► [Spam Filter Service] ────► [Dedup & Idempotency Cache]
        │                                                   │
        ▼                                                   ▼
[Classification Service] ──────────────────────► [Urgency Detection Service]
        │                                                   │
        ▼                                                   ▼
[Action Item Extractor] ──────────────► [Context Builder (Vector Store)]
        │                                                   │
        ▼                                                   ▼
[Reply Draft Generator] ──────────────► [Human-in-the-Loop Approval Queue]
        │                                                   │
        ▼                                                   ▼
[Follow-up Scheduler] ──────────────► [Outbound Mail Queue]
```

**Key Design Decisions:**
- **Decoupled stages** via message queues (Kafka/RabbitMQ) to allow independent scaling.
- **Stateless services** for easy replication and rolling deployments.
- **Persistent state** in a distributed cache (Redis) and vector store (Pinecone/Weaviate) for context retention.
- **Idempotency keys** derived from email `Message-ID` + `Received` timestamp hash.

---

## 3. Protocol & Data Contracts

### 3.1 Inbound Email Event (Canonical JSON)

```json
{
  "event_id": "uuid_v4",
  "message_id": "<original-message-id>",
  "received_at": "ISO8601 UTC",
  "from": {"email": "...", "name": "..."},
  "to": ["..."],
  "cc": ["..."],
  "subject": "...",
  "body_text": "...",
  "body_html": "...",
  "attachments": [{"id": "...", "mime_type": "...", "size": 123}],
  "headers": {"x-spam-score": 0.0, "x-priority": "normal"}
}
```

### 3.2 Pipeline Stage Outputs

| Stage | Output Schema (Key Fields) |
|-------|---------------------------|
| Spam Filter | `spam_score` (0-1), `is_spam` (bool), `reason` (string) |
| Classification | `category` (enum: `support`, `sales`, `billing`, `hr`, `legal`, `general`), `confidence` (0-1) |
| Urgency Detection | `urgency_level` (enum: `low`, `medium`, `high`, `critical`), `response_sla_minutes` (int) |
| Action Item Extractor | `action_items[]`: `{id, description, assignee, due_date, priority}` |
| Reply Draft Generator | `reply_text`, `reply_subject`, `suggested_tone` (enum) |
| Follow-up Scheduler | `follow_up_task`: `{type, trigger_at, recurrence, channel}` |

---

## 4. Core Processing Logic

### 4.1 Spam Filtering (Multi-Layer)

- **Layer 1 — Heuristic Rules:** Header analysis (SPF/DKIM/DMARC), sender reputation score, blacklist lookup, attachment type checks.
- **Layer 2 — ML Classifier:** Fine-tuned transformer (e.g., DistilBERT) on labeled spam/ham corpus. Outputs probability score.
- **Layer 3 — Behavioral Signals:** Rate of similar emails from same domain, link analysis, and content entropy.

**Decision Logic:**
```python
if spam_score > 0.9 or (spam_score > 0.7 and heuristic_flags):
    quarantine_or_reject()
else:
    proceed_to_classification()
```

**Reliability:** Spam filter is non-blocking; if model inference times out (>2s), fallback to heuristic-only decision with `degraded_mode=true` flag in telemetry.

### 4.2 Urgency Detection

- **Inputs:** Subject keywords, body sentiment, sender role (