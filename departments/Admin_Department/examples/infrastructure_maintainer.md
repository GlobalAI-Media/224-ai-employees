## infrastructure_maintainer
**Task:** Outline a preventive maintenance schedule for the server infrastructure supporting 224 AI employees, including backup verification, disk health checks, and load balancer tuning.

**Subject:** Preventive Maintenance Schedule – AI Employee Server Infrastructure (224 Nodes)

**To:** COO, Facility Management  
**From:** Infrastructure Maintainer, Admin Department  
**Priority:** High – Operational Continuity

---

## 1. Scope & Objective

This schedule ensures 99.99% uptime for the 224 AI employee runtime environment. Maintenance covers:
- Backup integrity verification
- Disk health & SMART monitoring
- Load balancer tuning & traffic distribution

**Target SLA:** < 30 minutes cumulative downtime per quarter per subsystem.

---

## 2. Preventive Maintenance Schedule

### 2.1 Daily (Automated – 02:00 UTC, duration 10 min)

| Task | Tool / Script | Threshold | Action on Failure |
|------|---------------|-----------|-------------------|
| Backup completion check | `backup_status.sh` | All 224 VM snapshots created within last 24h | Page on-call admin, re-trigger backup job |
| Disk I/O latency | `iostat -x 1 5` | avg await > 10 ms on any disk | Flag for weekly deep check |
| Load balancer health probe | `curl -f http://lb:8080/health` | 100% nodes responding 200 OK | Remove unhealthy node, notify Ops |

### 2.2 Weekly (Every Sunday – 03:00 UTC, duration 45 min)

| Task | Procedure | Verification | Resource |
|------|-----------|--------------|----------|
| Full backup restore test | Restore 1 random AI employee VM to isolated network | Boot, run 5 core tasks, compare output checksums | 1 spare compute node |
| Disk SMART long test | `smartctl -t long /dev/sdX` on all 224 storage drives | No reallocated sectors > 10, pending sectors = 0 | 2 hours per drive (run in batches of 16) |
| Load balancer log review | Parse LB access logs for 5xx errors, latency outliers | < 0.1% 5xx, p99 latency < 200 ms | Adjust backend weights if imbalance > 15% |

### 2.3 Monthly (First Saturday – 01:00 UTC, duration 2.5 hours)

| Task | Steps | Check | Fallback |
|------|-------|-------|----------|
| Off-site backup rotation | Copy last 4 weekly backups to cold storage | Checksum verification, 3-2-1 rule compliance | Re-run copy if any checksum mismatch |
| Disk health report | Run `smartctl -H` on all drives, generate trend report | Any drive with SMART attribute decline > 5% in 30 days | Schedule replacement within 7 days |
| Load balancer tuning | Rebalance traffic based on monthly usage patterns | Each node CPU < 70%, memory < 80% | Adjust weights, add temporary node if needed |

### 2.4 Quarterly (First Sunday of quarter – 00:00 UTC, duration 4 hours)

| Task | Procedure | Success Criteria | Rollback Plan |
|------|-----------|------------------|---------------|
| Full disaster recovery drill | Simulate total loss of primary data center | Restore 224 AI employees to secondary site in < 2 hours | Keep primary active until drill validated |
| Disk replacement cycle | Replace any drive with > 5 reallocated sectors or > 3 years age | 100% drives under warranty, SMART healthy | Hot spare auto-join RAID |
| Load balancer software update | Patch LB firmware to latest stable | All nodes pass health check within 5 minutes | Rollback to previous version if > 2% failure |

---

## 3. Resource Requirements

| Item | Quantity | Notes |
|------|----------|-------|
| Hot spare compute nodes | 4 | Pre-configured, idle |
| Hot spare storage drives | 8 | Same model as production |
| Backup storage capacity | 50 TB | For 4 weekly + 1 monthly full backup |
| On-call admin coverage | 2 per shift | 24/7 for critical alerts |

---

## 4. Escalation & Reporting

- **Daily/Weekly:** Automated report to Admin Dashboard
- **Monthly:** Summary to COO with trend analysis
- **Quarterly:** Full audit report with drill outcomes

**Critical failures (e.g., backup failure, disk failure > 2 drives):** Immediate escalation to COO via SMS + Slack.

---

## 5. Maintenance Windows & Communication

- All scheduled maintenance: **00:00–05:00 UTC** to minimize AI employee task disruption
- 48-hour advance notice to all department heads
- Status page updated 15 minutes before start

---

**Prepared by:** Infrastructure Maintainer  
**Approval required