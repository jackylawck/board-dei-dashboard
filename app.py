import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1. 頁面設定 (Page Configuration)
st.set_page_config(page_title="Board DEI Dashboard", layout="wide")

# 2. 雙語字典 (Bilingual Dictionary)
LANG = {
    "EN": {
        "title": "Board-level Executive Workforce Analytics Report",
        "sidebar_title": "Settings",
        "lang_sel": "Language / 語言",
        "metrics_title": "Key Talent Metrics",
        "turnover": "Global Turnover Rate",
        "gender_ratio": "Executive Gender Ratio",
        "pay_equity_title": "Pay Equity Analysis (Violin Plot)",
        "dept": "Department",
        "salary": "Annual Base Salary (USD)",
        "gender": "Gender",
        "male": "Male",
        "female": "Female"
    },
    "ZH": {
        "title": "董事會級別勞動力與 DEI 分析報告",
        "sidebar_title": "儀表板設定",
        "lang_sel": "Language / 語言",
        "metrics_title": "關鍵人才指標 (Key Metrics)",
        "turnover": "跨國團隊流失率",
        "gender_ratio": "高管層性別比例",
        "pay_equity_title": "薪酬公平性分析 (小提琴圖)",
        "dept": "部門",
        "salary": "年度底薪 (美元)",
        "gender": "性別",
        "male": "男性",
        "female": "女性"
    }
}

# 3. 側邊欄設定語言 (Sidebar Language Selector)
st.sidebar.title("⚙️ Settings / 設定")
selected_lang = st.sidebar.radio("Language / 語言", ["EN", "ZH"])
t = LANG[selected_lang] # t 就是目前的翻譯字典

# 4. 生成模擬數據 (Mock Data Generation)
# 在實際應用中，您可以將這裡替換為：df = pd.read_csv("your_latest_data.csv")
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
        "Status": np.random.choice(["Active", "Resigned"], n, p=[0.85, 0.15]) # 模擬流失率
    }
    df = pd.DataFrame(data)
    # 針對女性薪水做微調模擬，以便在圖表上看出差異（僅為示範）
    df.loc[df['Gender'] == 'Female', 'Salary'] *= 0.95 
    return df

df = load_data()

# 如果選擇中文，將 DataFrame 內的性別值替換為中文，以便圖表顯示
if selected_lang == "ZH":
    df_display = df.copy()
    df_display["Gender"] = df_display["Gender"].map({"Male": t["male"], "Female": t["female"]})
else:
    df_display = df.copy()

# 5. 儀表板主體 (Dashboard Main Body)
st.title(f"📊 {t['title']}")
st.markdown("---")

# 計算關鍵指標 (Calculate KPIs)
total_execs = len(df)
turnover_rate = (len(df[df["Status"] == "Resigned"]) / total_execs) * 100
female_ratio = (len(df[df["Gender"] == "Female"]) / total_execs) * 100

# 顯示 KPI 卡片 (KPI Metrics)
st.subheader(t["metrics_title"])
col1, col2, col3 = st.columns(3)
col1.metric(label="Total Executives", value=total_execs)
col2.metric(label=t["turnover"], value=f"{turnover_rate:.1f}%")
col3.metric(label=t["gender_ratio"], value=f"{female_ratio:.1f}% (Female)")

st.markdown("---")

# 6. 繪製高質量圖表：薪酬公平性小提琴圖 (Pay Equity Violin Plot)
st.subheader(t["pay_equity_title"])

# 使用 Seaborn 繪製
fig, ax = plt.subplots(figsize=(10, 5))
sns.violinplot(
    data=df_display, 
    x="Department", 
    y="Salary", 
    hue="Gender", 
    split=True, # 將男女合併在同一個小提琴圖兩側，非常適合比較分布
    inner="quart",
    palette={"Male": "#4C72B0", "Female": "#C44E52", t["male"]: "#4C72B0", t["female"]: "#C44E52"},
    ax=ax
)

# 圖表美化
ax.set_xlabel(t["dept"], fontsize=12)
ax.set_ylabel(t["salary"], fontsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.legend(title=t["gender"])

# 將 Matplotlib 圖表渲染到 Streamlit
st.pyplot(fig)

# (備註：要生成 PDF，您可以指示董事會成員使用瀏覽器的 Ctrl+P / Cmd+P，或者使用額外的庫如 pdfkit)
