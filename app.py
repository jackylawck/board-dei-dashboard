import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 頁面全域設定 (Page Configuration)
st.set_page_config(page_title="Board DEI & Talent Governance", layout="wide")

# 2. 雙語本地化字典 (Bilingual Localization Dictionary)
LANG = {
    "EN": {
        "title": "Board-level Executive Workforce Analytics",
        "sidebar_title": "Governance Control Panel",
        "upload_header": "Data Source Management",
        "upload_label": "Upload Executive Data (CSV)",
        "welcome": "👋 Welcome to the Board DEI & Governance Analytics System",
        "instruction": "To generate the analytics report, please upload your corporate HR data using the sidebar on the left. This system processes data in-memory to comply with Data Minimization and Privacy-by-Design principles.",
        "template_desc": "Ensure your dataset aligns with our AIGP-compliant schema. Download the standard template below.",
        "download_btn": "📥 Download Compliant CSV Template",
        "status_user": "🔒 Securely operating on uploaded corporate data. (Data processed in-memory only, zero cloud retention)",
        "metrics_title": "Key Talent Governance Metrics",
        "total_execs": "Total Executive Headcount",
        "turnover": "Global Turnover Rate",
        "gender_ratio": "Executive Gender Diversity",
        "pay_equity_title": "Pay Equity Analysis (Base Salary Distribution)",
        "dept": "Department",
        "salary": "Annual Base Salary (USD)",
        "gender": "Gender",
        "err_cols": "❌ Compliance Error: The uploaded CSV is missing required governance fields. Please check the template."
    },
    "ZH": {
        "title": "董事會級別勞動力與 DEI 治理分析",
        "sidebar_title": "治理儀表板控制系統",
        "upload_header": "數據源安全管理",
        "upload_label": "上傳高管層勞動力數據 (CSV)",
        "welcome": "👋 歡迎使用董事會 DEI 與人才風險治理系統",
        "instruction": "請於左側「控制面板」上傳您企業的 CSV 數據。本系統採用「記憶體內運算」架構，嚴格遵循數據最小化 (Data Minimization) 與隱私設計 (Privacy-by-Design) 原則。",
        "template_desc": "為確保薪酬公平性與演算法偏差審查之有效性，請確保您的數據符合 AIGP 標準架構。您可下載下方範本進行對照。",
        "download_btn": "📥 下載合規標準 CSV 數據範本",
        "status_user": "🔒 已安全載入企業內部數據。（數據僅於加密記憶體內運算，關閉即銷毀，符合高階資安合規）",
        "metrics_title": "關鍵人才治理指標 (Key Governance Metrics)",
        "total_execs": "高管總人數",
        "turnover": "跨國團隊流失率",
        "gender_ratio": "高管層性別比例",
        "pay_equity_title": "薪酬公平性審查 (底薪分佈小提琴圖)",
        "dept": "部門",
        "salary": "年度底薪 (美元)",
        "gender": "性別",
        "err_cols": "❌ 合規格式錯誤：上傳的 CSV 缺少必要的治理審查欄位，請下載標準範本確認欄位名稱與數量。"
    }
}

# 3. 側邊欄控制面板 (Sidebar Controls)
st.sidebar.title("⚙️ Control Panel")
selected_lang = st.sidebar.radio("Language / 語言", ["EN", "ZH"])
t = LANG[selected_lang]

st.sidebar.markdown("---")
st.sidebar.subheader(t["upload_header"])
uploaded_file = st.sidebar.file_uploader(label=t["upload_label"], type=["csv"])

# 4. 生成可供下載的合規 CSV 範本 (AIGP & HR Compliant Schema)
@st.cache_data
def get_template_csv():
    template_df = pd.DataFrame({
        "Emp_Hash": ["USR-A1B2", "USR-C3D4", "USR-E5F6", "USR-G7H8", "USR-I9J0", "USR-K1L2", "USR-M3N4", "USR-O5P6"],
        "Jurisdiction": ["Hong Kong", "Singapore", "London", "Hong Kong", "Tokyo", "London", "Singapore", "Hong Kong"],
        "Department": ["HR", "Finance", "Engineering", "Sales", "Marketing", "Engineering", "Sales", "HR"],
        "Job_Level": ["Director", "VP", "VP", "Director", "VP", "C-Level", "Director", "Director"],
        "Gender": ["Female", "Male", "Female", "Male", "Female", "Male", "Female", "Male"],
        "Age_Group": ["40-49", "50-59", "30-39", "40-49", "30-39", "50-59", "40-49", "30-39"],
        "Tenure_Years": [5, 12, 2, 8, 3, 15, 6, 1],
        "Performance_Rating": [4, 3, 5, 4, 3, 5, 4, 3],
        "Base_Salary": [130000, 145000, 155000, 110000, 125000, 150000, 115000, 128000],
        "Status": ["Active", "Resigned", "Active", "Active", "Resigned", "Active", "Active", "Active"]
    })
    return template_df.to_csv(index=False).encode('utf-8')

# 5. 主畫面邏輯 (Main Dashboard Logic)
st.title(f"📊 {t['title']}")

# 驗證必填欄位清單 (10 Mandatory Fields)
REQUIRED_COLS = {
    "Emp_Hash", "Jurisdiction", "Department", "Job_Level", "Gender", 
    "Age_Group", "Tenure_Years", "Performance_Rating", "Base_Salary", "Status"
}

# 狀態 A：如果沒有上傳檔案，顯示「歡迎頁面與下載範本」
if uploaded_file is None:
    st.info(t["welcome"])
    st.write(t["instruction"])
    st.markdown("---")
    st.write(t["template_desc"])
    
    st.download_button(
        label=t["download_btn"],
        data=get_template_csv(),
        file_name="AIGP_DEI_Data_Template.csv",
        mime="text/csv"
    )
    
    st.markdown("### Data Schema Preview / 治理數據架構預覽")
    preview_df = pd.DataFrame({
        "Emp_Hash": ["USR-A1B2", "USR-C3D4"],
        "Jurisdiction": ["Hong Kong", "Singapore"],
        "Department": ["HR", "Finance"],
        "Job_Level": ["Director", "VP"],
        "Gender": ["Female", "Male"],
        "Age_Group": ["40-49", "50-59"],
        "Tenure_Years": [5, 12],
        "Performance_Rating": [4, 3],
        "Base_Salary": [130000, 145000],
        "Status": ["Active", "Resigned"]
    })
    st.table(preview_df)

# 狀態 B：如果已經上傳檔案，進行驗證與圖表渲染
else:
    try:
        df = pd.read_csv(uploaded_file)
        
        # 嚴格驗證合規欄位是否齊全
        if not REQUIRED_COLS.issubset(df.columns):
            st.error(t["err_cols"])
            st.write(f"**Required columns:** {', '.join(REQUIRED_COLS)}")
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

            # 繪製薪酬公平性圖表 (使用新的 Base_Salary 欄位)
            st.subheader(t["pay_equity_title"])
            fig, ax = plt.subplots(figsize=(11, 5))
            
            sns.violinplot(
                data=df, 
                x="Department", 
                y="Base_Salary",  # 對應新的合規欄位
                hue="Gender", 
                split=True, 
                inner="quart", 
                palette={"Male": "#4C72B0", "Female": "#C44E52"}, 
                ax=ax
            )
            
            ax.set_xlabel(t["dept"], fontsize=12)
            ax.set_ylabel(t["salary"], fontsize=12)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            plt.legend(title="Gender")
            
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Error reading file: {e}")
