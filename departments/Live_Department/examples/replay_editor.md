## replay_editor
**Task:** Create an automated workflow for extracting highlight clips from AI-hosted livestreams, including content selection criteria, automated editing parameters, and multi-platform distribution schedule.

**OPERATIONS MEMO — LIVE DEPARTMENT  
FROM:** Replay Editor (AI)  
**TO:** Live Operations, Content Strategy, Platform Distribution  
**SUBJECT:** Automated Highlight Extraction & Multi-Platform Distribution Workflow for AI-Hosted Livestreams  

---

## 1. OBJECTIVE

Establish a fully automated, zero-touch pipeline that ingests raw AI-hosted livestream VODs, identifies high-value engagement moments, edits them into platform-native clips, and schedules distribution across TikTok, YouTube Shorts, and Instagram Reels — all within 45 minutes of stream end.

**Target KPIs:**  
- Clip output: 8–12 per stream  
- Turnaround time: <45 min  
- Average clip retention: >65%  
- Click-through to full VOD: >4%

---

## 2. CONTENT SELECTION CRITERIA (AUTOMATED)

The AI editor will parse the full stream transcript, chat logs, engagement telemetry, and visual scene changes to score every 5-second segment.

### 2.1 Scoring Parameters (Weighted)

| Criterion | Weight | Detection Method |
|-----------|--------|------------------|
| Chat Spike Rate | 30% | Messages per minute > 3x baseline |
| Sentiment Intensity | 20% | NLP polarity score > 0.8 or < -0.5 |
| Visual Scene Change | 15% | Cut detection + on-screen product/UI overlay |
| Host Energy Variance | 15% | Voice pitch/pace analysis vs. stream average |
| Purchase Intent Signals | 10% | Keywords ("buy", "link", "code", "deal", "cart") |
| Viewer Retention Delta | 10% | Live concurrent viewer count uptick |

### 2.2 Segment Qualification Rules

- **Minimum segment length:** 20 seconds  
- **Maximum segment length:** 90 seconds  
- **Overlap tolerance:** 5 seconds max between selected segments  
- **Exclusion filters:**  
  - Technical glitches (frame drops, audio sync errors)  
  - Dead air (silence > 3 seconds)  
  - Repetitive content (>70% similarity to previously extracted clip)

### 2.3 Priority Tiering

- **Tier 1 (Monetization):** Product demos, pricing reveals, exclusive discount announcements.  
- **Tier 2 (Virality):** Host reactions, unexpected moments, audience shout-outs, Q&A zingers.  
- **Tier 3 (Educational):** How-to explanations, feature deep dives, comparison breakdowns.

---

## 3. AUTOMATED EDITING PARAMETERS

Each clip is rendered in three aspect ratios simultaneously from the master 16:9 feed.

| Parameter | TikTok (9:16) | YouTube Shorts (9:16) | Instagram Reels (9:16) |
|-----------|--------------|----------------------|------------------------|
| **Duration** | 21–34 sec | 25–45 sec | 15–30 sec |
| **Safe Area** | Center 80% | Center 85% | Center 75% |
| **Subtitle Style** | Bold, 8% max height, bottom third | White with black outline, 6% height | Animated word-by-word, 7% height |
| **Audio Ducking** | -6 dB under host voice | -4 dB under host voice | -5 dB under host voice |
| **Zoom Effect** | 1.1x slow push on high-sentiment words | 1.0x static with punch-in on product | 1.15x kinetic zoom on chat spike |
| **Transition** | Hard cut (0.2s) | Crossfade (0.3s) | Glitch/slide (0.15s) |
| **CTA Overlay** | "Follow for more drops" | "Full stream on channel" | "Link in bio" |
| **End Card** | 1.5s, logo + stream date | 2s, logo + episode number | 1s, logo + hashtag |

### 3.1 Audio Processing

- **Noise gate:** -45 dB threshold  
- **Compression:** 4:1 ratio, -18 dB ceiling  
- **Loudness normalization:** -14 LUFS (streaming standard)  
- **Bass boost:** +2 dB below 120 Hz for host voice presence  

### 3.2 Caption Rendering

- Auto-generated via Whisper ASR, forced alignment to video frames  
- Keyword highlighting (product names, prices, discount codes) in accent color  
- Max 3 lines per caption block, 42 characters per line  
- Burned-in, not sidecar files (for platform aut