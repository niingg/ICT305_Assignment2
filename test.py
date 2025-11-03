import streamlit as st

# --- Page setup ---
st.set_page_config(page_title="Diabetes Risk Factors Dashboard", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Introduction", "H1", "H2", "H3", "H4", "H5", "Conclusion"])

# --- Header ---
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>Diabetes Risk Factors Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")  # a line separator

# --- Page content logic ---
if page == "Intro":
    st.subheader("Introduction")
    st.write("Welcome to the Diabetes Risk Factors Dashboard. Here you can explore various factors associated with diabetes risk.")
    
elif page == "H1":
    st.subheader("Hypothesis 1")
    st.write("Content for Hypothesis 1 will go here.")
    
elif page == "H2":
    st.subheader("Hypothesis 2")
    st.write("Content for Hypothesis 2 will go here.")
    
elif page == "H3":
    st.subheader("Hypothesis 3")
    st.write("Content for Hypothesis 3 will go here.")
    
elif page == "H4":
    st.subheader("Hypothesis 4")
    st.write("Content for Hypothesis 4 will go here.")
    
elif page == "H5":
    st.subheader("Hypothesis 5")
    st.write("Content for Hypothesis 5 will go here.")
    
elif page == "Conclusion":
    st.subheader("Conclusion")
    st.write("Summary of findings and insights will go here.")
