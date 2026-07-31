## compliance_auditor_sec
**Task:** Create a security compliance checklist aligned with SOC 2 Type II and ISO 27001 requirements for an AI workforce platform serving enterprise clients. Include evidence collection and audit preparation guidelines.

**SECURITY COMPLIANCE CHECKLIST: SOC 2 TYPE II & ISO 27001 FOR AI WORKFORCE PLATFORM**

**Classification:** Internal – Restricted  
**Audience:** CISO, Security Engineering, Compliance Team, AI Operations  
**Scope:** Global AI Media Group – AI Workforce Platform (multi-tenant, 224 AI employees, 18 departments)

---

## 1. THREAT MODEL & RISK CONTEXT

Before checklist execution, acknowledge the unique attack surface of an AI-managed workforce:

| Threat Vector | Risk Rating | Description |
|---|---|---|
| Prompt Injection / Indirect Manipulation | **Critical** | Malicious instructions embedded in enterprise client data or external feeds hijacking AI employee decision paths. |
| Model/Data Poisoning | **High** | Contamination of training or RAG (Retrieval-Augmented Generation) datasets, altering AI behavior for lateral movement or data exfiltration. |
| Tenant Isolation Failure | **Critical** | Cross-tenant data leakage via shared vector databases, model caches, or orchestration layers. |
| AI-to-AI Lateral Movement | **High** | Compromised AI employee exploiting inter-departmental API trust to access financial, HR, or client PII. |
| Supply Chain (Model/Plugin) | **High** | Third-party model weights, plugins, or MCP (Model Context Protocol) servers with backdoors. |
| Audit Log Evasion | **Medium** | AI agents autonomously deleting or modifying their own logs to cover malicious actions. |

**Zero-Trust Assumption:** Treat every AI employee as a potential insider threat with elevated privileges. No implicit trust based on department or role.

---

## 2. COMPLIANCE CHECKLIST (SOC 2 TYPE II + ISO 27001 MAPPED)

### 2.1 CONTROL ENVIRONMENT & RISK ASSESSMENT (ISO 27001: Clauses 4-6; SOC 2: CC1, CC3)

| # | Control Requirement | Evidence Required | Verification Method |
|---|---|---|---|
| 1.1 | Documented AI governance policy defining human oversight, AI employee authority boundaries, and kill-switch procedures. | Signed policy, org chart, board minutes. | Policy review; interview with AI Operations Director. |
| 1.2 | Formal risk assessment covering AI-specific threats (prompt injection, data poisoning, model drift) updated quarterly. | Risk register with threat models, likelihood/impact scores. | Audit sampling of risk register; validate against MITRE ATLAS framework. |
| 1.3 | Business continuity plan including manual fallback procedures for critical AI employee functions (e.g., payroll, client billing). | DR/BCP runbook, tested within last 6 months. | Review test results and restore time metrics. |

### 2.2 ACCESS CONTROL & IDENTITY (SOC 2: CC6; ISO 27001: A.9)

| # | Control Requirement | Evidence Required | Verification Method |
|---|---|---|---|
| 2.1 | Zero-trust architecture: Every AI employee has a unique service principal with least-privilege IAM roles. | IAM policy definitions, role assignments. | Automated scan of IAM roles vs. actual API calls (e.g., AWS Access Analyzer). |
| 2.2 | MFA enforced for all human administrators; AI employees use short-lived, rotated credentials (max 15 min TTL). | MFA enforcement logs, credential rotation scripts. | Review IdP logs; test credential expiry. |
| 2.3 | Tenant isolation: Logical and cryptographic separation of client data across vector DBs, model caches, and object storage. | Encryption key hierarchy (per-tenant keys), network segmentation diagrams. | Penetration test attempting cross-tenant data access. |
| 2.4 | Privileged Access Management (PAM) for AI employees with access to production secrets or client PII. | PAM session recordings, approval workflows. | Random session review; validate approval chain. |

### 2.3 DATA PROTECTION & PRIVACY (SOC 2: CC6, P1-P4; ISO 27001: A.8, A.18)

| # | Control Requirement | Evidence Required | Verification Method |
|---|---|---|---|
| 3.1 | Data classification schema applied to all AI training, inference, and log data (Public, Internal, Confidential, Restricted). | Data flow diagrams, classification labels in metadata. | Sample data assets; verify labels match content. |
| 3.2 | Encryption at rest (AES-256) and in transit (TLS 1.3) for all client data, model weights, and audit logs. | Encryption configuration, key management policy (HSM-backed). | Technical review of KMS policies; TLS cipher suite check. |
|