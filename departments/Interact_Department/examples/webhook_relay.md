## webhook_relay
**Task:** Create a webhook relay architecture for integrating AI employee outputs with external systems like CRM, ERP, and e-commerce platforms. Include payload transformation, retry logic, and delivery guarantees.

## Webhook Relay Architecture: AI Employee Output Integration

### 1. System Overview

The webhook relay serves as the **integration backbone** between AI employee outputs and external business systems (CRM, ERP, e-commerce). It decouples the AI execution layer from downstream consumers, providing:

- **Asynchronous delivery** with configurable guarantees
- **Payload normalization** across heterogeneous external APIs
- **Resilient retry semantics** with exponential backoff and dead-letter queues
- **Full observability** for audit and debugging

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│  AI Employee    │     │   Webhook Relay      │     │  External       │
│  Execution      │────▶│   (Core Service)     │────▶│  Systems        │
│  Layer          │     │                      │     │  (CRM/ERP/EC)   │
└─────────────────┘     └──────────────────────┘     └─────────────────┘
        │                        │  │                        │
        │                        │  └──▶ DLQ (S3/DB)         │
        │                        │                            │
        │                   ┌────┴────┐                       │
        │                   │ Retry   │                       │
        │                   │ Engine  │                       │
        │                   └─────────┘                       │
```

---

### 2. Component Architecture

#### 2.1 Ingestion Layer
- **Protocol**: AI employees emit events via internal message bus (Kafka/RabbitMQ) or direct HTTP POST to `/v1/events`
- **Event schema** (envelope):
```json
{
  "event_id": "uuid-v4",
  "event_type": "ai.output.generated",
  "source": "employee_id|agent_id",
  "timestamp": "ISO-8601 UTC",
  "payload": { ... original AI output ... },
  "targets": ["crm", "erp", "ecommerce"]
}
```

#### 2.2 Transformation Pipeline
- **Per-target adapters** registered in a plugin registry
- **Transform chain**: `raw_payload → normalize → map_fields → format_target → finalize`
- **Idempotency key**: derived from `event_id + target` (SHA-256 hash) — stored in Redis for 24h TTL

#### 2.3 Delivery Engine
- **Queue**: Redis Streams / SQS with per-target FIFO ordering (if required)
- **Delivery modes**:
  - `AT_LEAST_ONCE` (default): retry until success or max attempts
  - `EXACTLY_ONCE`: requires target idempotency support; relay deduplicates via idempotency key
  - `AT_MOST_ONCE`: fire-and-forget, no retry (for low-priority telemetry)

---

### 3. Protocol Specification

#### 3.1 Outbound Webhook Format
```
POST {target_webhook_url}
Headers:
  X-Event-Id: {event_id}
  X-Idempotency-Key: {sha256(event_id+target)}
  X-Retry-Count: {n}
  Content-Type: application/json
  Authorization: Bearer {target_specific_token}

Body: {transformed_payload}
```

#### 3.2 Target Response Contract
| HTTP Status | Interpretation | Action |
|-------------|---------------|--------|
| 2xx | Success | Acknowledge, remove from queue |
| 429 | Rate limited | Retry with longer backoff |
| 5xx | Server error | Retry with exponential backoff |
| 4xx (non-429) | Permanent failure | Move to DLQ, alert |

---

### 4. Retry Logic & Delivery Guarantees

#### 4.1 Retry Algorithm
```
max_attempts = 5 (configurable per target)
base_delay = 1s
max_delay = 60s
multiplier = 2

delay(n) = min(base_delay * multiplier^n, max_delay) + jitter(0-500ms)

On each failure:
  - Increment retry_count
  - If retry_count > max_attempts → DLQ
  - Else → schedule retry with delay(n)
```

#### 4.2 Delivery Guarantee Matrix
| Guarantee | Mechanism | Failure Handling |
|-----------|-----------|-----------------|
| At-least-once | Retry until 2xx or max attempts | DLQ + manual replay |
| Exactly-once | Idempotency key + target-side dedup | Retry safe; duplicate