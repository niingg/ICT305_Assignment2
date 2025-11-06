import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Import hypothesis modules with CORRECT functions
from hypothesis_h1 import (
    create_risk_factors_chart,
    create_individual_lifestyle_factors_chart,
    create_physical_activity_by_demographics_chart,
)

from hypothesis_h2 import (
    create_education_health_behaviors_chart,
    create_education_diabetes_trend_chart,
    create_income_diabetes_by_education_chart,
    create_education_lifestyle_diabetes_chart,
)

from hypothesis_h3 import (
    create_healthcare_coverage_chart,
    create_income_trends_dual_chart,
    create_access_barriers_chart,
    create_preexisting_factors_chart,
)

from hypothesis_h4 import (
    create_health_trends_chart,
    create_functional_limitations_comparison_chart,
    create_physical_activity_demographics_chart,
    create_functional_limitations_chart,
)

from hypothesis_h5 import (
    create_preexisting_conditions_chart,
    create_preexisting_conditions_demographics_chart,
    create_bmi_categories_chart,
    create_condition_count_chart,
)

# Load dataset
df = pd.read_csv('diabetes_binary_5050split_health_indicators_BRFSS2015.csv')
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-', '_')

# ============================================================================
# HELPER FUNCTIONS FOR H1
# ============================================================================

# ============================================================================
# PAGE SETUP
# ============================================================================

st.set_page_config(page_title="Diabetes Risk Factors Dashboard", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", [
    "Introduction",
    "**H1**: Lifestyle Habits and Diabetes",
    "**H2**: Education and Diabetes Prevention",
    "**H3**: Healthcare Access and Diabetes",
    "**H4**: Self-Rated Health and Diabetes",
    "**H5**: Pre-existing Health Conditions and Diabetes",
    "Conclusion"
])

# --- Header ---
st.markdown("<h1 style='text-align: center;'>Diabetes Risk Factors Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# ============================================================================
# PAGE CONTENT
# ============================================================================

if page == "Introduction":
    st.subheader("Introduction")
    st.write("Welcome to the Diabetes Risk Factors Dashboard. Here you can explore various factors associated with diabetes risk.")

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
    The dataset used in this analysis is derived from the **BRFSS 2015 Health Indicators Data**, 
    which contains health-related behavioral data collected by the CDC.
    It includes various features such as BMI, blood pressure indicators, healthcare access, lifestyle habits, and health metrics.

    The dataset will be used to explore five hypotheses regarding potential diabetes risk factors.
    """)

    # Display a sample of the dataset
    st.write("Here's a glimpse of the data:")
    st.dataframe(df.head())

    # Display some basic stats
    st.write("**Basic Dataset Information:**")
    st.write(f"- Number of records: {df.shape[0]:,}")
    st.write(f"- Number of features: {df.shape[1]}")
    st.write(f"- Diabetes prevalence: {df['diabetes_binary'].mean():.1%}")

    st.markdown("---")
    st.info("Use the sidebar to explore each hypothesis and see how these factors relate to diabetes risk.")

# ============================================================================
# H1: LIFESTYLE HABITS
# ============================================================================

elif page == "**H1**: Lifestyle Habits and Diabetes":
    st.subheader("Hypothesis 1: Lifestyle Habits and Diabetes")
    st.write("""
    **Hypothesis**: Modifiable behaviours – including smoking, physical inactivity, insufficient fruit and vegetable intake, 
    and heavy alcohol consumption – are associated with a higher risk of diabetes.
    """)
    st.write("The visualizations below show how lifestyle habits relate to diabetes risk.")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs([
        "Individual Factors",
        "Risk Factors Accumulation",
        "Physical Activity by Demographics"
    ])
    
    with tab1:
        st.write("**Individual Lifestyle Factors**")
        st.write("Compares diabetes rates between people with and without each risk factor, including 95% confidence intervals:")
        fig0 = create_individual_lifestyle_factors_chart(df)
        st.plotly_chart(fig0, use_container_width=True)
    
    with tab2:
        st.write("**Diabetes Prevalence by Number of Risk Factors**")
        st.write("Shows how diabetes risk increases as more lifestyle risk factors accumulate:")
        fig1 = create_risk_factors_chart(df)
        st.plotly_chart(fig1, use_container_width=True)
    
    with tab3:
        st.write("**Physical Activity vs Diabetes by Education, Age Group, and Sex**")
        st.write("Choose which demographic to view:")
        
        facet_choice = st.selectbox(
            "Select demographic view:",
            ["Education", "Age Group", "Sex"],
            key="h1_facet"
        )
        
        facet_map = {"Education": "education", "Age Group": "age", "Sex": "sex"}
        fig2 = create_physical_activity_by_demographics_chart(df, facet_type=facet_map[facet_choice])
        st.plotly_chart(fig2, use_container_width=True)

# ============================================================================
# H2: EDUCATION
# ============================================================================

elif page == "**H2**: Education and Diabetes Prevention":
    st.subheader("Hypothesis 2: Education and Diabetes Prevention")
    st.write("""
    **Hypothesis**: Higher educational attainment reduces the likelihood of diabetes, both directly through health literacy 
    and indirectly via healthier behaviours and improved healthcare access.
    """)
    st.write("""
    The visualizations below show how education relates to diabetes risk and health behaviors.
    """)
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs([
        "Health Behaviors by Education",
        "Diabetes by Education",
        "Income vs Education",
        "Education & Lifestyle Trends"
    ])
    
    with tab1:
        st.write("**Health Behaviors Improve with Education**")
        st.write("Shows the prevalence of healthy diet, physical activity, and regular checkups by education level:")
        fig1 = create_education_health_behaviors_chart(df)
        st.plotly_chart(fig1, use_container_width=True)
    
    with tab2:
        st.write("**Diabetes Rates Decline with Higher Education**")
        st.write("Clear trend showing diabetes rates decrease as education level increases:")
        fig2 = create_education_diabetes_trend_chart(df)
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab3:
        st.write("**Diabetes by Income and Education Level**")
        st.write("Heatmap showing how both income and education interact to affect diabetes risk:")
        fig3 = create_income_diabetes_by_education_chart(df)
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab4:
        st.write("**Education's Impact on Lifestyle and Diabetes**")
        st.write("Shows how education predicts lifestyle choices and diabetes rates:")
        fig4 = create_education_lifestyle_diabetes_chart(df)
        st.plotly_chart(fig4, use_container_width=True)

# ============================================================================
# H3: HEALTHCARE ACCESS
# ============================================================================

elif page == "**H3**: Healthcare Access and Diabetes":
    st.subheader("Hypothesis 3: Healthcare Access and Diabetes")
    st.write("""
    **Hypothesis**: Limited access to healthcare – due to cost barriers, lack of regular care, or low income – 
    is associated with higher rates of diabetes.
    """)
    st.write("""
    The visualizations below show how healthcare access relates to diabetes rates across different demographic groups 
    and income levels.
    """)

    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs([
        "Coverage & Barriers",
        "Income Trends",
        "Access Barriers",
        "Individual Conditions"
    ])

    with tab1:
        st.write("**Healthcare Coverage & Cost Barriers by Income Level**")
        st.write("Use the dropdown to view data for different income levels:")
        fig1 = create_healthcare_coverage_chart(df)
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        st.write("**Income Level Impact on Healthcare Access and Diabetes**")
        st.write("Left chart: Diabetes rate by income | Right chart: Healthcare coverage gaps by income")
        fig2 = create_income_trends_dual_chart(df)
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        st.write("**Cumulative Effect of Healthcare Access Barriers**")
        st.write("Shows diabetes rates based on number of access barriers (0, 1, or 2):")
        fig3 = create_access_barriers_chart(df)
        st.plotly_chart(fig3, use_container_width=True)

    with tab4:
        st.write("**Individual Cardiovascular Conditions**")
        st.write("Shows how each condition independently affects diabetes prevalence:")
        fig4 = create_preexisting_factors_chart(df)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.subheader("Key Insights")
    st.write("""
    - Healthcare access barriers significantly impact diabetes management and prevalence
    - Lower income is strongly associated with higher diabetes rates AND worse healthcare access
    - Multiple healthcare barriers compound the effect on diabetes risk
    - Cardiovascular conditions are important indicators of diabetes risk
    """)

# ============================================================================
# H4: SELF-RATED HEALTH
# ============================================================================

elif page == "**H4**: Self-Rated Health and Diabetes":
    st.subheader("Hypothesis 4: Self-Rated Health and Diabetes")
    st.write("""
    **Hypothesis**: Poor self-rated health and functional limitations – including low general health ratings, 
    more unhealthy days, and difficulty walking – are strongly associated with diabetes.
    """)
    st.write("""
    The visualizations below show how various health indicators relate to diabetes across different demographic groups.
    """)

    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs([
        "Health Trends",
        "Functional Limitations",
        "Physical Activity by Demographics",
        "Limitation Impact"
    ])

    with tab1:
        st.write("**Trends in Diabetes vs Unhealthy Days by General Health Rating**")
        st.write("Dual-axis chart showing diabetes rate alongside mental and physical unhealthy days:")
        fig1 = create_health_trends_chart(df)
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        st.write("**Functional Limitations Comparison**")
        st.write("Left: Difficulty walking | Right: Physical activity engagement")
        fig2 = create_functional_limitations_comparison_chart(df)
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        st.write("**Physical Activity Impact Across Demographics**")
        st.write("Use the dropdown to switch between Age Group, Sex, and BMI Category:")
        fig3 = create_physical_activity_demographics_chart(df)
        st.plotly_chart(fig3, use_container_width=True)

    with tab4:
        st.write("**Effect of Functional Limitations**")
        st.write("Shows diabetes rates by functional limitation status:")
        fig4 = create_functional_limitations_chart(df)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.subheader("Key Insights")
    st.write("""
    - Self-rated health is a powerful indicator of diabetes prevalence
    - Both mental and physical unhealthy days correlate with diabetes
    - Physical activity is protective against diabetes across ALL demographic groups
    - Functional limitations substantially increase diabetes risk
    """)

# ============================================================================
# H5: PRE-EXISTING CONDITIONS
# ============================================================================

elif page == "**H5**: Pre-existing Health Conditions and Diabetes":
    st.subheader("Hypothesis 5: Pre-existing Health Conditions and Diabetes")
    st.write("""
    **Hypothesis**: Individuals with pre-existing cardiometabolic conditions – such as stroke, heart disease or heart attack, 
    high blood pressure, high cholesterol, and elevated BMI – are more likely to be diagnosed with diabetes.
    """)
    st.write("""
    The visualizations below show how pre-existing health conditions relate to diabetes rates. 
    Pre-existing conditions include: Stroke, Heart Disease/Attack, High Blood Pressure, High Cholesterol, and Elevated BMI (≥30).
    """)

    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs([
        "Individual Conditions",
        "By Demographics",
        "BMI Categories",
        "Condition Count"
    ])

    with tab1:
        st.write("**Pre-existing Conditions and Diabetes Risk**")
        st.write("Use the dropdown to sort by Prevalence (diabetes rate) or Relative Risk (yes/no ratio):")
        fig1 = create_preexisting_conditions_chart(df)
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        st.write("**Pre-Existing Conditions by Demographics**")
        st.write("Use the dropdown to switch between Age Group and Sex views:")
        fig2 = create_preexisting_conditions_demographics_chart(df)
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        st.write("**Diabetes Rate by BMI Category**")
        st.write("Shows progression across 6 BMI classification levels with color gradient:")
        fig3 = create_bmi_categories_chart(df)
        st.plotly_chart(fig3, use_container_width=True)

    with tab4:
        st.write("**Effect of Multiple Pre-existing Conditions**")
        st.write("Shows how diabetes risk increases with each additional condition:")
        fig4 = create_condition_count_chart(df)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.subheader("Key Insights")
    st.write("""
    - Pre-existing conditions are strongly associated with higher diabetes risk
    - BMI is one of the strongest individual predictors of diabetes
    - Risk increases exponentially with each additional condition
    - Cardiovascular risk factors and diabetes are closely intertwined
    - Early screening and management of these conditions is crucial for diabetes prevention
    """)

# ============================================================================
# CONCLUSION
# ============================================================================

elif page == "Conclusion":
    st.subheader("Conclusion")
    st.write("""
    ## Summary of Findings

    This analysis explored five hypotheses about diabetes risk factors using the BRFSS 2015 Health Indicators dataset. 
    Here are the key findings:

    ### **H1: Lifestyle Habits**
    Modifiable behaviors significantly impact diabetes risk. Smoking, physical inactivity, and poor diet are key factors.
    These are the most controllable risk factors and represent the strongest opportunities for intervention.

    ### **H2: Education**
    [To be completed by your group - exploring how educational attainment affects diabetes risk]

    ### **H3: Healthcare Access**
    Healthcare access barriers create a powerful barrier to diabetes management and prevention.
    - **Income effect**: Lower income → less healthcare access → higher diabetes (clear trend)
    - **Access barriers**: Multiple barriers compound the risk
    - **Cardiovascular indicators**: Strongly predict diabetes risk
    - **Implication**: Addressing healthcare disparities is critical

    ### **H4: Self-Rated Health**
    Subjective health assessments are reliable indicators of diabetes risk.
    - **Health rating**: Excellent to Poor shows clear progression
    - **Unhealthy days**: Both mental and physical health matter
    - **Physical activity**: Protective effect across all demographics
    - **Functional limitations**: Substantially increase risk
    - **Implication**: Holistic health management is essential

    ### **H5: Pre-existing Conditions**
    Cardiometabolic conditions are strongly linked with diabetes.
    - **BMI**: Shows clear progression from underweight to obese
    - **Cardiovascular disease**: Each condition independently increases risk
    - **Cumulative effect**: Risk increases exponentially with multiple conditions
    - **Implication**: Integrated care for multiple conditions is needed

    ---

    ## Recommendations

    1. **Healthcare Access**: Ensure equitable access to preventive care, especially for low-income populations
    2. **Lifestyle Interventions**: Promote smoking cessation, physical activity, and healthy eating
    3. **Early Screening**: Screen for and manage cardiometabolic risk factors early
    4. **Community Programs**: Implement comprehensive diabetes prevention programs targeting high-risk populations
    5. **Health Education**: Increase health literacy to support informed decision-making

    ---

    ## Data Notes

    - **Dataset**: BRFSS 2015 Health Indicators, 50-50 split (diabetes/non-diabetes)
    - **Sample Size**: ~250,000 individuals
    - **Variables**: 22 health and demographic indicators
    - **Diabetes Prevalence**: 50% (balanced sample)

    """)