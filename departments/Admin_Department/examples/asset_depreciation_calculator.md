## asset_depreciation_calculator
**Task:** Create an asset lifecycle management plan for GPU clusters, storage arrays, and networking equipment used to run AI workloads. Include depreciation schedules, replacement triggers, and capex forecasting.

**Subject:** Asset Lifecycle Management Plan – GPU Clusters, Storage Arrays, and Networking Equipment  
**Date:** [Current Date]  
**Prepared by:** Admin Operations – Global AI Media Group  

---

## 1. Scope and Asset Classification

This plan covers three asset categories supporting 224 AI employees and their workloads:

| Asset Class | Typical Units | Estimated Useful Life (EUL) | Depreciation Method |
|-------------|---------------|----------------------------|---------------------|
| GPU Clusters (NVIDIA A100/H100, AMD MI250) | 4–8 racks per cluster | 3–4 years | Straight-line, 3-year |
| Storage Arrays (NVMe all-flash, HDD cold tier) | 2–4 PB usable | 4–5 years | Straight-line, 5-year |
| Networking Equipment (100/200/400 GbE switches, InfiniBand HDR) | 10–20 top-of-rack + 2–4 spine | 5–6 years | Straight-line, 5-year |

**Depreciation Schedule Basis:**  
- **GPU Clusters:** 36-month straight-line, 0% residual value (technology obsolescence).  
- **Storage Arrays:** 60-month straight-line, 10% residual value (HDD/NVMe salvage).  
- **Networking Equipment:** 60-month straight-line, 5% residual value (cables, optics salvageable).

---

## 2. Depreciation Schedules (Sample per $1M Investment)

### 2.1 GPU Cluster ($1M initial cost)
| Year | Annual Depreciation | Accumulated Depreciation | Book Value |
|------|---------------------|--------------------------|------------|
| 1    | $333,333            | $333,333                 | $666,667   |
| 2    | $333,333            | $666,667                 | $333,333   |
| 3    | $333,333            | $1,000,000               | $0         |

### 2.2 Storage Array ($1M initial cost)
| Year | Annual Depreciation | Accumulated Depreciation | Book Value |
|------|---------------------|--------------------------|------------|
| 1    | $180,000            | $180,000                 | $820,000   |
| 2    | $180,000            | $360,000                 | $640,000   |
| 3    | $180,000            | $540,000                 | $460,000   |
| 4    | $180,000            | $720,000                 | $280,000   |
| 5    | $180,000            | $900,000                 | $100,000   |

### 2.3 Networking Equipment ($1M initial cost)
| Year | Annual Depreciation | Accumulated Depreciation | Book Value |
|------|---------------------|--------------------------|------------|
| 1    | $190,000            | $190,000                 | $810,000   |
| 2    | $190,000            | $380,000                 | $620,000   |
| 3    | $190,000            | $570,000                 | $430,000   |
| 4    | $190,000            | $760,000                 | $240,000   |
| 5    | $190,000            | $950,000                 | $50,000    |

---

## 3. Replacement Triggers

Replacements are initiated when **any one** of the following conditions is met:

### 3.1 GPU Clusters
- **Performance Degradation:** Average inference latency exceeds 15 ms for 7 consecutive days (baseline: 5 ms).  
- **Utilization Threshold:** Sustained GPU utilization below 40% for 90 days (indicates workload mismatch).  
- **Failure Rate:** >5% of GPUs in a cluster fail per quarter (MTBF < 6 months).  
- **EOL/EOS:** Vendor end-of-life notification with <12 months of support remaining.  
- **Cost Efficiency:** New GPU generation delivers >2x performance per watt at same capex (trigger for early replacement).

### 3.2 Storage Arrays
- **Capacity Utilization:** >85% of usable capacity for 30 consecutive days (trigger for expansion or replacement).  
- **Latency Spike:** Average read latency >2 ms for NVMe tier or >20 ms for HDD tier for 14 days.  
- **Failure Rate:** >3 drive failures per 100 drives per quarter.  
- **Warranty Expiry:** <6 months remaining on manufacturer warranty.  
- **Technology Leap:** New storage technology (e.g., PCI