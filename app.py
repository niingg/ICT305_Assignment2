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
    "**H5**: Pre-Existing Health Conditions and Diabetes",
    "Conclusion"
])

# Header with light red background and serif font
styled_header()

# ==============
# PAGE CONTENT
# ==============

if page == "Introduction":
    styled_heading("Introduction", level=1, align="center")
    st.markdown("""
    <div style='text-align: center; font-size: 18px;'>
        Welcome to the <b>Diabetes Risk Factors Dashboard!</b>
        Here you can explore various risk factors associated with diabetes.\n
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")  
    st.info("💡 Recommended settings for the best viewing experience.\n\n"
    "**Menu → Settings →  ❎ Disable Wide mode ✅ Use Light mode**")
    
    st.markdown("---")
    styled_heading("Team Members", level=2)
    
    col1, col2, col3, col4, col5 =st.columns(5)
    with col1:
        st.markdown(f"""
        <div style='background-color: #FFF1A4; padding: 12px; border-radius: 8px; text-align: center;'>
            <span style='color: #000000; font-size: 20px;'><b>Gizella<b></span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style='background-color: #EEC8A3; padding: 12px; border-radius: 8px; text-align: center;'>
            <span style='color: #000000; font-size: 20px;'><b>Natthida<b></span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style='background-color: #DD9C7C; padding: 12px; border-radius: 8px; text-align: center;'>
            <span style='color: #000000; font-size: 20px;'><b>Regina<b></span>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div style='background-color: #D24C49; padding: 12px; border-radius: 8px; text-align: center;'>
            <span style='color: #000000; font-size: 20px;'><b>Salwa<b></span>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
        <div style='background-color: #A64A47; padding: 12px; border-radius: 8px; text-align: center;'>
            <span style='color: #000000; font-size: 20px;'><b>Yee Lin<b></span>
        </div>
        """, unsafe_allow_html=True)
    
    
    st.markdown("---")  

    styled_heading("The Case", level=2)
    st.write("""          
    Countries worldwide are grappling with the increasing prevalence of *diabetes mellitus*, commonly known as diabetes, in their populations. It was reported that 1 in 9 adults worldwide have been diagnosed with the condition in 2025, with the figure projected to grow to 1 in 8 by 2050.

    Diabetes is a chronic medical condition that occurs when the body cannot properly regulate blood sugar (glucose) levels. If left unmanaged, it can lead to serious health complications such as heart disease, kidney failure, and nerve damage.
                               
    A contributing factor to this trend is an increase in diagnosis of Type 2 diabetes. While Type 1 diabetes is an autoimmune condition, Type 2 diabetes can be caused by managable lifestyle factors such as poor dietary habits and lack of exercise.
    """)
    st.markdown("---")

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style='background-color: #F0F8FF; padding: 12px; border-radius: 8px; text-align: center;'>
            <strong>💉 Type 1</strong><br>
            <span style='color: #194875; font-size: 20px;'>Insulin Deficiency</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background-color: #F0F8FF; padding: 12px; border-radius: 8px; text-align: center;'>
            <strong>💊 Type 2</strong><br>
            <span style='color: #194875; font-size: 20px;'>Insulin Resistance</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    styled_heading("Our Mission", level=2)
    st.write("""
    **The Problem:**
    Despite the easy accessibility and availability of healthcare data, there are few resources that have translated complex datasets into meaningful insights.
             
    **Our Goal**
    This dashboard was developed to present facts and figures about risk factors associated with diabetes in an engaging and digestible manner, even for users with minimal medical knowledge.

    **The Narrative**         
    The progression of hypotheses in this dashboard follows the level of impact they have on the potential development of diabetes, in the order of least to most impactful. The conclusion summarises main takeaways from the dashboard and provides actionable recommendations for all target audiences.
    """)

    st.markdown("---")

    styled_heading("Target Audience", level=2, align="center" )
    col1, col2 = st.columns(2)
    st.markdown("---")

    
    with col1:
        st.markdown(f"""
        <div style='background-color: #F0F8FF; padding: 12px; border-radius: 8px; text-align: center;'>
            <span style='font-size: 20px;'><strong>👥 General Public</strong></span><br>
            <span style='color: #194875; font-size: 14px;'>Inform about factors contributing to development of diabetes
            </span>
        </div>
        """, unsafe_allow_html=True)
        
    
    with col2:
        st.markdown(f"""
        <div style='background-color: #F0F8FF; padding: 12px; border-radius: 8px; text-align: center;'>
            <span style='font-size: 20px;'><strong>🏛️ Governments and Policymakers</strong></span><br>
            <span style='color: #194875; font-size: 14px;'>Provide actionable insights for the design of public health programmes</span>
        </div>
        """, unsafe_allow_html=True)
    
    styled_heading("Dataset Overview", level=2)
    st.write("""
    The dataset used in this analysis is derived from the **CDC Diabetes Health Indicators Data**, 
    which contains health-related behavioral data collected by the Centers for Disease Control and Prevention (CDC) from the United States of America.
    It includes various features such as BMI, blood pressure indicators, healthcare access, lifestyle habits, and health metrics.
             
    In total, the dataset has 22 variables. A glimpse of the data table is shown below:
    """)

    # Display a sample of the dataset
    st.dataframe(df.head())

    st.write("")
    st.write("""
    These 22 variables were grouped into a few different domains, as seen in the table below:
    """)

    variables_info = pd.DataFrame({
        "Domain": [
            "Lifestyle Habits", "Demographics", "Healthcare Access",
            "Self-Rated Health", "Pre-Existing Conditions"
        ],
        "Variables": [
            "Smoking, Physical Activity, Fruit/Vegetable Intake, Alcohol Consumption",
            "Age, Sex, Education, Income, BMI",
            "Healthcare Coverage, Cost Barriers, Regular Checkups",
            "General Health Rating, Mental Health, Physical Health, Difficulty Walking, Physical Activity",
            "Stroke, Heart Disease/Attack, High Blood Pressure, High Cholesterol"
        ]
    })

    styled = (
        variables_info.style
            .hide(axis="index")
            .set_table_styles([
                # Header row: deep red background + white text
                {"selector": "th.col_heading", "props": [("background-color", "#EEEEEE"), ("color", "grey"), ("font-weight", "500")]},
                {"selector": "thead th",        "props": [("background-color", "#EEEEEE"), ("color", "grey"), ("font-weight", "500")]},
                # Optional: nicer cell spacing
                {"selector": "td",              "props": [("padding", "8px 10px"), ("vertical-align", "top")]},
                {"selector": "th",              "props": [("padding", "10px")]}
            ])
    )

    st.table(styled)

    # --- Additional Explanation ---
    st.markdown("""
    <style>
    /* Serif across this block */
    .explain-wrap, .explain-wrap * 

    /* Container */
    .explain-wrap{
    background: #fff;
    border: 1px solid #ebedf0;
    border-radius: 14px;
    padding: 18px 22px;
    box-shadow: 0 6px 16px rgba(0,0,0,.05);
    margin-top: 6px;
    }

    /* Heading */
    .explain-title{
    font-weight: 800; margin: 0 0 6px 0; font-size: 20px;
    color: %(primary)s;
    }

    /* Intro text */
    .explain-lead{
    margin: 6px 0 12px 0; color:#222; line-height:1.55;
    }

    /* Numbered list */
    .explain-list{
    counter-reset: num; list-style: none; padding-left: 0; margin: 8px 0 10px 0;
    }
    .explain-list li{
    counter-increment: num; position: relative;
    margin: 8px 0; padding-left: 40px; line-height: 1.5; color:#111;
    }
    .explain-list li::before{
    content: counter(num) ".";
    position: absolute; left: 0; top: 0;
    width: 28px; height: 28px; line-height: 28px; text-align: center;
    border-radius: 999px;
    background: %(chip_bg)s; color: %(primary)s; font-weight: 700;
    border: 1px solid #e6e9ef;
    }

    /* Closing line */
    .explain-note{
    margin-top: 10px; color:#333;
    }

    /* Dataset card */
    .dataset-card{
    margin-top: 14px;
    padding: 14px 16px;
    border: 1px solid #f0e3e3;
    border-radius: 12px;
    background: #fff7f7;
    }
    .dataset-card b{ color: %(primary)s; }
    .dataset-link a{ text-decoration: none; border-bottom: 1px dotted %(primary)s; }
    .dataset-link a:hover{ border-bottom-style: solid; }
    </style>

    <div class="explain-wrap">
    <div class="explain-title">Navigation</div>
    <div class="explain-lead">
        Based on the groupings above, five hypotheses were derived, forming the structure of the dashboard:
    </div>

    <ol class="explain-list">
        <li><b>Lifestyle Habits and Diabetes</b></li>
        <li><b>Education and Diabetes</b></li>
        <li><b>Healthcare Access and Diabetes</b></li>
        <li><b>Self-Rated Health and Diabetes</b></li>
        <li><b>Pre-Existing Health Conditions and Diabetes</b></li>
    </ol>

    <div class="explain-note">
        The dashboard is organised by these five hypotheses — use the side navigation to jump to each section.
    </div>
  
    """ % {
        "primary": COLORS.get("primary", "#8a0d12"),
        "chip_bg": COLORS.get("chip_bg", "#f5f7fa"),
    }, unsafe_allow_html=True)

    st.markdown("---")

    # BODY DIAGRAM - NEW SECTION
    styled_heading("🫀 How Diabetes Affects Your Body")
    display_body_diagram()
    
# =====================
# H1: LIFESTYLE HABITS
# =====================

elif page == "**H1**: Lifestyle Habits and Diabetes":
    styled_heading("Hypothesis 1: Lifestyle Habits and Diabetes", level=1, align="center")
    st.write("""
    **Hypothesis**: Modifiable behaviours – including smoking, physical inactivity, insufficient fruit and vegetable intake, and heavy alcohol consumption – are associated with a higher risk of diabetes.
    """)
    st.markdown("---")
    st.write("Wondering how lifestyle habits such as your diet, exercise, and smoking status impact your risk of developing diabetes? Browse through the visualisations below!")
    st.write("The **first tab** displays a general view of how all the lifestyle factors listed impacts diabetes risk.")
    st.write("The **second tab** shows how having 1 or more of these factors together affects the risk of diabetes.")
    st.write("Lastly, the **third tab** shows the impact of physical activity on the risk of developing diabetes.")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs([
        "Individual Factors",
        "Risk Factors Accumulation",
        "Physical Activity by Demographics"
    ])
    
    with tab1:
        st.write("**Diabetes Prevalence by Lifestyle Habits**")
        st.write("Shows the rate of diabetes for each type of lifestyle habit.")
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
        st.write("Shows how diabetes risk increases as more lifestyle risk factors (smoking, no physical activity, low fruit intake, low veggie intake) accumulate:")
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
        
        # SELECTBOX
        demographic_choice = st.selectbox(
            "Choose demographic to view:",
            ["Age Group", "Sex", "BMI Category"],
            key="h1_demographic"
        )
        
        fig2 = create_physical_activity_by_demographics_chart(df, demographic=demographic_choice)
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
    styled_heading("Hypothesis 2: Education and Diabetes",level=1, align="center")
    st.write("""
    **Hypothesis**: Higher educational attainment reduces the likelihood of diabetes, both directly through health literacy and indirectly via healthier behaviours and improved healthcare access.
    """)
    st.markdown("---")
    st.write("Now that you understand how lifestyle factors affect diabetes, let's dive into demographic influences!")
    st.write("The graph in the **first tab** investigates how education level impacts health behaviors, namely diet, physical activity, and regular checkups.")
    st.write("The **second tab** explores the direct relationship between education level and diabetes prevalence.")
    st.write("The **third tab** examines how income and education together influence diabetes risk.")
    st.write("Lastly, the **fourth tab** illustrates how education level affects lifestyle choices and diabetes rates as a whole.")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs([
        "Health Behaviors by Education Level",
        "Diabetes by Education Level",
        "Income vs Education Level",
        "Education Level & Lifestyle Trends"
    ])
    
    with tab1:
        st.write("**Health Behaviors Improve with Education**")
        st.write("Shows the prevalence of healthy diet, physical activity, and regular checkup habits by education level:")
        fig1 = create_education_health_behaviors_chart(df)
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("---")
        styled_heading("Key Insights", level=2)
        st.write("""
        - People with higher education levels are more likely to eat well, stay active, and go for regular checkups.
        - The rate of healthy diet, exercise, and screenings all rise from “Less than High School” to “College Graduate".
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
        - As income and education increase together, diabetes rate falls steadily.
        - The lowest diabetes rates appear among those who have completed college education and draw higher income.
        """)
    
    with tab4:
        st.write("**Education's Impact on Lifestyle and Diabetes**")
        st.write("Shows how education levels correspond with lifestyle choices and diabetes rates:")
        fig4 = create_education_lifestyle_diabetes_chart(df)
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("---")
        styled_heading("Key Insights")
        st.write("""
        - At higher education levels, people are more active and eat more fruits and vegetables.
        - Diabetes rates falls steadily as education level rises.
        - This shows a direct link between education, healthy habits, and lower diabetes risk.
        """)

# ============================================================================
# H3: HEALTHCARE ACCESS
# ============================================================================

elif page == "**H3**: Healthcare Access and Diabetes":
    styled_heading("Hypothesis 3: Healthcare Access and Diabetes", level=1, align="center")
    st.write("""
    **Hypothesis**: Limited access to healthcare – due to cost barriers, lack of regular care, or low income – 
    is associated with higher rates of diabetes.
    """)
    st.markdown("---")
    st.write("""
    Next, let’s take a look at how access to healthcare shapes diabetes diagnosis and management!
    """)
    st.write("In the **first tab**, the first graph investigates how healthcare coverage affects diabetes rates, while the second graph looks at how the ability to afford seeing a doctor affects diabetes rates.")
    st.write("The **second tab** compares diabetes rates and healthcare coverage ownership rates across income groups.")
    st.write("The **third tab** examines how the number of healthcare access barriers (lack of coverage and inability to afford seeing a doctor) affects diabetes rates.")

    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs([
        "Coverage & Barriers",
        "Income Trends",
        "Access Barriers",
    ])

    with tab1:
        st.write("**Healthcare Coverage & Cost Barriers to Doctors by Income Level**")
        st.write("Use the dropdown to view data for different income levels:")
        
        # SELECTBOX FOR INCOME LEVEL
        income_options = [
            '< $10k', '$10k-$15k', '$15k-$20k', '$20k-$25k',
            '$25k-$35k', '$35k-$50k', '$50k-$75k', '> $75k'
        ]
        selected_income = st.selectbox(
            "Select income level:",
            income_options,
            index=4,  # Default to $25k-$35k
            key="h3_income"
        )
        
        fig1 = create_healthcare_coverage_chart(df, income_level=selected_income)
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown("---")
        styled_heading("Key Insights")
        st.write("""
        - Diabetes rates are consistently higher among those without healthcare coverage or with cost barriers to doctors.
        - Low-income groups (<$25k) show the largest gap between “Yes” and “No” responses.
        - High income groups (>$75k) show much lower diabetes rates and fewer barriers.
        """)

    with tab2:
        st.write("**Income Level Impact on Healthcare Access and Diabetes**")
        st.write("Left: Diabetes rate by income | Right: Healthcare coverage gaps by income")
        fig2 = create_income_trends_dual_chart(df)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("---")
        styled_heading("Key Insights")
        st.write("""
        - Diabetes rates decline steadily at higher income levels.
        - The lowest-income groups (<$15k) have diabetes rates nearly double that of the highest-income group.
        - As income level increases, diabetes rates and lack of healthcare coverage show a parallel trend of decreasing.
        """)

    with tab3:
        st.write("**Cumulative Effect of Healthcare Access Barriers**")
        st.write("Shows diabetes rates based on number of access barriers (healthcare coverage, cost barrier to doctor):")
        fig3 = create_access_barriers_chart(df)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("---")
        styled_heading("Key Insights")
        st.write("""
        - The quantity of access barriers does not have a significant impact on diabetes rates.
        - Identical rates of diabetes are reported in groups with 0 and 2 barriers, with a minor spike in the group with only 1 barrier.
        - This implies that access to healthcare does not necessarily lower risk of diabetes.
        """)

# ============================================================================
# H4: SELF-RATED HEALTH
# ============================================================================

elif page == "**H4**: Self-Rated Health and Diabetes":
    styled_heading("Hypothesis 4: Self-Rated Health and Diabetes", level=1, align="center")
    st.write("""
    **Hypothesis**: Poor self-rated health and functional limitations – including low general health ratings, 
    more unhealthy days, and difficulty walking – are strongly associated with diabetes.
    """)
    st.markdown("---")
    st.write("""
    Next, let's explore how various health indicators relate to diabetes across different demographic groups.
    """)
    st.write("The **first tab** compares trends between the rate of diabetes against the number of days of poor physical and mental health.")
    st.write("In the **second tab**, the first graph compares walking difficulty with diabetes rate, while the second graph contrasts physical activity against diabetes rate.")
    st.write("The **third tab** investigates the cumulative effect of health limitations on diabetes rates.")

    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs([
        "Health Trends",
        "Functional Limitations",
        "Limitation Impact"
    ])

    with tab1:
        st.write("**Trends in Diabetes vs Unhealthy Days by General Health Rating**")
        st.write("Dual-axis chart showing diabetes rate versus days of poor mental and physical health:")
        fig1 = create_health_trends_chart(df)
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("---")
        styled_heading("Key Insights")
        st.write("""
        - Diabetes rates rise sharply as self-rated health declines (Excellent → Poor).
        - The number of days of poor mental and physical health show a parallel increase.
        - Patterns suggest mutual reinforcement of poor well-being and diabetes.

        """)

    with tab2:
        st.write("**Functional Limitations Comparison**")
        st.write("Left: Difficulty walking | Right: Engagement in Physical Activity")
        fig2 = create_functional_limitations_comparison_chart(df)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("---")
        styled_heading("Key Insights")
        st.write("""
        - Difficulty walking is associated with a significant increase in diabetes rates.
        - In contrast, regular physical activity is observed with lower diabetes rates.
        - Mobility and activity act as strong indications.
        """)

    with tab3:
        st.write("**Effect of Functional Limitations**")
        st.write("Shows how diabetes rates change by number of functional limitations reported:")
        fig4 = create_functional_limitations_chart(df)
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("---")
        styled_heading("Key Insights")
        st.write("""
        - Having even one physical limitation greatly increases the chance of diabetes.
        - The difference in having additional limiations is large and consistent.
        """)

# ============================================================================
# H5: PRE-EXISTING CONDITIONS
# ============================================================================

elif page == "**H5**: Pre-Existing Health Conditions and Diabetes":
    styled_heading("Hypothesis 5: Pre-Existing Health Conditions and Diabetes", level=1, align="center")
    st.write("""
    **Hypothesis**: Individuals with pre-existing cardiometabolic conditions – such as stroke, heart disease or heart attack, 
    high blood pressure, high cholesterol, and elevated BMI – are more likely to be diagnosed with diabetes.
    """)
    st.markdown("---")
    st.write("""
    Finally, we will explore how pre-existing health conditions affect diabetes rates!
    """)
    st.write("Pre-existing conditions include: Stroke, Heart Disease/Attack, High Blood Pressure, High Cholesterol, and Elevated BMI (≥30).")
    st.write("The **first tab** compares the rate of diabetes across individuals who have/don’t have been diagnosed with one of the other four diseases.")
    st.write("The **second tab** explores how having one or more Pre-existing conditions impacts diabetes rates across different age groups.")
    st.write("The **third tab** investigates the rate of diabetes across various BMI categories (based on the USA’s CDC classification).")
    st.write("The **fourth tab** assesses how the accumulation of multiple Pre-existing conditions influences diabetes prevalence.")

    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs([
        "Individual Conditions",
        "By Demographics",
        "BMI Categories",
        "Condition Count"
    ])

    with tab1:
        st.write("**Pre-Existing Conditions and Diabetes Risk**")
        st.write("Use the dropdown to sort by Prevalence (diabetes rate) or Relative Risk (yes/no ratio):")
        
        # SELECTBOX FOR SORT METHOD
        sort_method = st.selectbox(
            "Sort by:",
            ["Prevalence", "Relative Risk"],
            key="h5_sort"
        )
        
        # Map display name to function parameter
        sort_param = "Relative Risk" if "Relative" in sort_method else "Prevalence"
        
        fig1 = create_preexisting_conditions_chart(df, sort_by=sort_param)
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
        - This indicates a strong linear relationship between excess weight and diabetes risk.
        """)

    with tab4:
        st.write("**Effect of Multiple Pre-Existing Conditions**")
        st.write("Shows how diabetes risk increases with each additional condition:")
        fig4 = create_condition_count_chart(df)
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("---")
        styled_heading("Key Insights")
        st.write("""
        - People with other health problems (like high blood pressure or heart disease) are consistently more likely to have diabetes at every age.
        - Men (59.8%) have marginally higher rates than women (57.7%).
        - Aging and the presence of more health conditions both increase the likelihood of diabetes.
        - Each additional condition, up to three, substantially increases the risk of diabetes.
        """)

# ============================================================================
# CONCLUSION
# ============================================================================

elif page == "Conclusion":
    styled_heading("Conclusion", level=1, align="center")
    
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


    # CSS 
    st.markdown("""
    <style>
    :root{
    --card-bg: #ffffff;
    --card-border: #ebedf0;
    --card-shadow: 0 6px 18px rgba(0,0,0,.06);
    --title: #8a0d12;        /* deep red accent */
    --muted: #5b616e;
    --chip-bg: #f5f7fa;
    --chip-text: #3d4551;
    }
    .hypo-grid{
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: 16px;
    margin: 8px 0 4px 0;
    }
    .hypo-card{
    grid-column: span 12;
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 18px 18px 14px 18px;
    box-shadow: var(--card-shadow);
    }
    @media (min-width: 900px){
    .hypo-card.half{ grid-column: span 6; }
    }
    .hypo-title{
    display:flex; align-items:center; gap:10px;
    font-weight: 800; font-size: 20px; color: var(--title); margin: 0 0 8px 0;
    }
    .hypo-title .emoji{ font-size: 22px; }
    .hypo-body{ color:#111; line-height:1.5; margin: 0 0 8px 0; }
    .hypo-muted{ color: var(--muted); }
    .hypo-list{ margin: 6px 0 0 0; padding-left: 20px; }
    .hypo-chip{
    display:inline-block; margin-top:10px;
    background: var(--chip-bg); color: var(--chip-text);
    border: 1px solid #e6e9ef; border-radius: 999px;
    padding: 6px 10px; font-size: 12px; font-weight: 600;
    }
    .hr{ height: 1px; background: #f0f2f6; margin: 10px 0 4px 0; }
    </style>
    """, unsafe_allow_html=True)

    # --- Layout as responsive grid of cards ---
    st.markdown('<div class="hypo-grid">', unsafe_allow_html=True)

    # H1
    st.markdown("""
    <div class="hypo-card">
    <div class="hypo-title"><span class="emoji">🥦</span> H1: Lifestyle Habits</div>
    <p class="hypo-body">
        Modifiable behaviors significantly impact diabetes risk. Smoking, physical inactivity, and poor diet are key factors.
        These are the most controllable risk factors and represent the strongest opportunities for intervention.
    </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")

    # H2
    st.markdown("""
    <div class="hypo-card half">
    <div class="hypo-title"><span class="emoji">🎓</span> H2: Education</div>
    <p class="hypo-body">
        Diabetes prevalence decreases as the level of education increases. Higher education levels also correspond with better lifestyle habits. Public outreach programs targeting demographics with lower education levels can bridge the gap in diabetes prevention knowledge.
    </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")


    # H3
    st.markdown("""
    <div class="hypo-card half">
    <div class="hypo-title"><span class="emoji">🏥</span> H3: Healthcare Access</div>
    <p class="hypo-body">
        Higher rates of diabetes are reported in people with healthcare coverage, stemming from insured individuals who are more likely to be diagnosed due to screening access. Surprisingly, the number of access barriers does not significantly impact diabetes rates, indicating that access to healthcare does not guarantee prevention of diabetes.
    """, unsafe_allow_html=True)
    st.markdown("")
    
    # H4
    st.markdown("""
    <div class="hypo-card half">
    <div class="hypo-title"><span class="emoji">🧭</span> H4: Self-Rated Health</div>
    <p class="hypo-body">
        Self-health assessments, while subjective and informal, are reliable indicators of diabetes risk. Individuals who poorly rated their physical and mental health, as well as mobility and exercise frequency, displayed higher rates of diabetes.
    </p>
    """, unsafe_allow_html=True)
    st.markdown("")

    # H5
    st.markdown("""
    <div class="hypo-card half">
    <div class="hypo-title"><span class="emoji">🫀</span> H5: Pre-Existing Conditions</div>
    <p class="hypo-body">
        Cardiometabolic conditions, stroke and obesity are strongly linked with higher diabetes rates. An increased risk of developing diabetes was observed in higher age demographics, as well as in groups with multiple pre-existing conditions.
    </p>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  

    # Soft divider 
    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

    
    # SECTION 3: Sankey Diagram (NEW!)
    styled_heading("Data Flow & Hypothesis Conclusions")
    st.write("This Sankey diagram visualizes how data variables flow through each hypothesis to their conclusions (Accept/Reject):")
    
    # Display the Sankey diagram
    sankey_fig = create_sankey_diagram()
    st.plotly_chart(sankey_fig, use_container_width=True)
    
    st.info("""
    **Diagram Guide:**
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
        **For Healthcare Providers & Policymakers:**
        1. Promote lifestyle intervention programs
        2. Screen for and manage cardiometabolic risk factors early
        3. Target high-risk populations with community programs
        4. Ensure equitable access to preventive care
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
    st.markdown("---")

    # SECTION 6: Citation
    styled_heading("References")
    st.write(f"""
    - **Dataset**: CDC Diabetes Health Indicators, 50-50 split (diabetes/non-diabetes) https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators
    - **Pictures**: 
    - Arteries -> https://commons.wikimedia.org/wiki/File:Arterial_System.png 
    - Body -> https://www.hiclipart.com/free-transparent-background-png-clipart-pxirg 
    - Brain -> https://www.dreamstime.com/stock-illustration-brain-front-view-icon-human-hnternal-organs-symbol-vector-illustration-cartoon-style-isolated-white-background-image89183850 
    - Heart -> https://www.istockphoto.com/vector/anatomical-heart-isolated-heart-diagnostic-center-sign-human-heart-cartoon-design-gm1177145926-328507854 
    - Left and Right Kidneys -> https://pngtree.com/freepng/human-kidney_16414842.html 
    - Liver -> https://pngtree.com/freepng/liver-frontal-liver-clip-art_6017745.html 
    - Lungs -> https://pngtree.com/freepng/vector-illustration-of-lung-anatomy-in-medical-biology-set-against-a-white-background-vector_12922676.html 
    - Pancreas -> https://pngtree.com/freepng/human-pancreas_16414480.html 
    - Stomach -> https://pngtree.com/freepng/visceral-stomach_5420103.html 
    """)