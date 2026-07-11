import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 頁面全域設定 (Page Configuration)
st.set_page_config(page_title="Board DEI & Talent Analytics", layout="wide")

# 2. 雙語本地化字典 (Bilingual Localization Dictionary)
LANG = {
    "EN": {
        "title": "Board-level Executive Workforce Analytics",
        "sidebar_title": "Dashboard Control",
        "upload_header": "Data Source Management",
        "upload_label": "Upload Executive Data (CSV)",
        "welcome": "👋 Welcome to the Board DEI Analytics System",
        "instruction": "To generate the analytics report, please upload your corporate HR data using the sidebar on the left.",
        "template_desc": "Don't have a file ready? Download our standard template, fill in your data, and upload it to see the dashboard in action.",
        "download_btn": "📥 Download Standard CSV Template",
        "status_user": "🔒 Securely operating on uploaded corporate data. (Data processed in-memory only)",
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
        "title": "董事會級別勞動力與 DEI 數據分析",
        "sidebar_title": "儀表板控制系統",
        "upload_header": "數據源安全管理",
        "upload_label": "上傳高管層勞動力數據 (CSV)",
        "welcome": "👋 歡迎使用董事會 DEI 數據儀表板",
        "instruction": "請於左側「控制面板」上傳您企業的 CSV 數據檔案，系統將自動生成互動式分析報告。",
        "template_desc": "不知道檔案格式怎麼填？請點擊下方按鈕下載標準 CSV 範本，填入您的數據後再重新上傳即可。",
        "download_btn": "📥 下載標準 CSV 數據範本",
        "status_user": "🔒 已安全載入企業內部數據。（數據僅於記憶體內運算，符合資安合規）",
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
selected_lang = st.sidebar.radio("Language / 語言", ["EN", "ZH"])
t = LANG[selected_lang]

st.sidebar.markdown("---")
st.sidebar.subheader(t["upload_header"])
uploaded_file = st.sidebar.file_uploader(label=t["upload_label"], type=["csv"])

# 4. 生成可供下載的 CSV 範本 (Generate downloadable template in-memory)
@st.cache_data
def get_template_csv():
    # 這就是別人下載後會看到的 Excel/CSV 範本內容
    template_df = pd.DataFrame({
        "Department": ["HR", "Finance", "Engineering", "Sales", "Marketing", "Engineering", "Sales", "HR"],
        "Gender": ["Female", "Male", "Female", "Male", "Female", "Male", "Female", "Male"],
        "Salary": [130000, 145000, 155000, 110000, 125000, 150000, 115000, 128000],
        "Status": ["Active", "Resigned", "Active", "Active", "Resigned", "Active", "Active", "Active"]
    })
    return template_df.to_csv(index=False).encode('utf-8')

# 5. 主畫面邏輯 (Main Dashboard Logic)
st.title(f"📊 {t['title']}")

# 如果沒有上傳檔案，顯示「歡迎頁面與下載範本」
if uploaded_file is None:
    st.info(t["welcome"])
    st.write(t["instruction"])
    st.markdown("---")
    st.write(t["template_desc"])
    
    # 放置下載按鈕
    st.download_button(
        label=t["download_btn"],
        data=get_template_csv(),
        file_name="DEI_Data_Template.csv",
        mime="text/csv"
    )
    
    # 顯示預覽表格讓使用者直觀了解格式
    st.markdown("### Data Format Preview / 數據格式預覽")
    preview_df = pd.DataFrame({
        "Department": ["HR", "Finance", "..."],
        "Gender": ["Female", "Male", "..."],
        "Salary": [130000, 145000, "..."],
        "Status": ["Active", "Resigned", "..."]
    })
    st.table(preview_df)

# 如果已經上傳檔案，顯示「儀表板圖表」
else:
    try:
        df = pd.read_csv(uploaded_file)
        required_cols = {"Department", "Gender", "Salary", "Status"}
        
        if not required_cols.issubset(df.columns):
            st.error(t["err_cols"])
        else:
            st.success(t["status_user"])
            st.markdown("---")
            
            # KPI 運算
            total_execs = len(df)
            turnover_rate = (len(df[df["Status"].str.lower() == "resigned"]) / total_execs) * 100 if total_execs > 0 else 0
            female_count = len(df[df["Gender"].str.lower() == "female"])
            female_ratio = (female_count / total_execs) * 100 if total_execs > 0 else 0

            # 顯示 KPI 卡片
            st.subheader(t["metrics_title"])
            col1, col2, col3 = st.columns(3)
            col1.metric(label=t["total_execs"], value=f"{total_execs} Pax")
            col2.metric(label=t["turnover"], value=f"{turnover_rate:.1f}%")
            col3.metric(label=t["gender_ratio"], value=f"{female_ratio:.1f}% (Female)")

            st.markdown("---")

            # 繪製圖表
            st.subheader(t["pay_equity_title"])
            fig, ax = plt.subplots(figsize=(11, 5))
            sns.violinplot(
                data=df, x="Department", y="Salary", hue="Gender", 
                split=True, inner="quart", 
                palette={"Male": "#4C72B0", "Female": "#C44E52"}, ax=ax
            )
            ax.set_xlabel(t["dept"], fontsize=12)
            ax.set_ylabel(t["salary"], fontsize=12)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            plt.legend(title="Gender")
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Error reading file: {e}")
