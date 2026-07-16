# System Architecture & Privacy-by-Design Documentation

This document outlines the architectural safeguards implemented in the Board-level DEI Dashboard to ensure absolute data protection and regulatory compliance (e.g., HK PCPD Guidance, GDPR).

## Data Flow & In-Memory Processing
To mitigate the risk of cross-border data transfer limitations and unauthorized cloud data retention, the system utilizes a **Zero-Storage Architecture**:

1. **Ingest:** The user uploads an encrypted or hashed corporate CSV file via the secure Streamlit HTTPS interface.
2. **Process:** Data is read directly into volatile memory (RAM) as a Pandas DataFrame.
3. **Render:** Seaborn and Matplotlib generate aggregate statistical visualizations (Violin Plots).
4. **Purge:** No data is committed to persistent storage, local disks, or third-party databases. Once the browser session is closed, the memory buffer is completely flushed.

## Data Minimization Principles
The data schema strictly enforces a pseudonymous identifier framework:
* **No Direct PII:** The system completely rejects names, national ID numbers, or exact dates of birth.
* **Emp_Hash Requirement:** Organizations must pre-hash employee identities (e.g., SHA-256 tokens like `USR-A1B2`) before ingestion, ensuring that even in the event of memory introspection, no real-world individual can be re-identified.
