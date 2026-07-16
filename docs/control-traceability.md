# Control Traceability Matrix (合規控制點追蹤矩陣)

This dashboard bridges the gap between software development and international AI governance standards. The table below maps specific architectural components in `app.py` to **ISO/IEC 42001:2023** and the **IAPP AIGP Body of Knowledge**.

| Standard / Framework Reference | Control Objective | Technical Implementation in Dashboard | Evidence / Location |
| :--- | :--- | :--- | :--- |
| **ISO/IEC 42001 Annex A.6.2** | Data Management for AI Systems (資料治理) | Enforced mandatory 10-field template schema rejecting direct Personally Identifiable Information (PII). | `app.py` -> `REQUIRED_COLS` validation block |
| **ISO/IEC 42001 Annex A.5.3** | AI System Impact Assessment (偏見審查) | Automated execution of Pay Equity analysis across departments using dual-hue Seaborn distribution tracking. | `app.py` -> `pay_equity_title` and `sns.violinplot` |
| **IAPP AIGP Domain IV** | Governing AI Deployment & Use (可持續監測) | Integrated continuous compliance signals via an automated Github Actions pipeline executing standard code health checks. | `.github/workflows/pylint.yml` |
| **HK PCPD AI Guidance** | Data Minimization & Security | In-memory data structures ensuring corporate compensation data never persists on public cloud nodes. | `docs/architecture.md` (Zero-Storage Policy) |
