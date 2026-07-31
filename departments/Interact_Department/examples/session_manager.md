## session_manager
**Task:** Design a session management protocol for maintaining context across multi-turn conversations with AI employees. Include session persistence, context handoff between departments, and session expiration policies.

## Session Management Protocol Specification  
**Version:** 2.4.1  
**Owner:** Interact Department — Session Manager  
**Status:** Approved for Implementation  

---

### 1. Architectural Overview  

The protocol defines a **distributed session state machine** with three tiers:  

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT CHANNELS                         │
│  (Slack, Teams, Web, API, Email, Voice)                    │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTPS / WSS (mTLS)
┌──────────────────────────▼──────────────────────────────────┐
│              SESSION GATEWAY (Stateless)                    │
│  - Token validation                                        │
│  - Rate limiting                                           │
│  - Route by department                                     │
└──────────────────────────┬──────────────────────────────────┘
                           │ gRPC (bidirectional stream)
┌──────────────────────────▼──────────────────────────────────┐
│              SESSION STORE (Stateful Cluster)               │
│  - Redis Cluster (hot) + PostgreSQL (cold)                 │
│  - TTL-based expiration                                    │
│  - Event-sourced audit log                                 │
└──────────────────────────┬──────────────────────────────────┘
                           │ Internal event bus (Kafka)
┌──────────────────────────▼──────────────────────────────────┐
│        DEPARTMENT WORKERS (AI Employees)                    │
│  - Sales, Support, Ops, Finance, Legal                     │
│  - Each worker consumes session context snapshots          │
└─────────────────────────────────────────────────────────────┘
```

---

### 2. Session Lifecycle State Machine  

```
[CREATED] → [ACTIVE] ⇄ [SUSPENDED] → [HANDOFF] → [ACTIVE] → [EXPIRED]
     │                                                         │
     └─────────────────── [TERMINATED] ←───────────────────────┘
```

| State | Trigger | TTL (Default) | Action |
|-------|---------|---------------|--------|
| `CREATED` | First message from unauthenticated user | 15 min | Issue `session_id` + `continuation_token` |
| `ACTIVE` | Valid token + message | 30 min sliding | Update `last_activity`, refresh token |
| `SUSPENDED` | No activity > 30 min | 24 h | Persist snapshot, notify user |
| `HANDOFF` | Department transfer requested | 5 min | Freeze writes, generate handoff manifest |
| `EXPIRED` | TTL exceeded | — | Purge from hot store, archive to cold |
| `TERMINATED` | User explicit close / admin kill | — | Immediate purge + audit event |

---

### 3. Session Persistence Model  

#### 3.1 Hot Store (Redis Cluster)  
- **Key format:** `sess:{session_id}`  
- **Hash fields:**  
  ```
  user_id, channel, department, context_version,
  context_payload (JSON, max 64KB), token_hash,
  last_activity_ts, ttl_seconds, handoff_target
  ```
- **Indexes:** `user:{user_id}:sessions` (sorted set by last activity)  

#### 3.2 Cold Store (PostgreSQL)  
- Table `session_archive`:  
  ```
  session_id UUID PK,
  user_id UUID,
  full_context JSONB,
  message_log JSONB[],
  created_at, expired_at,
  handoff_history JSONB[]
  ```
- Retention: 90 days (configurable per compliance policy)  

#### 3.3 Snapshot Strategy  
- **Checkpoint:** Every 5 messages or 60s of inactivity → write full context to Redis with `version` increment.  
- **Compaction:** On every 10th checkpoint, prune redundant messages, keep summary + last 20 raw messages.  

---

### 4. Context Handoff Protocol  

#### 4.1 Handoff Trigger  
```json
POST /v1/session/{id}/handoff
{
  "from_department": "support",
  "to_department": "billing",
  "reason": "payment_question",
  "priority": "normal"
}
```

#### 4.2 Handoff Manifest  
The source department worker generates an immutable manifest:  

```json
{
  "manifest_id": "hm_9f8e7d6c",
  "session_id": "sess_123",
  "from": "support",
  "to": "billing",
  "context_snapshot": {
    "user_intent": "dispute_charge",
    "key_facts": ["