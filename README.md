# 📊 Board-level DEI & Talent Governance Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dei-dashboard.streamlit.app)

**👉 [Click here to view the Live Dashboard / 點擊此處體驗互動式儀表板](https://dei-dashboard.streamlit.app)**

---

## 📖 Project Overview (專案概述)
This automated Python/Streamlit web application is designed to replace manual Excel reporting. It transforms raw HR data into secure, interactive, and board-ready visualizations. The dashboard focuses on key workforce metrics, including Diversity, Equity, and Inclusion (DEI), pay equity, and retention risks, providing a data-driven foundation for executive decision-making.

這是一個專為取代傳統 Excel 手工報表而設計的自動化 Python/Streamlit 網頁應用程式。將原始人力資源數據轉化為安全、互動式且適合董事會審閱的高質量圖表，聚焦於多元包容（DEI）、薪酬公平性與人才流失風險。

## ✨ Key Features (核心功能)
* **Bilingual Interface (雙語介面):** Seamlessly switch between English and Traditional Chinese (繁體中文) to accommodate diverse board members.
* **Executive KPIs (高階關鍵指標):** Real-time tracking of Global Turnover Rate and Executive Gender Diversity.
* **Pay Equity Analysis (薪酬公平性分析):** Utilizing Seaborn violin plots to visualize base salary distributions across departments and genders, proactively identifying potential pay gaps.
* **In-Memory Data Processing (記憶體內運算):** Allows users to upload corporate CSV data that is processed entirely in-memory with zero cloud retention.

## 🛡️ Governance & Risk Management (治理與風險管理視角)
Built with AI Governance Professional (AIGP) and corporate compliance standards in mind:
* **Data Minimization (數據最小化原則):** The required data schema (Emp_Hash, Jurisdiction, Job_Level, etc.) is strictly defined to prevent the re-identification of highly sensitive Personally Identifiable Information (PII).
* **Bias Auditing (偏差審查):** Provides a transparent statistical view of compensation distribution and performance ratings, helping organizations align with ESG standards and mitigate algorithmic or systemic biases.

## 🛠️ Tech Stack (技術棧)
* **Framework:** Streamlit
* **Data Processing:** Pandas, NumPy
* **Data Visualization:** Matplotlib, Seaborn

## 🚀 How to Run Locally (本地執行方式)

1. Clone this repository:
   ```bash
   git clone [https://github.com/jackylawck/board-dei-dashboard.git](https://github.com/jackylawck/board-dei-dashboard.git)
