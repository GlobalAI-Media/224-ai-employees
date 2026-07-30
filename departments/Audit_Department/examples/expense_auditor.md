## expense_auditor
**Task:** Develop an automated expense verification system for AI compute costs, API usage fees, and infrastructure spending. Include variance analysis thresholds and escalation criteria.

**AUDIT MEMORANDUM – CONFIDENTIAL**

**To:** Audit Committee, Global AI Media Group  
**From:** Expense Auditor, Internal Audit Department  
**Subject:** Automated Expense Verification System – AI Compute, API, and Infrastructure Costs  
**Date:** [Current Date]  
**Reference:** IIA Standard 2320 – Nature of Work; COSO Internal Control – Monitoring Activities  

---

### 1. Audit Objectives

- **Objective 1:** Ensure all AI compute costs, API usage fees, and infrastructure spending are accurately recorded, authorized, and allocated to the correct cost centers.
- **Objective 2:** Detect anomalous or unauthorized expenditures exceeding predefined materiality thresholds.
- **Objective 3:** Provide real-time or near-real-time variance analysis with automated escalation to management and internal audit.
- **Objective 4:** Align with COSO’s Control Environment and Monitoring components, and IIA’s Performance Standards for continuous auditing.

### 2. Methodology

The system will be designed as a **continuous auditing module** embedded within the Group’s ERP and cloud billing platforms. The approach includes:

- **Data Ingestion:** Automated extraction from AWS, Azure, GCP, OpenAI, Anthropic, and internal infrastructure logs via API connectors.
- **Normalization:** Mapping vendor-specific line items (e.g., GPU hours, token counts, storage GB) to a unified chart of accounts.
- **Variance Analysis Engine:** Statistical and rule-based comparison against:
  - Historical rolling 12-month averages (seasonally adjusted)
  - Budgeted amounts per cost center
  - Peer benchmarks (industry median cost per token/compute hour)
- **Sampling Approach:** For high-risk categories (e.g., GPU clusters, LLM API calls), 100% transaction review. For low-risk categories (e.g., static storage), stratified random sampling with a 95% confidence level and 5% tolerable error rate.
- **Control Framework:** COSO’s five components: Control Environment (policy enforcement), Risk Assessment (thresholds), Control Activities (automated approvals), Information & Communication (dashboards), Monitoring (continuous alerts).

### 3. Variance Analysis Thresholds and Escalation Criteria

| **Expense Category** | **Variance Threshold** | **Escalation Criteria** | **Risk Rating** |
|----------------------|------------------------|--------------------------|-----------------|
| **AI Compute (GPU/TPU)** | >10% deviation from 12-month rolling average OR >5% from budget | Immediate alert to Cost Center Manager; if >15% deviation, escalate to VP Engineering and Internal Audit | High |
| **API Usage Fees (LLM, embedding, fine-tuning)** | >20% increase in daily token count vs. 7-day moving average OR >$5,000/day unforecasted | Alert to AI Operations Lead; if >30% or >$15,000/day, escalate to CTO and Audit Committee | High |
| **Infrastructure (storage, networking, CDN)** | >15% deviation from budget OR >$10,000 monthly overspend | Alert to Infrastructure Manager; if >25% or >$50,000, escalate to CFO | Medium |
| **Miscellaneous (support, licensing)** | >$2,000 monthly variance without pre-approval | Alert to Procurement; if >$10,000, escalate to VP Finance | Low |

**Note:** All thresholds are dynamic and will be recalibrated quarterly based on rolling data and risk appetite approved by the Audit Committee.

### 4. Findings Format (Example)

Each automated alert will generate a structured finding:

- **Finding ID:** AUD-EXP-2025-001
- **Category:** AI Compute
- **Description:** GPU cluster “A100-3” incurred $45,000 in unforecasted costs during the week of [Date], representing a 22% variance from the 12-month average.
- **Root Cause:** Unauthorized batch job launched by AI Employee ID 112 (model training script) without prior cost approval.
- **Control Deficiency:** Lack of pre-run cost estimation check for ad-hoc training jobs.
- **Risk Rating:** High
- **Recommendation:** Implement mandatory cost estimation and approval workflow for all training jobs exceeding $10,000.
- **Responsible Party:** AI Operations Lead
- **Due Date:** [Date + 14 days]

### 5. Recommendations

1. **Implement Automated Pre-Approval Workflow:** For all AI compute and API calls exceeding $5,000 per execution, require digital approval from the Cost Center Manager via the ERP system. This aligns with COSO’s Control Activities.
2. **Deploy Real-Time Dashboards:** Provide cost center managers with live views of current vs. budgeted spend, with color-coded alerts (green/yellow/red)