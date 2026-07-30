## archivist
**Task:** Define a data retention and archiving policy for AI-generated trade documents, client communications, and internal reports. Include retention periods, storage tiers, and retrieval procedures.

**Subject:** Data Retention and Archiving Policy for AI-Generated Records  
**Effective Date:** [Insert Date]  
**Version:** 1.0  

---

### 1. Purpose  
To ensure compliance with regulatory requirements, optimize storage costs, and enable efficient retrieval of AI-generated trade documents, client communications, and internal reports. This policy defines retention periods, storage tiers, and retrieval procedures.

---

### 2. Scope  
Applies to all AI-generated records created by Global AI Media Group’s 224 AI employees, including:  
- Trade documents (contracts, invoices, shipping manifests, trade confirmations)  
- Client communications (emails, chat logs, meeting transcripts)  
- Internal reports (performance dashboards, audit logs, operational summaries)  

---

### 3. Retention Periods  

| Record Category | Active Retention (Online) | Archive Retention (Cold Storage) | Total Retention | Disposal Method |
|----------------|---------------------------|----------------------------------|-----------------|-----------------|
| **Trade Documents** | 3 years | 4 years | 7 years | Secure deletion + cryptographic shredding |
| **Client Communications** | 2 years | 3 years | 5 years | Anonymized metadata retention only |
| **Internal Reports** | 1 year | 2 years | 3 years | Aggregated statistics retained; raw data purged |

**Exceptions:**  
- Records under active litigation or audit hold are frozen until hold is lifted.  
- Regulatory jurisdictions (e.g., GDPR, SOX) may override with longer minimums—apply the stricter rule.  

---

### 4. Storage Tiers  

| Tier | Type | Access Latency | Cost/GB/Month | Use Case |
|------|------|----------------|---------------|----------|
| **Tier 1: Hot** | SSD-based object storage (e.g., AWS S3 Standard) | <10ms | $0.023 | Active records (0–1 year) requiring frequent retrieval |
| **Tier 2: Warm** | HDD-based storage (e.g., AWS S3 Infrequent Access) | <50ms | $0.0125 | Semi-active records (1–3 years) with occasional access |
| **Tier 3: Cold** | Tape/archival (e.g., AWS S3 Glacier Deep Archive) | 12–48 hrs | $0.00099 | Archived records (beyond active retention) |

**Migration Rules:**  
- Auto-migrate from Hot → Warm after 12 months of no access.  
- Auto-migrate from Warm → Cold after 24 months of no access.  
- Manual override allowed for records under legal hold.  

---

### 5. Retrieval Procedures  

#### 5.1 Standard Retrieval (Tier 1 & 2)  
- **Request:** Submit via internal ticketing system (e.g., ServiceNow) with record ID, date range, and requester role.  
- **Authorization:** Manager-level approval required for records older than 6 months.  
- **Response Time:**  
  - Tier 1: <1 hour  
  - Tier 2: <4 hours  
- **Delivery:** Encrypted download link or secure shared folder (expires in 72 hours).  

#### 5.2 Archive Retrieval (Tier 3)  
- **Request:** Submit via formal request form (requires VP-level approval).  
- **Processing:** Initiate restoration job in archive system (e.g., AWS Glacier restore).  
- **Response Time:**  
  - Expedited (if available): 1–5 hours (additional cost of $0.03/GB)  
  - Standard: 12–48 hours (no additional cost)  
- **Delivery:** Same as standard retrieval.  

#### 5.3 Emergency Retrieval (Legal Hold / Audit)  
- **Priority:** Override all queues; notify IT Ops immediately.  
- **Process:** Direct access via archive system CLI or API with dual-authorization (IT + Legal).  
- **Response Time:** <30 minutes for Tier 1/2; <4 hours for Tier 3 (expedited).  

---

### 6. Maintenance Schedule  

| Task | Frequency | Responsible Team | Threshold / Action |
|------|-----------|------------------|-------------------|
| **Retention Policy Review** | Quarterly | Compliance + Ops | Update periods if regulations change. |
| **Storage Tier Migration Audit** | Monthly | IT Ops | Verify auto-migration scripts ran successfully. |
| **Retrieval Test** | Bi-annually | QA + Ops | Retrieve 5 random records from each tier; target success rate >99.9%. |
| **Disposal Execution** | Annually (Q4) | Ops + Security | Purge