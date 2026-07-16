# Threat Modeling & Risk Mitigation Matrix

Applying the **STRIDE** methodology and **ISO 42001 Risk Assessment** framework, this project evaluates potential threats to corporate workforce analytics.

| Threat Category | Specific Risk Scenario | Impact | Mitigation Implemented | Risk Level (Residual) |
| :--- | :--- | :--- | :--- | :--- |
| **Information Disclosure** | Unauthorized actors intercepting executive base salary data during transmission. | High | Enforced End-to-End Encryption via HTTPS/TLS 1.3 during deployment. | **Low** |
| **Repudiation** | Inability to audit who accessed or modified the deployment pipeline. | Medium | Integrated **GitHub Actions (Pylint Quality Audit)** to provide an unalterable immutable audit trail of all code changes. | **Low** |
| **Denial of Service** | Malformed or excessively large CSV uploads crashing the executive rendering instance. | Medium | Implemented a robust `try-except` parsing architecture with file-type restrictions (`.csv` only) in `app.py`. | **Low** |
| **Identity Linkage** | Re-identification of unique salaries in small departments (Inference Attack). | High | *Limitation Layer:* Added structural warning in user guidelines recommending a minimum group size of N>=5 for statistical rendering. | **Medium** |
