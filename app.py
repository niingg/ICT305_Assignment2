import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ============================================================================
# STYLING FUNCTIONS
# ============================================================================

# Color constants
COLORS = {
    "primary": "#931A23",
    "secondary": "#E8C6AE",        # Accent (light tan)
    "positive": "#2ECC71",         # Green (good data)
    "neutral": "#3498DB",          # Blue (neutral)
    "background_grid": "#F2F4F7",  # Light background
    "grid": "rgba(0, 0, 0, 0.08)", # Grid lines
    "success": "#2ECC71",
    "warning": "#F39C12",
    "error": "#E74C3C",
    "header_bg": "#FFE5E5",
}

# function to style headings
def styled_heading(text, level=2, color="#931A23", align="left"):
    """Display a heading with color, weight, and alignment."""
    tags = {1: "h1", 2: "h2", 3: "h3"}
    tag = tags.get(level, "h2")
    font_sizes = {1: "32px", 2: "24px", 3: "18px"}
    font_size = font_sizes.get(level, "24px")
    
    html = f"""
    <{tag} style='
        color: {color};
        font-size: {font_size};
        font-weight: 700;
        margin-bottom: 16px;
        text-align: {align};
    '>{text}</{tag}>
    """
    st.markdown(html, unsafe_allow_html=True)

# function to add background colour for header
def styled_header():
    """
    Display the app header with light red background and serif font.
    Replaces the default header styling with professional branding.
    """
    html = f"""
    <div style='
        background-color: {COLORS["header_bg"]};
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    '>
        <h1 style='
            text-align: center;
            color: {COLORS["primary"]};
            font-size: 40px;
            margin: 0;
        '>Diabetes Risk Factors Dashboard</h1>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
    st.markdown("---")

# Import hypothesis modules with functions
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

from conclusion import create_sankey_diagram
from introduction import display_body_diagram

# Load dataset
df = pd.read_csv('diabetes.csv')
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-', '_') #standardising column names

# ==============
# PAGE SETUP
# ==============

st.set_page_config(page_title="Diabetes Risk Factors Dashboard", layout="wide")

# sidebar nagivation - radio button style
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", [
    "Introduction",
    "**H1**: Lifestyle Habits and Diabetes",
    "**H2**: Education and Diabetes",
    "**H3**: Healthcare Access and Diabetes",
    "**H4**: Self-Rated Health and Diabetes",
    "**H5**: Pre-existing Health Conditions and Diabetes",
    "Conclusion"
])

# Header with light red background and serif font
styled_header()

# ==============
# PAGE CONTENT
# ==============

if page == "Introduction":
    styled_heading("Introduction", level=2)
    st.write("Welcome to the Diabetes Risk Factors Dashboard! Here you can explore various factors associated with diabetes risk.")

    styled_heading("Case Introduction", level=2)
    st.write("""
    Diabetes is a chronic medical condition that occurs when the body cannot properly regulate blood sugar (glucose) levels. 
    If left unmanaged, it can lead to serious health complications such as heart disease, kidney failure, and nerve damage. 

    Understanding the **risk factors** associated with diabetes is crucial for early detection and prevention. 
    This dashboard explores key health indicators and their relationship with the likelihood of developing diabetes.
    """)

    st.markdown("---")

    styled_heading("Dataset Overview", level=2)
    st.write("""
    The dataset used in this analysis is derived from the **BRFSS 2015 Health Indicators Data**, 
    which contains health-related behavioral data collected by the CDC.
    It includes various features such as BMI, blood pressure indicators, healthcare access, lifestyle habits, and health metrics.
             
    In total, the dataset has 22 variables. A glimpse of the data table is shown below:
    """)

    # Display a sample of the dataset
    st.dataframe(df.head())

    st.write("")
    st.write("""
    Based on these 22 variables, we decided to group them into a few different domains, as seen in the table below:
    """)

    variables_info = pd.DataFrame(
        {
            "Domain": ["Lifestyle Habits", "Demographics", "Healthcare Access", "Self-Rated Health", "Pre-existing Conditions"],
            "Variables": [
                "Smoking, Physical Activity, Fruit/Vegetable Intake, Alcohol Consumption", "Age, Sex, Education, Income, BMI",
                "Healthcare Coverage, Cost Barriers, Regular Checkups", "General Health Rating, Mental Health, Physical Health, Difficulty Walking",
                "Stroke, Heart Disease/Attack, High Blood Pressure, High Cholesterol"]
        })
    st.table(variables_info)

    # Additional explanation
    st.write("")
    st.write("Based on the above groupings, we came up with our five hypotheses:")
    st.write("1. Lifestyle Habits and Diabetes")
    st.write("2. Education and Diabetes")
    st.write("3. Healthcare Access and Diabetes")
    st.write("4. Self-Rated Health and Diabetes")
    st.write("5. Pre-existing Health Conditions and Diabetes")
    st.write("")
    st.write("Our dashboard is organised according to these five hypotheses, with one section for each. Please explore the hypotheses by clicking the buttons in the side navigation bar!")
    st.markdown("---")
    st.write("For more information about the dataset, please visit the dataset page at https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators")


    st.markdown("---")
    
    # BODY DIAGRAM - NEW SECTION
    styled_heading("🫀 How Diabetes Affects Your Body")
    display_body_diagram()
    
# =====================
# H1: LIFESTYLE HABITS
# =====================

elif page == "**H1**: Lifestyle Habits and Diabetes":
    styled_heading("Hypothesis 1: Lifestyle Habits and Diabetes", level=2)
    st.write("Wondering how lifestyle habits such as your diet, exercise, and smoking status impact your risk of diabetes? Browse through the visualisations below!")
    st.write("The **first tab** explores an overall view of how all the lifestyles factors listed impacts your diabetes risk.")
    st.write("The **second tab** shows how having 1 or more of these factors together impacts the risk of diabetes.")
    st.write("Lastly, the **third tab** shows..... [CLARIFY WITH GIZ AND NAT FOR EXPLANATION]")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs([
        "Individual Factors",
        "Risk Factors Accumulation",
        "Physical Activity by Demographics"
    ])
    
    with tab1:
        fig0 = create_individual_lifestyle_factors_chart(df)
        st.plotly_chart(fig0, use_container_width=True)
        st.markdown("---")
        styled_heading("Key Insights", level=2)
        st.write("""
        - People who smoke or don’t exercise have much higher diabetes rates than those who don’t.
        - Physical inactivity (62%) shows the strongest link with diabetes risk.
        - Those with low fruit or vegetable intake also show slightly higher diabetes levels.
        """)
    
    with tab2:
        st.write("**Diabetes Prevalence by Number of Risk Factors**")
        st.write("Shows how diabetes risk increases as more lifestyle risk factors accumulate:")
        fig1 = create_risk_factors_chart(df)
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("---")
        styled_heading("Key Insights", level=2)
        st.write("""
        - The more unhealthy habits a person has, the higher their diabetes risk.
        - Diabetes rate increases from 38% (no risks) to nearly 60% (three risks).
        - Having even one or two bad habits significantly raises the likelihood of diabetes.
        """)
    
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
        st.markdown("---")
        styled_heading("Key Insights", level=2)
        st.write("""
        - Across all groups, physically active people have much lower diabetes rates than inactive ones.
        - The gap is largest among older adults (60–74) and those with less education.
        - Higher education and regular activity together lead to the lowest diabetes levels (as low as 36%).
        """)

# ===============
# H2: EDUCATION
# ===============

elif page == "**H2**: Education and Diabetes":
    styled_heading("Hypothesis 2: Education and Diabetes", level=2)
    st.write("Now that you understand how lifestyle factors affect diabetes, let's dive into demographic influences!")
    st.write("The graph in the **first tab** investigates how education level impacts health behaviors, namely diet, physical activity, and regular checkups.")
    st.write("The **second tab** explores the direct relationship between education level and diabetes prevalence.")
    st.write("The **third tab** examines how income and education together influence diabetes risk.")
    st.write("Lastly, the **fourth tab** illustrates how education level affects lifestyle choices and diabetes rates as a whole.")
    
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
        st.markdown("---")
        styled_heading("Key Insights", level=2)
        st.write("""
        - People with higher education levels are more likely to eat well, stay active, and go for regular checkups.
        - The rate of healthy diet, exercise, and screenings all rise from “Less than High School” to “College Graduate.
        - This suggests that education improves awareness and discipline toward healthy living.
        - College graduates show the highest rates of positive health habits in all categories.
        """)
    
    with tab2:
        st.write("**Diabetes Rates Decline with Higher Education**")
        st.write("Clear trend showing diabetes rates decrease as education level increases:")
        fig2 = create_education_diabetes_trend_chart(df)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("---")
        styled_heading("Key Insights", level=2)
        st.write("""
        - The rate of diabetes clearly decreases as education level increases.
        - Those with less than high school have about 68% diabetes rate, while college graduates have around 40%.
        - This shows that education plays a strong protective role against diabetes.
        """)
    
    with tab3:
        st.write("**Diabetes by Income and Education Level**")
        st.write("Heatmap showing how both income and education interact to affect diabetes risk:")
        fig3 = create_income_diabetes_by_education_chart(df)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("---")
        styled_heading("Key Insights", level=2)
        st.write("""
        - People with low income and low education have the highest diabetes rates across all groups.
        - As income and education increase together, the diabetes rate drops steadily.
        - The lowest diabetes rates appear among those with college education and higher income.
        """)
    
    with tab4:
        st.write("**Education's Impact on Lifestyle and Diabetes**")
        st.write("Shows how education predicts lifestyle choices and diabetes rates:")
        fig4 = create_education_lifestyle_diabetes_chart(df)
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("---")
        styled_heading("Key Insights")
        st.write("""
        - With more education, people are more active and eat more fruits and vegetables.
        - At the same time, diabetes rates drop steadily as education level rises.
        - This shows a direct link between education, healthy habits, and lower diabetes risk.
        """)

# ============================================================================
# H3: HEALTHCARE ACCESS
# ============================================================================

elif page == "**H3**: Healthcare Access and Diabetes":
    styled_heading("Hypothesis 3: Healthcare Access and Diabetes", level=2)
    st.write("""
    **Hypothesis**: Limited access to healthcare – due to cost barriers, lack of regular care, or low income – 
    is associated with higher rates of diabetes.
    """)
    st.write("""
    The visualizations below show how healthcare access relates to diabetes rates across different demographic groups 
    and income levels.
    """)

    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs([
        "Coverage & Barriers",
        "Income Trends",
        "Access Barriers",
    ])

    with tab1:
        st.write("**Healthcare Coverage & Cost Barriers by Income Level**")
        st.write("Use the dropdown to view data for different income levels:")
        fig1 = create_healthcare_coverage_chart(df)
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("---")
        styled_heading("Key Insights")
        st.write("""
        - Diabetes rates are consistently higher among those without healthcare coverage or with cost barriers.
        - Low-income groups (<$25k) show the largest gap between “Yes” and “No” responses.
        - High income groups (>$75k) show much lower diabetes rates and fewer barriers.
        """)

    with tab2:
        st.write("**Income Level Impact on Healthcare Access and Diabetes**")
        st.write("Left chart: Diabetes rate by income | Right chart: Healthcare coverage gaps by income")
        fig2 = create_income_trends_dual_chart(df)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("---")
        styled_heading("Key Insights")
        st.write("""
        - Diabetes rates decline steadily with higher income levels.
        - The lowest-income groups (<$15k) have diabetes rates nearly double that of the highest-income group.
        - Lack of healthcare coverage also drops drasticly with income, showing parallel trends.
        """)

    with tab3:
        st.write("**Cumulative Effect of Healthcare Access Barriers**")
        st.write("Shows diabetes rates based on number of access barriers (0, 1, or 2):")
        fig3 = create_access_barriers_chart(df)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("---")
        styled_heading("Key Insights")
        st.write("""
        - 0 barriers has the lowest diabetes rate and 2 barriers has the highest diabetes rate.
        - The jump from 0 to 2 barriers shows a clear compounding effect.
        - Demonstrates that multiple healthcare challenges increase risk, not just add to it.
        """)

# ============================================================================
# H4: SELF-RATED HEALTH
# ============================================================================

elif page == "**H4**: Self-Rated Health and Diabetes":
    styled_heading("Hypothesis 4: Self-Rated Health and Diabetes")
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
        st.markdown("---")
        styled_heading("Key Insights")
        st.write("""
        - Moving from Excellent to Poor self-rated health, diabetes rises sharply.
        - Mental and physical unhealthy days increase in parallel.
        - Patterns suggest mutual reinforcement of poor wellbeing and diabetes.
        - Self-ratings serve as a strong early signal.
        """)

    with tab2:
        st.write("**Functional Limitations Comparison**")
        st.write("Left: Difficulty walking | Right: Physical activity engagement")
        fig2 = create_functional_limitations_comparison_chart(df)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("---")
        styled_heading("Key Insights")
        st.write("""
        - Difficulty walking = much higher diabetes rate.
        - Regular physical activity = lower diabetes rate.
        - Mobility and activity act as strong risk/protective factors.
        """)

    with tab3:
        st.write("**Physical Activity Impact Across Demographics**")
        st.write("Use the dropdown to switch between Age Group, Sex, and BMI Category:")
        fig3 = create_physical_activity_demographics_chart(df)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("---")
        styled_heading("Key Insights")
        st.write("""
        - In every facet, active groups have lower diabetes rates.
        - (60+) and obese groups gain the largest benefit from activity.
        - Males are slightly higher than females across states, but the activity gap dominates.
        """)

    with tab4:
        st.write("**Effect of Functional Limitations**")
        st.write("Shows diabetes rates by functional limitation status:")
        fig4 = create_functional_limitations_chart(df)
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("---")
        styled_heading("Key Insights")
        st.write("""
        - Having any physical limitation greatly increases the chance of diabetes.
        - The difference between having no limitations and at least one is large and consistent.
        - Even small mobility problems can indicate a higher risk of long-term illness.
        """)

# ============================================================================
# H5: PRE-EXISTING CONDITIONS
# ============================================================================

elif page == "**H5**: Pre-existing Health Conditions and Diabetes":
    styled_heading("Hypothesis 5: Pre-existing Health Conditions and Diabetes")
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
        st.markdown("---")
        styled_heading("Key Insights")
        st.write("""
        - All four conditions show much higher diabetes rates for those affected vs those without.
        - Heart disease (75%) and stroke (74%) have the highest diabetes prevalence, showing strong comorbidity.
        - High blood pressure (67%) and high cholesterol (64%) are also major contributors, due to shared metabolic risk.
        """)

    with tab2:
        st.write("**Pre-Existing Conditions by Demographics**")
        st.write("Use the dropdown to switch between Age Group and Sex views:")
        fig2 = create_preexisting_conditions_demographics_chart(df)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("---")
        styled_heading("Key Insights")
        st.write("""
        - Diabetes rates rise steadily with age, with the sharpest jump seen from middle to older adults (45+).
        - Individuals with pre-existing conditions experience a much higher prevalence across all ages — from 16% (18–29) to 65% (60–74).
        - Males (59.8%) show slightly higher rates than females (57.7%), but the presence of chronic conditions outweighs gender differences.
        """)

    with tab3:
        st.write("**Diabetes Rate by BMI Category**")
        st.write("Shows progression across 6 BMI classification levels with color gradient:")
        fig3 = create_bmi_categories_chart(df)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("---")
        styled_heading("Key Insights")
        st.write("""
        - Diabetes rates rise progressively with BMI, from 26% (underweight) to 76% (Class 3 obesity).
        - The sharpest increase begins at BMI ≥30 (obesity threshold).
        - Indicates a strong linear relationship between excess weight and diabetes risk.
        """)

    with tab4:
        st.write("**Effect of Multiple Pre-existing Conditions**")
        st.write("Shows how diabetes risk increases with each additional condition:")
        fig4 = create_condition_count_chart(df)
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("---")
        styled_heading("Key Insights")
        st.write("""
        - Older people have a higher chance of diabetes than younger ones.
        - People with other health problems (like high blood pressure or heart disease) are much more likely to have diabetes at every age.
        - Men (59.8%) have slightly higher rates than women (57.7%), but the difference is small.
        - Getting older and having more health problems both make diabetes much more likely.
        """)

# ============================================================================
# CONCLUSION
# ============================================================================

elif page == "Conclusion":
    st.markdown("<h2 style='text-align: center;'>Conclusion</h2>", unsafe_allow_html=True)
    
    # Introduction
    st.write("""
    This analysis explored five hypotheses about diabetes risk factors using the **CDC Diabetes Health Indicators dataset**. 
    This page summarizes the key findings from each hypothesis.
    """)
    st.markdown("---")
    
    # SECTION 1: Summary of Findings
    styled_heading("Summary of Findings")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div style='background-color: #E8F5E9; padding: 12px; border-radius: 8px; text-align: center;'>
            <strong>H1: Lifestyle</strong><br>
            <span style='color: #738a6e; font-size: 20px;'>✅ Accepted</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background-color: #E8F5E9; padding: 12px; border-radius: 8px; text-align: center;'>
            <strong>H2: Education</strong><br>
            <span style='color: #738a6e; font-size: 20px;'>✅ Accepted</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background-color: #FFE5E5; padding: 12px; border-radius: 8px; text-align: center;'>
            <strong>H3: Healthcare</strong><br>
            <span style='color: #9B1128; font-size: 20px;'>❌ Rejected</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style='background-color: #E8F5E9; padding: 12px; border-radius: 8px; text-align: center;'>
            <strong>H4: Self-Health</strong><br>
            <span style='color: #738a6e; font-size: 20px;'>✅ Accepted</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div style='background-color: #E8F5E9; padding: 12px; border-radius: 8px; text-align: center;'>
            <strong>H5: Conditions</strong><br>
            <span style='color: #738a6e; font-size: 20px;'>✅ Accepted</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # SECTION 2: Detailed Findings
    styled_heading("Detailed Findings by Hypothesis")
    
    st.write("""
    #### **H1: Lifestyle Habits**
    Modifiable behaviors significantly impact diabetes risk. Smoking, physical inactivity, and poor diet are key factors.
    These are the most controllable risk factors and represent the strongest opportunities for intervention.
    
    ---
    
    #### **H2: Education**
    [To be completed by your group - exploring how educational attainment affects diabetes risk]
    
    ---
    
    #### **H3: Healthcare Access**
    Healthcare access barriers create a powerful barrier to diabetes management and prevention.
    - **Income effect**: Lower income → less healthcare access → higher diabetes (clear trend)
    - **Access barriers**: Multiple barriers compound the risk
    - **Cardiovascular indicators**: Strongly predict diabetes risk
    - **Implication**: Addressing healthcare disparities is critical
    
    ---
    
    #### **H4: Self-Rated Health**
    Subjective health assessments are reliable indicators of diabetes risk.
    - **Health rating**: Excellent to Poor shows clear progression
    - **Unhealthy days**: Both mental and physical health matter
    - **Physical activity**: Protective effect across all demographics
    - **Functional limitations**: Substantially increase risk
    - **Implication**: Holistic health management is essential
    
    ---
    
    #### **H5: Pre-existing Conditions**
    Cardiometabolic conditions are strongly linked with diabetes.
    - **BMI**: Shows clear progression from underweight to obese
    - **Cardiovascular disease**: Each condition independently increases risk
    - **Cumulative effect**: Risk increases exponentially with multiple conditions
    - **Implication**: Integrated care for multiple conditions is needed
    """)
    
    st.markdown("---")
    
    # SECTION 3: Sankey Diagram (NEW!)
    styled_heading("Data Flow & Hypothesis Conclusions")
    st.write("This Sankey diagram visualizes how data variables flow through each hypothesis to their conclusions (Accept/Reject):")
    
    # Display the Sankey diagram
    sankey_fig = create_sankey_diagram()
    st.plotly_chart(sankey_fig, use_container_width=True)
    
    st.info("""
    **How to read the diagram:**
    - **Left side (Data Variables)**: The 18 measured health indicators from the dataset
    - **Middle (Hypotheses)**: The 5 research questions being tested
    - **Right side (Conclusions)**: Whether each hypothesis was Accepted or Rejected
    - **Flow width**: Represents the magnitude of data relationships
    - **Colors**: Different colors represent different data pathways
    """)
    
    st.markdown("---")
    
    # SECTION 4: Recommendations
    styled_heading("Key Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("""
        **For Individuals:**
        1. Focus on modifiable behaviors (smoking, physical activity, diet)
        2. Maintain awareness of pre-existing health conditions
        3. Regular health check-ups and screening
        4. Improve health literacy through education
        """)
    
    with col2:
        st.write("""
        **For Healthcare Providers & Policy:**
        1. Ensure equitable access to preventive care
        2. Promote lifestyle intervention programs
        3. Screen for and manage cardiometabolic risk factors early
        4. Target high-risk populations with community programs
        """)
    
    st.markdown("---")
    
    # SECTION 5: Data Notes
    styled_heading("Data Notes")
    st.write(f"""
    - **Dataset**: CDC Diabetes Health Indicators, 50-50 split (diabetes/non-diabetes)
    - **Sample Size**: {df.shape[0]:,} individuals
    - **Variables**: {df.shape[1]} health and demographic indicators
    - **Diabetes Prevalence**: 50% (balanced sample)
    """)