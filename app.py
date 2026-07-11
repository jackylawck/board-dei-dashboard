import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Board DEI Dashboard", layout="wide")

# 2. Bilingual Dictionary
LANG = {
    "EN": {
        "title": "Board-level Executive Workforce Analytics Report",
        "sidebar_title": "Settings",
        "lang_sel": "Language / 語言",
        "metrics_title": "Key Talent Metrics",
        "total_execs": "Total Executives",
        "turnover": "Global Turnover Rate",
        "gender_ratio": "Executive Gender Ratio",
        "pay_equity_title": "Pay Equity Analysis (Violin Plot)",
        "dept": "Department",
        "salary": "Annual Base Salary (USD)",
        "gender": "Gender"
    },
    "ZH": {
        "title": "董事會級別勞動力與 DEI 分析報告",
        "sidebar_title": "儀表板設定",
        "lang_sel": "Language / 語言",
        "metrics_title": "關鍵人才指標 (Key Metrics)",
        "total_execs": "高管總人數",
        "turnover": "跨國團隊流失率",
        "gender_ratio": "高管層性別比例",
        "pay_equity_title": "薪酬公平性分析 (小提琴圖)",
        "dept": "部門",
        "salary": "年度底薪 (美元)",
        "gender": "性別"
    }
}

# 3. Sidebar Language Selector
st.sidebar.title(f"⚙️ {LANG['EN']['sidebar_title']} / 儀表板設定")
selected_lang = st.sidebar.radio("Language / 語言", ["EN", "ZH"])
t = LANG[selected_lang]

# 4. Mock Data Generation
@st.cache_data
def load_data():
    np.random.seed(42)
    n = 200
    depts = ["Engineering", "Sales", "Finance", "HR", "Marketing"]
    data = {
        "Employee_ID": range(1, n+1),
        "Department": np.random.choice(depts, n),
        "Gender": np.random.choice(["Male", "Female"], n, p=[0.6, 0.4]),
        "Salary": np.random.normal(120000, 30000, n),
        "Status": np.random.choice(["Active", "Resigned"], n, p=[0.85, 0.15])
    }
    df = pd.DataFrame(data)
    # Simulate a slight structural pay gap for visualization purposes
    df.loc[df['Gender'] == 'Female', 'Salary'] *= 0.95 
    return df

df = load_data()

# 5. Dashboard Main Body
st.title(f"📊 {t['title']}")
st.markdown("---")

# Calculate KPIs
total_execs = len(df)
turnover_rate = (len(df[df["Status"] == "Resigned"]) / total_execs) * 100
female_ratio = (len(df[df["Gender"] == "Female"]) / total_execs) * 100

# Display KPI Cards
st.subheader(t["metrics_title"])
col1, col2, col3 = st.columns(3)
col1.metric(label=t["total_execs"], value=total_execs)
col2.metric(label=t["turnover"], value=f"{turnover_rate:.1f}%")
col3.metric(label=t["gender_ratio"], value=f"{female_ratio:.1f}% (Female)")

st.markdown("---")

# 6. Pay Equity Violin Plot (Fail-Safe Version)
st.subheader(t["pay_equity_title"])

fig, ax = plt.subplots(figsize=(10, 5))
sns.violinplot(
    data=df, 
    x="Department", 
    y="Salary", 
    hue="Gender", 
    split=True, 
    inner="quart",
    palette={"Male": "#4C72B0", "Female": "#C44E52"},
    ax=ax
)

# Apply UI translations safely to labels without breaking fonts inside the canvas
ax.set_xlabel(t["dept"], fontsize=12)
ax.set_ylabel(t["salary"], fontsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.legend(title="Gender")

# Render to Streamlit
st.pyplot(fig)
