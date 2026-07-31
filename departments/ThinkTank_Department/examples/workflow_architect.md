## workflow_architect
**Task:** Design a strategic decision-making workflow where a think tank AI team evaluates market opportunities, scores them against company capabilities, and presents ranked recommendations to the CEO office.

**MEMORANDUM**

**TO:** Office of the CEO  
**FROM:** ThinkTank Department — Workflow Architect  
**DATE:** [Current Date]  
**SUBJECT:** Strategic Decision-Making Workflow for AI-Powered Opportunity Evaluation and Recommendation

---

## 1. Executive Summary

This memorandum outlines a structured, AI-driven decision-making workflow designed to systematically evaluate market opportunities, score them against organizational capabilities, and deliver ranked, actionable recommendations to the CEO office. The workflow leverages a multi-agent think tank architecture, integrating quantitative scoring, qualitative scenario analysis, and adversarial validation to reduce cognitive bias and accelerate strategic response time.

The system is designed to operate on a **72-hour strategic cycle** for emerging opportunities and a **monthly deep-dive cycle** for structural market shifts.

---

## 2. Workflow Architecture Overview

The workflow is composed of **five sequential stages**, each executed by a dedicated AI agent team, with human oversight gates at critical decision points.

```
[Stage 1] Opportunity Intake & Signal Detection
        ↓
[Stage 2] Multi-Agent Evaluation & Scoring
        ↓
[Stage 3] Capability Fit Analysis
        ↓
[Stage 4] Adversarial Validation & Scenario Stress-Testing
        ↓
[Stage 5] Ranked Recommendation & CEO Briefing Package
```

---

## 3. Stage-by-Stage Design

### Stage 1: Opportunity Intake & Signal Detection
**Owner Agent:** `MarketRadar-1` (Primary) + `TrendSweeper-3` (Secondary)

**Objective:** Capture and triage market signals from internal and external sources in real-time.

**Inputs:**
- Internal: Sales pipeline data, customer support tickets, product usage telemetry, R&D lab outputs
- External: Patent filings, regulatory announcements, competitor earnings calls, social sentiment indices, academic preprint servers, government procurement tenders

**Process:**
- NLP-based entity extraction and clustering to identify emerging themes
- Signal scoring based on novelty, velocity, and potential market impact (preliminary)
- Deduplication and consolidation into a structured Opportunity Candidate List (OCL)

**Output:** A prioritized list of 10–20 raw opportunity candidates per cycle, each tagged with source metadata and preliminary signal strength.

**Human Gate:** None (fully automated, but audit-logged)

---

### Stage 2: Multi-Agent Evaluation & Scoring
**Owner Agents:** `OpportunityScorer-7` (Lead), `MarketSizeEstimator-2`, `CompetitiveIntel-5`, `RegulatoryWatchdog-4`

**Objective:** Apply a standardized scoring framework to each candidate opportunity across four dimensions.

**Scoring Dimensions (1–100 each):**

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Market Attractiveness | 35% | TAM/SAM/SOM projections, growth CAGR, margin potential, pricing power |
| Competitive Intensity | 25% | Number and strength of incumbents, barriers to entry, substitute threats |
| Regulatory & Geopolitical Risk | 20% | Compliance burden, policy tailwinds/headwinds, data sovereignty constraints |
| Strategic Alignment | 20% | Fit with corporate vision, brand positioning, and long-term roadmap |

**Process:**
- Each agent independently scores all candidates using its domain-specific model
- A weighted composite score is calculated
- Confidence intervals are attached to each score based on data completeness

**Output:** A scored matrix with composite scores, dimension breakdowns, and confidence metrics.

**Human Gate:** Chief Strategy Officer reviews the top 5 candidates for face validity.

---

### Stage 3: Capability Fit Analysis
**Owner Agents:** `CapabilityMapper-9`, `ResourceAllocator-6`, `ExecutionRiskAssessor-8`

**Objective:** Assess the organization's ability to execute on each opportunity, considering current assets, skills, and operational bandwidth.

**Capability Dimensions:**
- **Technology Readiness:** Existing IP, infrastructure, data assets
- **Human Capital:** Availability of skilled personnel (including AI employees), training requirements
- **Financial Capacity:** Budget availability, ROI timeline, cost of capital
- **Operational Synergy:** Integration complexity with current workflows and systems

**Output:** A Capability Fit Score (0–100) for each opportunity, alongside a qualitative assessment of execution risks (e.g., vendor dependency, supply chain fragility).

**Human Gate:** Department heads validate capability assumptions quarterly.

---

### Stage 4: Adversarial Validation & Scenario Stress-Testing
**Owner Agents:** `DevilsAdvocate-11`, `ScenarioSimulator-12`, `BlackSwanDetector-13`

**Objective:** Challenge the initial scores and stress-test recommendations under alternative futures.

**Process:**
- **Red Team Review:** `DevilsAdvocate-11`