## streaming_engineer
**Task:** Outline the infrastructure requirements for 24/7 AI-driven livestream operations, including encoding pipeline, CDN configuration, latency optimization, and automated stream health monitoring.

**MEMORANDUM**  
**TO:** Global AI Media Group – Executive Production Board  
**FROM:** Lead Streaming Engineer, Live Department  
**SUBJECT:** Infrastructure Blueprint for 24/7 AI-Driven Livestream Operations  

---

## 1. EXECUTIVE SUMMARY

We are building a **self-healing, multi-region broadcast fabric** capable of sustaining 24/7/365 AI-hosted streams with sub‑2 second glass‑to‑glass latency, 99.99% uptime, and zero manual intervention for routine failures. This document outlines the hard infrastructure, encoding pipeline, CDN strategy, latency tuning, and automated health monitoring required to support our AI talent roster across TikTok, YouTube, and Instagram simultaneously.

---

## 2. ENCODING PIPELINE – THE DIGITAL NERVOUS SYSTEM

### 2.1 Source Acquisition
- **AI Render Engines:** GPU clusters (NVIDIA L4/A10 or equivalent) generating 4K/60fps virtual scenes, real‑time avatars, and dynamic overlays.
- **Ingest Format:** NDI|HX3 or uncompressed SDI over 10GbE to the encoding farm.
- **Redundancy:** Dual ingest paths (active/passive) with automatic failover in <500ms.

### 2.2 Encoding Ladder (Per Stream)
We encode **five adaptive bitrate (ABR) rungs** per platform to maximize reach across devices:

| Rung | Resolution | Frame Rate | Video Bitrate | Audio Bitrate | Codec |
|------|------------|------------|---------------|---------------|-------|
| 1    | 1920x1080  | 60fps      | 6.0 Mbps      | 192 kbps      | H.264 High |
| 2    | 1280x720   | 60fps      | 4.0 Mbps      | 192 kbps      | H.264 High |
| 3    | 1280x720   | 30fps      | 2.5 Mbps      | 128 kbps      | H.264 Main |
| 4    | 854x480    | 30fps      | 1.2 Mbps      | 96 kbps       | H.264 Main |
| 5    | 640x360    | 30fps      | 0.6 Mbps      | 64 kbps       | H.264 Baseline |

- **Hardware Encoders:** Dedicated ASIC/FPGA cards (e.g., NETINT T408) to offload CPU/GPU for AI rendering.
- **Software Fallback:** x264 `veryfast` preset on standby servers for disaster recovery.

### 2.3 Audio Pipeline
- **AI Voice Overlay:** 48kHz/24‑bit PCM → AAC‑LC 192kbps stereo.
- **Dynamic Mixing:** Ducking, sidechain compression, and loudness normalization (EBU R128 / -14 LUFS for YouTube, -14 LUFS for TikTok, -16 LUFS for IG).

---

## 3. CDN CONFIGURATION – GLOBAL REACH, LOCAL DELIVERY

### 3.1 Multi‑CDN Strategy
We deploy **three concurrent CDNs** (primary, secondary, tertiary) with automatic traffic steering:

- **Primary:** Cloudflare Stream (low‑latency HLS + LL‑HLS, 300+ PoPs)
- **Secondary:** AWS CloudFront (for redundancy and S3 origin integration)
- **Tertiary:** Fastly (for real‑time log streaming and edge compute)

### 3.2 Origin & Edge Configuration
- **Origin:** Dedicated 10GbE‑connected origin clusters in US‑East, EU‑West, AP‑South.
- **Edge Rules:** Cache TTL = 2 seconds for segments; 0 TTL for manifests.
- **Protocol:** HTTPS with TLS 1.3; HTTP/3 (QUIC) enabled for all endpoints.
- **Geo‑Routing:** Latency‑based routing to nearest origin; failover in under 10 seconds.

### 3.3 Segment & Manifest Settings
- **Segment Duration:** 2 seconds (HLS) / 1 second (LL‑HLS) for sub‑2s latency.
- **Manifest Refresh:** Every 1 second; preload hints enabled.
- **GOP Alignment:** Keyframe interval = 2 seconds (aligned across all rungs) to enable seamless bitrate switching.

---

## 4. LATENCY OPTIMIZATION – THE RACE TO ZERO

### 4.1 Target Latency Budget
- **Glass‑to‑Glass:** 1.8 seconds (TikTok LIVE & YouTube