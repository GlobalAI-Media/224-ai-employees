## tech_data_pipeline_engineer
**Task:** Design a real-time data pipeline to monitor performance metrics of 224 AI employees, using streaming and batch processing.

# Real-Time AI Employee Performance Monitoring Pipeline

## Overview

Designing a data pipeline to monitor 224 AI employees requires a hybrid streaming + batch architecture that captures sub-second metrics, aggregates for dashboards, and supports historical analysis. The system must handle 224 concurrent agent streams, each emitting ~50 metrics/sec (11,200 events/sec baseline), with burst capacity for anomaly spikes.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        AI Employee Fleet (224)                      │
│  [Agent 1] [Agent 2] ... [Agent 224] (each emits metrics @ 50Hz)   │
└─────────────────────────┬───────────────────────────────────────────┘
                          │ gRPC / HTTP / WebSocket
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Ingestion Layer (Kafka + API Gateway)            │
│  Topics: agent_metrics, agent_logs, agent_errors, agent_health      │
│  Partitions: 16 per topic (hash by agent_id)                        │
└──────────┬──────────────────────────────────────────────────────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
┌─────────┐ ┌─────────┐
│Stream    │ │Stream    │
│Processor │ │Processor │
│(Flink)   │ │(Flink)   │
└────┬─────┘ └────┬─────┘
     │            │
     ▼            ▼
┌─────────┐ ┌─────────┐
│Real-time │ │Historical│
│Metrics DB│ │Store     │
│(Druid)   │ │(S3/Parq.)│
└────┬─────┘ └────┬─────┘
     │            │
     ▼            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Serving Layer                                    │
│  Grafana (real-time dashboards) + Presto/Trino (ad-hoc queries)    │
│  AlertManager (PagerDuty, Slack)                                    │
└─────────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Ingestion Layer (Kafka + API Gateway)

**Topics & Partitions:**
```yaml
topics:
  - name: agent_metrics
    partitions: 16
    retention: 7d
    config:
      cleanup.policy: delete
      compression.type: lz4
  - name: agent_errors
    partitions: 8
    retention: 30d
  - name: agent_health
    partitions: 4
    retention: 1d
```

**Producer Configuration (gRPC):**
```protobuf
message AgentMetric {
  string agent_id = 1;
  string metric_name = 2;
  double value = 3;
  map<string, string> tags = 4;
  int64 timestamp = 5;  // Unix nanoseconds
}

// Batch 100 metrics per message to reduce overhead
message MetricBatch {
  repeated AgentMetric metrics = 1;
  string source_agent_id = 2;
  int64 batch_timestamp = 3;
}
```

### 2. Stream Processing (Flink)

**Job Topology:**
```sql
-- Real-time aggregation per agent (1-minute windows)
CREATE TABLE agent_perf_minute (
  agent_id STRING,
  window_start TIMESTAMP(3),
  avg_response_time DOUBLE,
  p95_response_time DOUBLE,
  error_rate DOUBLE,
  throughput DOUBLE,
  cpu_usage DOUBLE,
  memory_usage DOUBLE,
  active_sessions BIGINT,
  watermark FOR rowtime AS event_time
) WITH (
  'connector' = 'kafka',
  'topic' = 'agent_metrics',
  'properties.bootstrap.servers' = 'kafka:9092',
  'format' = 'avro-confluent'
);

-- Sliding window aggregation (5-minute windows, slide every 1 minute)
INSERT INTO agent_perf_5min
SELECT
  agent_id,
  TUMBLE_START(event_time, INTERVAL '5' MINUTE) AS window_start,
  AVG(response_time) AS avg_rt,
  APPROX_PERCENTILE(response_time, 0.95) AS p95_rt,
  COUNT(*) / 300 AS throughput,
  AVG(cpu_usage) AS avg_cpu,
  AVG(memory_usage) AS avg_mem
FROM agent_metrics_stream
GROUP BY agent_id, TUMBLE(event_time, INTERVAL '5' MINUTE);
```

**Anomaly Detection (Cep):**
```java
// Detect sustained high error rate (>5% for 3 consecutive minutes)
Pattern<AgentMetric, ?> anomalyPattern = Pattern
    .<AgentMetric>begin("first")
    .where(metric -> metric.getErrorRate() > 0.05)
    .next("second")
    .where(metric -> metric.getErrorRate() > 0.05)
    .next("third")
    .where(metric -> metric.getErrorRate() > 0.05)
    .within(Time.minutes(3));

PatternStream<AgentMetric> patternStream = CEP.pattern(stream, anomalyPattern);
```

### 3. Storage Layer

**Real-time (Druid) Schema:**
```json
{
  "dataSchema": {
    "dataSource": "agent_metrics",
    "timestampSpec": { "column": "event_time", "format": "auto"