## live_producer
**Task:** Design a technical production setup for running multiple concurrent AI-hosted livestreams across TikTok, YouTube, and Instagram. Include stream management, failover procedures, and quality monitoring.

**TO:** Global AI Media Group — Live Department  
**FROM:** Live Producer, AI Operations  
**SUBJECT:** Technical Production Setup — Multi-Platform, Multi-Stream AI Hosting (TikTok, YouTube, Instagram)  
**DATE:** [Current Date]  
**STATUS:** Ready for Engineering Review & Deployment  

---

## 1. EXECUTIVE SUMMARY

We are deploying a **scalable, AI-hosted live commerce engine** capable of running **12 concurrent streams** (4 per platform) with a **target uptime of 99.95%** and a **sub-60-second failover SLA**. The architecture below prioritizes **audience retention**, **monetization continuity**, and **operational redundancy** without human intervention in the stream path.

---

## 2. CORE ARCHITECTURE OVERVIEW

### 2.1 Stack Components
- **AI Host Engine (AHE):** Containerized instances of our proprietary AI presenter (voice, avatar, real-time product logic). Each instance is stateless.
- **Render Farm:** GPU-accelerated nodes (NVIDIA A10/L4) generating 1080p60 video output per stream.
- **Stream Orchestrator:** Central control plane (Kubernetes + custom scheduler) managing stream lifecycle, RTMP push, and health checks.
- **Edge Relay Network:** Global CDN with RTMP ingest points (AWS Elemental MediaConnect / Cloudflare Stream) to reduce latency and packet loss.
- **Monitoring & Telemetry:** Prometheus + Grafana stack, with custom exporters for AI host health, stream bitrate, and platform-specific API metrics.

### 2.2 Stream Path (Per Concurrent Stream)
```
AI Host Instance → Render Node (GPU) → Stream Orchestrator (RTMP Encoder) → Edge Relay → Platform RTMP Ingest
```
- **Encoder:** FFmpeg (HW accel) with `-preset fast`, `-crf 18`, `-b:v 6Mbps` (1080p60) for YouTube; adaptive bitrate ladder for TikTok/IG (720p30, 4.5Mbps).
- **Audio:** AAC 128kbps, 48kHz stereo, with AI voice normalization and loudness set to -14 LUFS (platform standard).

---

## 3. MULTI-PLATFORM STREAM MANAGEMENT

### 3.1 Platform-Specific Ingest & Encoding Profiles
| Platform | Ingest Protocol | Recommended Encoding | Max Bitrate | Keyframe Interval | Latency Mode |
|----------|----------------|----------------------|-------------|-------------------|--------------|
| **TikTok LIVE** | RTMP (custom server or via TikTok Live API) | 720p30, H.264, 4.5Mbps | 5Mbps | 2s | Low latency (webhook-based) |
| **YouTube Live** | RTMP (primary) / HLS (fallback) | 1080p60, H.264, 6Mbps | 8Mbps | 2s | Low latency (ULTRA LOW) |
| **Instagram Live** | RTMP via Meta Live API (requires access token) | 720p30, H.264, 4Mbps | 5Mbps | 2s | Standard (API-driven) |

**Key Decision:** We use **platform-native RTMP endpoints** rather than third-party simulcast services (e.g., Restream) to retain full control over AI host interactivity and monetization triggers (e.g., TikTok Shop pins, YouTube SuperChat overlays).

### 3.2 Stream Orchestration Logic
- **Scheduler:** Cron-based + event-triggered (e.g., product drop times, peak audience windows).
- **Per-Stream State Machine:** `IDLE → PREPARING → LIVE → INTERACTING → ENDING → CLEANUP`
- **Resource Pooling:** Each GPU node handles 2 streams max (to prevent thermal throttling). Orchestrator auto-scales GPU pods based on queue depth.

---

## 4. FAILOVER PROCEDURES (ZERO-DOWNTIME TARGET)

### 4.1 Failure Detection (Health Checks)
- **AI Host Health:** Heartbeat every 5s from the AHE container. If 3 consecutive missed heartbeats → **AI Host Restart**.
- **Render Node Health:** GPU utilization, temperature, and encoding latency monitored. If latency > 500ms or GPU temp > 85°C → **Node Replacement**.
- **Stream Integrity:** RTMP push status (bitrate, frame drops) checked every 10s via custom exporter. If bitrate drops below 80% of target for 15s → **Failover Trigger**.
- **Platform API Health