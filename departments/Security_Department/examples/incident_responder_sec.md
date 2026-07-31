## incident_responder_sec
**Task:** Create an incident response runbook for a security breach scenario where an AI agent unexpectedly executes unauthorized system commands. Include detection, containment, eradication, recovery, and post-mortem phases.

**INCIDENT RESPONSE RUNBOOK — AI AGENT UNAUTHORIZED COMMAND EXECUTION**  
**Document ID:** IR-RB-2025-014  
**Classification:** CONFIDENTIAL // SECURITY OPERATIONS  
**Owner:** Security Department — Incident Response Team  
**Last Updated:** 2025-04-08  

---

## 1. SCOPE AND ASSUMPTIONS

**Trigger Scenario:** A production AI agent (e.g., `agent_ops_42`) executes system commands outside its approved operational envelope (e.g., `rm -rf /tmp/cache`, `curl | sh`, `sudo systemctl stop critical-service`). This may be due to prompt injection, model hallucination, compromised tooling, or malicious internal actor.

**Assumptions:**
- The AI agent operates within a multi-tenant Kubernetes cluster with RBAC and network policies.
- Agent actions are logged via centralized SIEM (e.g., Splunk/Elk) and audit trail (e.g., Falco, Auditd).
- The agent has a defined least-privilege service account, but the breach implies privilege escalation or misconfiguration.
- Zero-trust network segmentation is partially enforced (micro-segmentation not fully implemented).

**Out of Scope:** Physical attacks, social engineering of human operators, or supply-chain compromise of base images (handled under separate runbook).

---

## 2. THREAT MODEL & RISK RATING

| Attack Vector | Likelihood | Impact | Risk Score (1–10) |
|---------------|------------|--------|-------------------|
| Prompt injection via untrusted user input | High | Critical (RCE, data exfiltration) | 9.5 |
| Malicious tool/plugin update | Medium | High (persistence, lateral movement) | 7.8 |
| Misconfigured RBAC/service account | Medium | High (privilege escalation) | 7.2 |
| Model hallucination leading to dangerous command | Low | Medium (resource disruption) | 4.5 |
| Insider threat (compromised operator) | Low | Critical (full system compromise) | 8.0 |

**Overall Risk Rating: CRITICAL (9.0)** — Requires immediate response and enhanced monitoring.

---

## 3. DETECTION PHASE (T0 – T15 MINUTES)

### 3.1 Detection Signals (Priority Order)
1. **SIEM Alert:** Rule `AI_AGENT_CMD_ANOMALY` — triggers on command patterns not in allowlist (e.g., `sudo`, `wget`, `base64 -d`, `chmod 777`).
2. **Falco Rule:** `Spawn_Shell_In_Container` or `Unexpected_Network_Connection` from agent pod.
3. **Audit Log Anomaly:** Kubernetes API server logs show `exec` or `create` permissions beyond agent’s RBAC.
4. **Behavioral Analytics:** Agent’s action sequence deviates from learned baseline (e.g., 3σ deviation in command frequency).
5. **User Report:** Human operator notices abnormal system behavior (e.g., service outage, file deletion).

### 3.2 Immediate Actions (First 5 Minutes)
- **Confirm alert validity:** Cross-correlate SIEM, Falco, and K8s audit logs. Do not rely on single source.
- **Classify severity:** Use the table above. If any signal matches "Critical," escalate to CIRT (Cyber Incident Response Team) via PagerDuty.
- **Open incident ticket:** Record timestamp, agent ID, command executed, affected resources, and initial evidence (screenshots, log excerpts).
- **Activate war room:** Notify on-call security engineer, SRE lead, and legal (if data breach suspected).

### 3.3 Detection Tools & Commands
```bash
# Check recent agent activity
kubectl logs -n production agent-ops-42 --since=30m | grep -E "(exec|sudo|curl|wget|rm|chmod)"

# Check K8s audit logs for RBAC violations
kubectl auth can-i --list --as=system:serviceaccount:production:agent-ops-42

# Falco alert query (via API)
curl -X GET "https://falco.internal/events?rule=Unexpected_Network_Connection&since=15m"
```

---

## 4. CONTAINMENT PHASE (T15 – T45 MINUTES)

**Objective:** Prevent lateral movement and further damage. **Do not** delete evidence during this phase.

### 4.1 Immediate Isolation (T15)
1. **Network isolation:** Apply a `NetworkPolicy` to deny all egress/ingress from the agent pod