# 📊 Board-level DEI & Workforce Analytics Dashboard

## 📖 Project Overview (專案概述)
This automated Python/Streamlit web application is designed to replace manual Excel reporting. It transforms raw HR data into secure, interactive, and board-ready visualizations. The dashboard focuses on key workforce metrics, including Diversity, Equity, and Inclusion (DEI), pay equity, and retention risks, providing a data-driven foundation for executive decision-making.

這是一個專為取代傳統 Excel 手工報表而設計的自動化 Python/Streamlit 網頁應用程式。將原始人力資源數據轉化為安全、互動式且適合董事會審閱的高質量圖表，聚焦於多元包容（DEI）、薪酬公平性與人才流失風險。

## ✨ Key Features (核心功能)
* **Bilingual Interface (雙語介面):** Seamlessly switch between English and Traditional Chinese (繁體中文) to accommodate diverse board members.
* **Executive KPIs (高階關鍵指標):** Real-time tracking of Global Turnover Rate and Executive Gender Ratio.
* **Pay Equity Analysis (薪酬公平性分析):** Utilizing Seaborn violin plots to visualize salary distributions across departments and genders, proactively identifying potential pay gaps.
* **Automated Reporting (一鍵自動化):** Eliminates repetitive Excel formatting; updates instantly when the underlying data source is refreshed.

## 🛡️ Governance & Risk Management (治理與風險管理視角)
As an HR and Governance tool, this project is built with corporate compliance in mind:
* **Data Minimization (數據最小化原則):** Designed to aggregate executive metrics to prevent the re-identification of highly sensitive Personally Identifiable Information (PII).
* **Bias Detection (偏差審查):** Provides a transparent statistical view of compensation distribution, helping organizations align with ESG standards and mitigate algorithmic or systemic biases.

## 🛠️ Tech Stack (技術棧)
* **Framework:** Streamlit
* **Data Processing:** Pandas, NumPy
* **Data Visualization:** Matplotlib, Seaborn

## 🚀 How to Run Locally (本地執行方式)

1. Clone this repository:
   ```bash
   git clone [https://github.com/jackylawck/board-dei-dashboard.git](https://github.com/jackylawck/board-dei-dashboard.git)
