## message_router
**Task:** Design a multi-channel message routing architecture for handling customer inquiries across email, WhatsApp, Telegram, and Slack. Include intent classification, priority queuing, and escalation rules to human operators.

## Message Routing Architecture: Multi-Channel Customer Inquiry System

### 1. System Overview

The routing layer functions as a **centralized ingestion and dispatch fabric** that normalizes heterogeneous channel payloads into a canonical event model, applies deterministic and ML-based routing policies, and guarantees at-least-once delivery to downstream consumers (AI agents, human operator queues, or archival stores).

```
[Email SMTP]     [WhatsApp BSP]   [Telegram Bot]   [Slack App]
      |                |                |               |
      v                v                v               v
+-------------------------------------------------------------+
|                 CHANNEL ADAPTERS (Edge)                     |
|  - Protocol termination, auth, rate limiting                |
|  - Payload normalization -> Canonical Message Envelope      |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                 INGESTION BUS (Kafka / Pulsar)              |
|  - Topics: raw.inbound.{channel}                            |
|  - Partition key: conversation_id (hash)                    |
|  - Retention: 7d hot, 30d cold                              |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                 INTENT CLASSIFIER (Async Consumer)          |
|  - Model: fine-tuned transformer (multilingual)             |
|  - Output: intent_id, confidence, entities, language        |
|  - Fallback: rule-based keyword matcher (low confidence)    |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                 ROUTING ENGINE (Stateful Service)           |
|  - Priority assignment (P0-P3)                              |
|  - Queue selection (AI agent pool / human queue)            |
|  - Escalation policy evaluation                             |
|  - Idempotency check (dedupe by message_id)                 |
+-------------------------------------------------------------+
                              |
              +---------------+----------------+
              |                                |
              v                                v
+------------------------+        +---------------------------+
|   AI AGENT EXECUTOR    |        |   HUMAN OPERATOR QUEUE    |
|  - LLM-based response  |        |  - SLA timers             |
|  - Tool-calling        |        |  - Skill-based routing    |
|  - Confidence gates    |        |  - Round-robin / LIFO     |
+------------------------+        +---------------------------+
              |                                |
              +---------------+----------------+
                              |
                              v
+-------------------------------------------------------------+
|                 OUTBOUND DISPATCHER                          |
|  - Channel-specific formatters (HTML, WhatsApp template)    |
|  - Delivery receipt tracking (webhook callbacks)            |
|  - Retry with exponential backoff + dead-letter queue       |
+-------------------------------------------------------------+
```

---

### 2. Canonical Message Envelope

All inbound messages are normalized to this schema before entering the routing pipeline:

```json
{
  "schema_version": "1.2",
  "message_id": "uuid-v7",                    // globally unique, idempotency key
  "conversation_id": "uuid-v7",               // stable per customer-thread
  "channel": "email|whatsapp|telegram|slack",
  "channel_ref": {                            // channel-specific identifiers
    "thread_id": "...",
    "sender_id": "...",
    "channel_message_id": "..."
  },
  "customer": {
    "external_id": "...",                     // hashed PII
    "language": "en|es|de|...",
    "tier": "standard|premium|vip"
  },
  "content": {
    "text": "...",
    "attachments": [{"type": "image|pdf|audio", "url": "..."}],
    "timestamp": "ISO-8601"
  },
  "classification": {                          // populated by intent classifier
    "intent_id": "billing|support|sales|complaint|other",
    "confidence": 0.93,
    "entities": {"order_id": "12345", "product": "X"},
    "sentiment": "negative|neutral|positive"
  },
  "routing": {
    "priority": "P0|P1|P2|P3",
    "queue": "ai_agent|human_escalation|auto_reply",
    "escalation_reason": "low_confidence|sentiment_negative|vip_customer"
  }
}
```

---

### 3. Intent Classification Pipeline

**Stage 1 — Preprocessing:**
- Language detection (fastText, ~2ms)
- PII redaction (regex + NER) before model inference
- Attachment type detection (for escalation if needed