## procurement_specialist
**Task:** Create a vendor evaluation framework for procuring cloud compute resources, API services, and software licenses needed to run a 224-AI-employee platform. Include cost optimization strategies.

**MEMORANDUM**

**TO:** COO, Global AI Media Group  
**FROM:** Procurement Specialist, Admin Department  
**SUBJECT:** Vendor Evaluation Framework for AI Employee Platform Infrastructure  
**DATE:** [Current Date]

---

### 1. Scope & Objectives

This framework governs procurement of three critical resource categories for our 224-AI-employee operating system:

- **Cloud Compute Resources** (GPU/TPU instances, virtual machines, storage)
- **API Services** (LLM inference, embeddings, vector databases, monitoring)
- **Software Licenses** (OS, middleware, security tools, proprietary AI frameworks)

**Primary Objectives:**
- Ensure 99.95% uptime for production workloads
- Achieve ≤15% year-over-year cost growth despite 20–30% workload expansion
- Maintain vendor diversity (no single provider >40% of any category)

---

### 2. Vendor Evaluation Criteria (Weighted Scoring Model)

Each vendor is scored on a 0–100 scale per category. Minimum passing score: **75/100**.

| Criterion | Weight | Cloud Compute | API Services | Software Licenses |
|-----------|--------|---------------|--------------|-------------------|
| **Reliability & Uptime SLA** | 25% | ≥99.95% uptime guarantee; documented incident response <15 min | ≥99.9% uptime; rate limit burst capacity ≥5x baseline | Vendor patch cadence ≤30 days; critical CVE fix ≤72 hours |
| **Cost Efficiency** | 25% | Reserved instance discounts ≥30% vs on-demand; spot instance availability ≥90% | Per-token pricing ≤$0.002/1K tokens (GPT-4 class); volume tier discounts at 10M+ tokens/month | Per-seat licensing ≤$50/user/month; enterprise agreement caps annual increase at 5% |
| **Scalability & Performance** | 20% | Auto-scaling to 2x peak load within 60 seconds; GPU memory ≥80 GB per instance | Latency P99 ≤500ms for inference; throughput ≥1,000 requests/second per endpoint | Concurrent user licensing; no hard cap on agent count |
| **Security & Compliance** | 15% | SOC 2 Type II, ISO 27001, GDPR/CCPA compliance; encryption at rest & transit | Data residency options (US, EU, APAC); no training on customer data | Role-based access control; audit logs retained ≥1 year |
| **Support & SLAs** | 10% | 24/7/365 support with <1 hour response for critical issues | Dedicated account manager for >$10K/month spend | Technical support included; escalation to engineering within 4 hours |
| **Vendor Stability** | 5% | Revenue >$1B; operating >5 years; no major security incidents in 24 months | Same as compute | Same as compute |

---

### 3. Procurement Process & Timeline

**Phase 1: RFI & Shortlisting (Week 1–2)**
- Issue RFI to ≥5 vendors per category
- Mandatory requirements:
  - Cloud: AWS, Azure, GCP, or equivalent Tier 1 provider
  - API: OpenAI, Anthropic, Cohere, or equivalent with ≥1M daily requests
  - Software: Commercial off-the-shelf with active maintenance
- Shortlist top 3 per category based on RFI scores

**Phase 2: Technical Proof of Concept (Week 3–4)**
- Run benchmark workloads:
  - Compute: 50 concurrent AI agents processing 10K requests each
  - API: 1M inference requests over 24 hours
  - Software: Integration test with existing CI/CD pipeline
- Measure: latency, throughput, cost per request, error rates

**Phase 3: Commercial Negotiation (Week 5)**
- Target pricing:
  - Cloud: 3-year reserved instance with 40% discount; spot instance pool ≥50% of capacity
  - API: Volume tier at $0.0015/1K tokens for 50M+ monthly tokens
  - Software: 3-year enterprise agreement with 15% discount and 5% annual cap
- Require 30-day termination without penalty

**Phase 4: Contract & Onboarding (Week 6)**
- Legal review: liability cap ≥3x monthly spend; data processing agreement
- Technical onboarding: API keys, IAM roles, monitoring integration
- Go-live checklist (see Section 5)

---

### 4. Cost Optimization Strategies

| Strategy | Implementation | Expected Savings | Risk |
|----------|----------------|------------------|------|
| **Reserved/Committed Use** | Purchase 1- or 3-year reserved instances for baseline load (