import streamlit as st
import pandas as pd

# dataset
df = pd.read_csv('diabetes.csv')

# --- Page setup ---
st.set_page_config(page_title="Diabetes Risk Factors Dashboard", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Introduction", "**H1**: Lifestyle Habits and diabetes", "**H2**: Education and diabetes prevention", "**H3**: Healthcare access and diabetes", "**H4**: Self-rated health and diabetes", "**H5**: Pre-existing health conditions and diabetes", "Conclusion"])

# --- Header ---
st.markdown("<h1 style='text-align: center;'>Diabetes Risk Factors Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")  # a line separator

# --- Page content logic ---
if page == "Introduction":
    st.subheader("Introduction")
    st.write("Welcome to the Diabetes Risk Factors Dashboard. Here you can explore various factors associated with diabetes risk.")
    st.write("SALWA AND REGINA TO TWEAK THIS SECTION")

    st.subheader("Case Introduction")
    st.write("""
    Diabetes is a chronic medical condition that occurs when the body cannot properly regulate blood sugar (glucose) levels. 
    If left unmanaged, it can lead to serious health complications such as heart disease, kidney failure, and nerve damage. 

    Understanding the **risk factors** associated with diabetes is crucial for early detection and prevention. 
    This dashboard explores key health indicators and their relationship with the likelihood of developing diabetes.
    """)

    st.markdown("---")

    st.subheader("Dataset Overview")
    st.write("""
    The dataset used in this analysis is derived from the **Pima Indians Diabetes Database**, 
    which contains medical diagnostic measurements of women aged 21 and above. 
    It includes various features such as glucose concentration, BMI, blood pressure, insulin levels, and age.  

    The dataset will be used to explore five hypotheses regarding potential diabetes risk factors.
    """)

    # Display a sample of the dataset
    st.write("Here’s a glimpse of the data:")
    st.dataframe(df.head())

    # Display some basic stats
    st.write("**Basic Dataset Information:**")
    st.write(f"- Number of records: {df.shape[0]}")
    st.write(f"- Number of features: {df.shape[1]}")

    st.markdown("---")
    st.info("Use the sidebar to explore each hypothesis and see how these factors relate to diabetes risk.")
    
elif page == "**H1**: Lifestyle Habits and diabetes":
    st.subheader("Hypothesis 1: Lifestyle Habits and diabetes")
    st.write("**Hypothesis**: Modifiable behaviours – including smoking, physical inactivity, insufficient fruit and vegetable intake, and heavy alcohol consumption – are associated with a higher risk of diabetes.")
    st.write("Let's explore all variables first. The graph below shows how each lifestyle habit relates to diabetes prevalence in the dataset.")
    # st.write("Rationale: Lifestyle factors are the most modifiable determinants of health. Demonstrating their impact provides evidence for targeted prevention campaigns and behavioural interventions.")
    
elif page == "**H2**: Education and diabetes prevention":
    st.subheader("Hypothesis 2")
    st.write("Content for Hypothesis 2 will go here.")
    
elif page == "**H3**: Healthcare access and diabetes":
    st.subheader("Hypothesis 3")
    st.write("Content for Hypothesis 3 will go here.")
    
elif page == "**H4**: Self-rated health and diabetes":
    st.subheader("Hypothesis 4")
    st.write("Content for Hypothesis 4 will go here.")
    
elif page == "**H5**: Pre-existing health conditions and diabetes":
    st.subheader("Hypothesis 5")
    st.write("Content for Hypothesis 5 will go here.")
    
elif page == "Conclusion":
    st.subheader("Conclusion")
    st.write("Summary of findings and insights will go here.")
