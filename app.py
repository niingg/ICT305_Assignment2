import streamlit as st

st.set_page_config(page_title="Diabetes Risk Factors Dashboard", layout="wide")

# =============================
# Custom Figma-style CSS
# =============================
st.markdown("""
<style>
.main {
    background-color: #ffffff;
}
.block-container {
    padding-top: 0rem;
    padding-bottom: 2rem;
}

.title-wrap {
    display: flex;
    flex-direction: column;
    gap: 0.1rem;
}
.title-wrap .title {
    color: #1E66FF;
    font-size: 1.7rem;
    font-weight: 700;
    margin: 0;
}
.title-wrap .subtitle {
    color: #6B7280;
    font-size: 0.95rem;
    margin: 0;
}
.page-count {
    color: #6B7280;
    font-weight: 500;
    font-size: 0.9rem;
}

/* Tabs */
div[data-baseweb="tab-list"] > button {
    border-radius: 9999px !important;
    background-color: #f4f5f7 !important;
    color: #374151 !important;
    font-weight: 600 !important;
    margin-right: 0.5rem !important;
    padding: 0.45rem 1rem !important;
    transition: all 0.25s ease;
}
div[data-baseweb="tab-list"] > button[data-selected="true"] {
    background-color: #1E66FF !important;
    color: #ffffff !important;
    box-shadow: 0px 3px 10px rgba(30,102,255,0.25);
}
</style>
""", unsafe_allow_html=True)

# =============================
# Header
# =============================

st.markdown("""
<div class="dashboard-header">
  <div class="title-wrap">
    <div class="title">Diabetes Risk Factors Dashboard</div>
  </div>
</div>
""", unsafe_allow_html=True)

# =============================
# Tabs
# =============================
tabs = st.tabs([
    "Introduction",
    "H1: Lifestyle Habits",
    "H2: Education",
    "H3: Healthcare Access"
])

# --- Introduction ---
with tabs[0]:
    st.header("Introduction :3")
    st.write("""
    This dashboard presents findings from the **CDC BRFSS 2015 dataset**, 
    analysing how lifestyle, education, and healthcare access influence diabetes risk.
    Navigate through each tab to explore the interactive results.
    """)

# --- Hypothesis 1 ---
with tabs[1]:
    st.markdown("### H1: Lifestyle Habits and Diabetes")
    try:
        st.components.v1.html(open("H1.html").read(), height=950, scrolling=True)
    except FileNotFoundError:
        st.warning("⚠️ 'H1.html' not found. Export your H1 notebook to HTML and place it in this folder.")

# --- Hypothesis 2 ---
with tabs[2]:
    st.markdown("### H2: Education and Diabetes")
    try:
        st.components.v1.html(open("H2.html").read(), height=950, scrolling=True)
    except FileNotFoundError:
        st.warning("⚠️ 'H2.html' not found. Export your H2 notebook to HTML and place it in this folder.")

# --- Hypothesis 3 ---
with tabs[3]:
    st.markdown("### H3: Healthcare Access and Diabetes")
    try:
        st.components.v1.html(open("H3.html").read(), height=950, scrolling=True)
    except FileNotFoundError:
        st.warning("⚠️ 'H3.html' not found. Export your H3 notebook to HTML and place it in this folder.")
