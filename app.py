import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1. 頁面全域設定 (Page Configuration)
st.set_page_config(page_title="Board DEI & Talent Analytics", layout="wide")

# 2. 雙語本地化字典 (Bilingual Localization Dictionary)
LANG = {
    "EN": {
        "title": "Board-level Executive Workforce Analytics Report",
        "sidebar_title": "Dashboard Control",
        "lang_sel": "Language / 語言",
        "upload_header": "Data Source Management",
        "upload_label": "Upload Executive Data (CSV format)",
        "upload_help": "Expected columns: Department, Gender, Salary, Status",
        "status_mock": "⚠️ Currently showing generated MOCK DATA. Upload your corporate CSV in the sidebar for live analytics.",
        "status_user": "🔒 Securely operating on uploaded corporate data. (Data processed in-memory, no cloud retention)",
        "metrics_title": "Key Talent Governance Metrics",
        "total_execs": "Total Executive Headcount",
        "turnover": "Global Turnover Rate",
        "gender_ratio": "Executive Gender Diversity",
        "pay_equity_title": "Pay Equity Analysis (Compensation Distribution)",
        "dept": "Department",
        "salary": "Annual Base Salary (USD)",
        "gender": "Gender",
        "err_cols": "❌ Format Error: The uploaded CSV must contain 'Department', 'Gender', 'Salary', and 'Status' columns."
    },
    "ZH": {
        "title": "董事會級別勞動力與 DEI 數據分析報告",
        "sidebar_title": "儀表板控制系統",
        "lang_sel": "Language / 語言",
        "upload_header": "數據源安全管理",
        "upload_label": "上傳高管層勞動力數據 (僅限 CSV 格式)",
        "upload_help": "必要欄位名稱：Department, Gender, Salary, Status",
        "status_mock": "⚠️ 目前顯示系統模擬數據。請於左側側邊欄上傳企業 CSV 檔案以進行即時數據驅動分析。",
        "status_user": "🔒 已安全載入企業內部數據。（數據僅於記憶體內運算，網頁關閉後即徹底銷毀，符合資安合規）",
        "metrics_title": "關鍵人才治理指標 (Key Metrics)",
        "total_execs": "高管總人數",
        "turnover": "跨國團隊流失率",
        "gender_ratio": "高管層性別比例",
        "pay_equity_title": "薪酬公平性審查 (薪酬分佈小提琴圖)",
        "dept": "部門",
        "salary": "年度底薪 (美元)",
        "gender": "性別",
        "err_cols": "❌ 檔案格式錯誤：上傳的 CSV 必須包含 'Department', 'Gender', 'Salary' 與 'Status' 欄位。"
    }
}

# 3. 側邊欄控制面板 (Sidebar Controls)
st.sidebar.title("⚙️ Control Panel")

# 語言切換
selected_lang = st.sidebar.radio("Language / 語言", ["EN", "ZH"])
t = LANG[selected_lang]

st.sidebar.markdown("---")

# 檔案上傳器
st.sidebar.subheader(t["upload_header"])
uploaded_file = st.sidebar.file_uploader(
    label=t["upload_label"], 
    type=["csv"], 
    help=t["upload_help"]
)

# 4. 數據載入邏輯與安全機制 (Data Loading & Fallback Mechanism)
@st.cache_data
def generate_mock_data():
    """生成合規展示用的模擬數據"""
    np.random.seed(42)
    n = 200
    depts = ["Engineering", "Sales", "Finance", "HR", "Marketing"]
    data = {
        "Employee_ID": range(1, n+1),
        "Department": np.random.choice(depts, n),
        "Gender": np.random.choice(["Male", "Female"], n, p=[0.6, 0.4]),
        "Salary": np.random.normal(120000, 25000, n),
        "Status": np.random.choice(["Active", "Resigned"], n, p=[0.88, 0.12])
    }
    df = pd.DataFrame(data)
    # 模擬結構性薪酬差距，以便小提琴圖展示出對比效果
    df.loc[df['Gender'] == 'Female', 'Salary'] *= 0.94 
    return df

# 決定使用上傳數據還是模擬數據
data_source_status = "mock"
if uploaded_file is not None:
    try:
        user_df = pd.read_csv(uploaded_file)
        # 驗證必要欄位是否存在
        required_cols = {"Department", "Gender", "Salary", "Status"}
        if required_cols.issubset(user_df.columns):
            df = user_df
            data_source_status = "user"
        else:
            st.error(t["err_cols"])
            df = generate_mock_data()
    except Exception as e:
        st.error(f"Error reading file: {e}")
        df = generate_mock_data()
else:
    df = generate_mock_data()

# 5. 儀表板主體架構 (Main Dashboard Layout)
st.title(f"📊 {t['title']}")

# 根據數據來源顯示對應的資安與治理提示
if data_source_status == "mock":
    st.info(t["status_mock"])
else:
    st.success(t["status_user"])

st.markdown("---")

# 6. 核心指標運算 (KPI Computation)
total_execs = len(df)
# 計算流失率：(已離職人數 / 總人數) * 100
turnover_rate = (len(df[df["Status"].str.lower() == "resigned"]) / total_execs) * 100 if total_execs > 0 else 0
# 計算女性高管比例
female_count = len(df[df["Gender"].str.lower() == "female"])
female_ratio = (female_count / total_execs) * 100 if total_execs > 0 else 0

# 顯示 KPI 卡片
st.subheader(t["metrics_title"])
col1, col2, col3 = st.columns(3)
col1.metric(label=t["total_execs"], value=f"{total_execs} Pax")
col2.metric(label=t["turnover"], value=f"{turnover_rate:.1f}%")
col3.metric(label=t["gender_ratio"], value=f"{female_ratio:.1f}% (Female)")

st.markdown("---")

# 7. 薪酬公平性審查圖表 (Pay Equity Violin Plot)
st.subheader(t["pay_equity_title"])

# 圖表內部標籤與圖例固定使用標準英文，確保在缺乏中文字型的雲端 Linux 伺服器上 100% 穩定不崩潰
fig, ax = plt.subplots(figsize=(11, 5))
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

# 畫布邊框外層（X/Y軸名稱）則安全調用雙語字典
ax.set_xlabel(t["dept"], fontsize=12)
ax.set_ylabel(t["salary"], fontsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.legend(title="Gender")

# 將圖表渲染至 Streamlit 網頁
st.pyplot(fig)
